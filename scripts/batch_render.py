# scripts/batch_render.py
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent
QUEUE_FILE = ROOT / "config" / "render_queue.json"
OUTPUT_DIR = ROOT / "output"
MEDIA_DIR = ROOT / "media"
QUALITY = "-qh"  # 改为 -ql 可切换为预览质量

def load_queue():
    """加载渲染队列：优先读 JSON，否则自动扫描 scenes/"""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)["scenes"]

    print("🔍 未找到 render_queue.json，自动扫描 scenes/ 目录...")
    queue = []
    scenes_dir = ROOT / "scenes"
    for py in sorted(scenes_dir.glob("*.py")):
        with open(py, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("class ") and "Scene" in line and "(" in line:
                    cls = line.split("(")[0].replace("class ", "").strip()
                    queue.append({"file": str(py.relative_to(ROOT)), "class": cls})
    return queue

def render_scene(item):
    file_rel = item["file"]
    cls = item["class"]
    out_name = f"{cls}_final.mp4"
    
    # 使用当前环境的 python -m manim，最稳定兼容 uv
    cmd = [sys.executable, "-m", "manim", QUALITY, file_rel, cls, "--output_file", out_name]
    
    try:
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
        return out_name
    except subprocess.CalledProcessError as e:
        err_log = e.stderr[-400:].replace("\n", " ")
        print(f"\n❌ {cls} 渲染失败: {err_log}")
        return None

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    queue = load_queue()
    if not queue:
        print("⚠️ 队列为空，请检查 scenes/ 或创建 config/render_queue.json")
        return

    print(f"🎬 准备渲染 {len(queue)} 个场景 | 质量: {QUALITY}")
    success = 0
    for item in tqdm(queue, desc="进度", unit="scene"):
        out_file = render_scene(item)
        if out_file:
            # Manim 输出路径: media/videos/<文件名>/<quality>/xxx.mp4
            matched = list(MEDIA_DIR.glob(f"**/{out_file}"))
            if matched:
                dest = OUTPUT_DIR / out_file
                shutil.move(str(matched[0]), str(dest))
                print(f"✅ 已归档: {dest}")
                success += 1
            else:
                print(f"⚠️ 找不到输出文件 {out_file}")

    print(f"\n🎉 渲染完成! 成功: {success}/{len(queue)} | 文件已移至 output/")

if __name__ == "__main__":
    main()