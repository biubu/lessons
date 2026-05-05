#!/usr/bin/env python3
"""
构建脚本：生成音频 + 渲染视频
用法：python scripts/build_scene.py gravitational_waves
"""
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from audio_manager import generate_audio, AUDIO_DIR
from manim import config

# 场景剧本模板（实际应该从 JSON 文件读取）
SCRIPT_TEMPLATES = {
    "gravitational_waves": [
        "引力波是时空的涟漪，由加速的质量产生",
        "爱因斯坦的广义相对论预言了它的存在",
        "2015年，LIGO首次探测到引力波信号",
        "这开启了引力波天文学的新时代",
    ],
    "fourier_transform": [
        "任何信号都可以分解成不同频率的正弦波",
        "傅里叶变换将信号从时域转换到频域",
        "这是现代信号处理的基石",
    ],
}


def generate_script_audio(scene_name):
    """为场景生成所有音频文件"""
    if scene_name not in SCRIPT_TEMPLATES:
        print(f"No script template for {scene_name}")
        return []

    texts = SCRIPT_TEMPLATES[scene_name]
    results = []

    for i, text in enumerate(texts):
        audio_path, duration = generate_audio(text, scene_name, i)
        results.append({
            "text": text,
            "audio_path": audio_path,
            "duration": duration,
        })
        print(f"  [{i+1}/{len(texts)}] {text[:30]}... ({duration:.1f}s)")

    return results


def render_scene(scene_name, quality="low"):
    """渲染场景视频"""
    scene_class = "".join(word.capitalize() for word in scene_name.split("_")) + "Scene"
    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}[quality]

    cmd = f".venv/bin/manim {quality_flag} --format=mp4 scenes/{scene_name}.py {scene_class}"
    print(f"\nRendering: {cmd}")
    os.system(cmd)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_scene.py <scene_name>")
        print("Available scenes:", ", ".join(SCRIPT_TEMPLATES.keys()))
        return

    scene_name = sys.argv[1]
    quality = sys.argv[2] if len(sys.argv) > 2 else "low"

    print(f"Building scene: {scene_name}")
    print("=" * 50)

    # 生成音频
    print("1. Generating audio...")
    script = generate_script_audio(scene_name)

    # 保存剧本
    script_path = Path("assets/subtitles") / f"{scene_name}.json"
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    print(f"   Script saved to {script_path}")

    # 渲染视频
    print("\n2. Rendering video...")
    render_scene(scene_name, quality)

    print("\nDone!")


if __name__ == "__main__":
    main()
