import sys
sys.setrecursionlimit(5000)
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Agilent_Quotes_Tracker.py'],
             pathex=['C:\\Users\\derbates\\OneDrive - Agilent Technologies\\Documents\\_staging\\Data-Developer-Droolkit\\pyinstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Agilent_Quotes_Tracker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Agilent_Quotes_Tracker')