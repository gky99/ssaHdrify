# -*- mode: python ; coding: utf-8 -*-
import argparse
import platform

OS_TYPE = platform.system()

parser = argparse.ArgumentParser()
parser.add_argument("--app-version", action="store", default="0.0.1")
options = parser.parse_args()

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/asset/*', "asset")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ssa_hdrify',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['hdr.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ssa_hdrify',
)
app = BUNDLE(
    coll,
    name='ssa hdrify.app',
    icon='hdr.icns',
    bundle_identifier='ssa hdrify',
    version=options.app_version
)
