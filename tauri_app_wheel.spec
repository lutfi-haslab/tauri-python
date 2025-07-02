# tauri_app_wheel.spec
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

dist_info_path = "/Users/hy4-mac-002/.pyenv/versions/3.13.3/lib/python3.13/site-packages/pytauri_wheel-0.6.0.dist-info"

a = Analysis(
    ['python/src/tauri_app_wheel/__main__.py'],
    pathex=['python/src'],
    debug=False,  # Set to False for production builds
    binaries=[],
    datas=[
        ('python/src/tauri_app_wheel/frontend', 'tauri_app_wheel/frontend'),
        ('python/src/tauri_app_wheel/icons', 'tauri_app_wheel/icons'),
        ('python/src/tauri_app_wheel/capabilities', 'tauri_app_wheel/capabilities'),
        (dist_info_path, 'pytauri_wheel-0.6.0.dist-info'),
        ('python/src/tauri_app_wheel/tauri.conf.json', 'tauri_app_wheel'),
    ],
    hiddenimports=[
        'sniffio',
        'pytauri',
        'pytauri_wheel',
        'pytauri_wheel.ext_mod',
        'pytauri_plugins.notification'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # This is crucial for BUNDLE
    name='tauri-app-wheel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # Set to False for GUI apps
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='tauri-app-wheel'
)

# This is the key part - BUNDLE creates the .app
app = BUNDLE(
    coll,
    name='tauri-app-wheel.app',
    icon='python/src/tauri_app_wheel/icons/icon.ico',  # Add your .icns icon file here
    bundle_identifier='com.haslab.tauriappwheel',
    info_plist={
        'CFBundleName': 'Tauri App Wheel',
        'CFBundleDisplayName': 'Tauri App Wheel',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,  # Set to True for menubar-only apps
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '10.13.0',
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': True
        },
        'NSMicrophoneUsageDescription': 'This app needs microphone access',
        'NSCameraUsageDescription': 'This app needs camera access',
        # Add other permissions as needed
    }
)