# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Ui.py'],
             pathex=['D:\\python\\zsw\\Gui\\real'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [('list-icon.png','D:\\python\\zsw\\Gui\\real\\list-icon.png','DATA'),('logo.png','D:\\python\\zsw\\Gui\\real\\logo.png','DATA'),('images.png','D:\\python\\zsw\\Gui\\real\\images.png','DATA'),('add.png','D:\\python\\zsw\\Gui\\real\\add.png','DATA'),('content.png','D:\\python\\zsw\\Gui\\real\\content.png','DATA'),('dec.png','D:\\python\\zsw\\Gui\\real\\dec.png','DATA'),('go.png','D:\\python\\zsw\\Gui\\real\\go.png','DATA'),('goType.png','D:\\python\\zsw\\Gui\\real\\goType.png','DATA'),('set.png','D:\\python\\zsw\\Gui\\real\\set.png','DATA'),('title.png','D:\\python\\zsw\\Gui\\real\\title.png','DATA'),('user.png','D:\\python\\zsw\\Gui\\real\\user.png','DATA'),('userSet.png','D:\\python\\zsw\\Gui\\real\\userSet.png','DATA')],
          [],
          name='Ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
