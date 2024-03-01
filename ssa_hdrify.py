"""调整SSA字幕亮度。"""

from __future__ import annotations

import argparse
import os
import re
from tkinter import Tk, filedialog

import ass as ssa
import colour
import numpy as np
from colour import RGB_Colourspace
from colour.models import eotf_inverse_BT2100_PQ, sRGB_to_XYZ, XYZ_to_xyY, xyY_to_XYZ, XYZ_to_RGB, \
    RGB_COLOURSPACE_BT2020, eotf_BT2100_PQ

COLOURSPACE_BT2100_PQ = RGB_Colourspace(
    name='COLOURSPACE_BT2100',
    primaries=RGB_COLOURSPACE_BT2020.primaries,
    whitepoint=RGB_COLOURSPACE_BT2020.whitepoint,
    matrix_RGB_to_XYZ=RGB_COLOURSPACE_BT2020.matrix_RGB_to_XYZ,
    matrix_XYZ_to_RGB=RGB_COLOURSPACE_BT2020.matrix_XYZ_to_RGB,
    cctf_encoding=eotf_inverse_BT2100_PQ,
    cctf_decoding=eotf_BT2100_PQ,
)
"""HDR color space on display side."""


def files_picker() -> list[str]:
    """询问用户并返回字幕文件"""
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilenames(filetypes=[('ASS files', '.ass .ssa'),
                                                  ('all files', '.*')])


def apply_oetf(source: list[float], luma: float):
    """
    args:
    source: linear RGB tuple (0-1, 0-1, 0-1)
    luma: luma value for the ORIGINAL sRGB colour.
    """
    args = parse_args()
    pq_result = colour.oetf(source, 'ITU-R BT.2100 PQ')
    hlg_result = colour.oetf(source, 'ITU-R BT.2100 HLG')

    if args.gamma == 'pq':
        return pq_result
    elif args.gamma == 'hlg':
        return hlg_result
    else:
        # linear mix between 0.1 and 0.2
        pq_mix_ratio = (np.clip(luma, 0.1, 0.2) - 0.1) / 0.1
        return hlg_result * (1 - pq_mix_ratio) + pq_result * pq_mix_ratio


def sRgbToHdr(source: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Convert RGB color in SDR color space to HDR color space.

    How it works:
     1. Convert the RGB color to reference xyY color space to get absolute chromaticity and linear luminance response
     2. Time the target brightness of SDR color space to the Y because Rec.2100 has an absolute luminance
     3. Convert the xyY color back to RGB under Rec.2100/Rec.2020 color space.

    Notes:
     -  Unlike sRGB and Rec.709 color space which have their OOTF(E) = EOTF(OETF(E)) equals or almost equals to y = x,
        it's OOTF is something close to gamma 2.4. Therefore, to have matched display color for color in SDR color space
        the COLOURSPACE_BT2100_PQ denotes a display color space rather than a scene color space. It wasted me quite some
        time to figure that out :(
     -  Option to set output luminance is removed because PQ has an absolute luminance level, which means any color in
        the Rec.2100 color space will be displayed the same on any accurate display regardless of the capable peak
        brightness of the device if no clipping happens. Therefore, the peak brightness should always target 10000 nits
        so the SDR color can be accurately projected to the sub-range of Rec.2100 color space
    args:
    colour -- (0-255, 0-255, 0-255)
    """
    args = parse_args()
    srgb_brightness = args.sub_brightness

    normalized_sdr_color = np.array(source) / 255
    xyY_sdr_color = XYZ_to_xyY(sRGB_to_XYZ(normalized_sdr_color, apply_cctf_decoding=True))

    xyY_hdr_color = xyY_sdr_color.copy()
    target_luminance = xyY_sdr_color[2] * srgb_brightness
    xyY_hdr_color[2] = target_luminance

    output = XYZ_to_RGB(xyY_to_XYZ(xyY_hdr_color), colourspace=COLOURSPACE_BT2100_PQ, apply_cctf_encoding=True)

    output = np.round(output * 255)

    return (int(output[0]), int(output[1]), int(output[2]))


def transformColour(colour):
    rgb = (colour.r, colour.g, colour.b)
    transformed = sRgbToHdr(rgb)
    colour.r = transformed[0]
    colour.g = transformed[1]
    colour.b = transformed[2]


def transformEvent(event):
    line = event.text
    matches = []
    for match in re.finditer(r'\\[0-9]?c&H([0-9a-fA-F]{2,})&', line):
        start = match.start(1)
        end = match.end(1)
        hex_colour = match.group(1)
        hex_colour.rjust(6, '0')
        b = int(hex_colour[0:2], 16)
        g = int(hex_colour[2:4], 16)
        r = int(hex_colour[4:6], 16)
        (r, g, b) = sRgbToHdr((r, g, b))
        hex_colour = '{:02x}{:02x}{:02x}'.format(b, g, r)
        matches.append((start, end, hex_colour.upper()))

    for start, end, hex_colour in matches:
        line = line[:start] + hex_colour + line[end:]

    event.text = line


def ssaProcessor(fname: str):
    if not os.path.isfile(fname):
        print(f'Missing file: {fname}')
        return

    with open(fname, encoding='utf_8_sig') as f:
        sub = ssa.parse(f)
    for s in sub.styles:
        transformColour(s.primary_color)
        transformColour(s.secondary_color)
        transformColour(s.outline_color)
        transformColour(s.back_color)

    for e in sub.events:
        transformEvent(e)

    output_fname = os.path.splitext(fname)
    output_fname = output_fname[0] + '.hdr.ass'

    with open(output_fname, 'w', encoding='utf_8_sig') as f:
        sub.dump_file(f)
        print(f'Wrote {output_fname}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--sub-brightness',
                        metavar='val',
                        type=int,
                        help=("设置字幕最大亮度，纯白色字幕将被映射为该亮度。"
                              "(默认: %(default)s)"),
                        default=100)
    parser.add_argument('-f',
                        '--file',
                        metavar='path',
                        type=str,
                        help=('输入字幕文件。可重复添加。'),
                        action='append')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()
    files = args.file
    if not files:
        files = files_picker()
    for f in files:
        ssaProcessor(f)

    print("Press Enter to exit...")
    input("按回车键退出...")
