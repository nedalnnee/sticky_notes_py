# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/dell/Desktop/sticky_notes/src/main.py'],
    pathex=['C:/Users/dell/Desktop/sticky_notes'],
    binaries=[],
    datas=[('C:/Users/dell/Desktop/sticky_notes/assets', 'assets')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'sqlite3'],
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
    a.binaries,
    a.datas,
    [],
    name='StickyNotes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/dell/Desktop/sticky_notes/assets/app_icon.ico'],
)
