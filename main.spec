# -*- mode: python ; coding: utf-8 -*-
import sys
import os

from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks
from kivy_deps import sdl2, glew, gstreamer

from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None

path = os.path.abspath(".")

a = Analysis(
    ['main.py'],
    pathex=[path],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=runtime_hooks(),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    **get_deps_all()
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    Tree(r'C:\\Users\\tauan\\OneDrive\\Documentos\\Scripts\\App Dan Base'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RPG',
)
