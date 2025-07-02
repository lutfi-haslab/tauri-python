# PyTauri-Wheel+ Vanilla TS

`pytauri-wheel` provides precompiled dynamic libraries, so you no longer need a Rust compiler. You can run Tauri applications with just Python.

---

```bash
git clone https://github.com/pytauri/pytauri.git
cd pytauri

# build frontend assets
bun install
bun run build

# activate virtual environment
uv venv
source .venv/bin/activate
# or powershell: .venv\Scripts\Activate.ps1

# This step will compile `pytauri-wheel` locally (requires Rust compiler),
# or you can download the precompiled `pytauri-wheel` from PyPi.
uv pip install --reinstall -e python/pytauri-wheel

cd examples/tauri-app-wheel

# install the example package
pipenv install --reinstall -e ./python
```

## Run in Development Mode

```bash
bun run dev  # launch Vite dev server
python -m jurigged -w python/src -v python/src/tauri_app_wheel/__main__.py
```

then in another terminal:

```bash
# Set environment variable to tell `tauri_app_wheel` to
# use vite dev server as the frontend dist,
# see `python/src/tauri_app_wheel/__init__.py` for details
export TAURI_APP_WHEEL_DEV=1 # 0 for production
# or in powershell: $env:TAURI_APP_WHEEL_DEV=1

python -m tauri_app_wheel
```

## Run in Production Mode

```bash
pnpm build  # build frontend assets
export TAURI_APP_WHEEL_DEV=0
python -m tauri_app_wheel
```

## Build SDist and Wheel

```bash
bun run build  # build frontend assets
uv build ./python

pipenv run pyinstaller tauri_app_wheel.spec
```
