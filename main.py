#!/usr/bin/env python3
"""入口脚本：调用 batch_render.py 渲染所有场景。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    batch_script = ROOT / "scripts" / "batch_render.py"
    if not batch_script.exists():
        print(f"❌ 找不到 {batch_script}")
        sys.exit(1)
    sys.exit(subprocess.run([sys.executable, str(batch_script)]).returncode)
