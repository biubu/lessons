#!/usr/bin/env python3
"""批量生成所有场景的音频和字幕文件"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio_manager import generate_all_audio, save_script, load_script
from pathlib import Path

# 定义所有场景的剧本
SCRIPTS = {
    "fourier_transform": {
        "title": "傅里叶变换：任意波形都能拆成正弦波",
        "segments": [
            {"text": "任何复杂的波形，都可以分解成一系列正弦波的叠加", "animation": "show_wave"},
            {"text": "这就是傅里叶变换的核心思想", "animation": "show_decompose"},
            {"text": "从时域到频域，我们看到信号的另一面", "animation": "show_frequency"},
        ]
    },
    "double_slit": {
        "title": "双缝实验：一个电子如何同时通过两条缝？",
        "segments": [
            {"text": "电子既不是波也不是粒子，而是量子物体", "animation": "show_electron"},
            {"text": "当我们观察时，它才变成粒子", "animation": "show_observation"},
            {"text": "这就是量子力学的测量问题", "animation": "show_conclusion"},
        ]
    },
    "gravitational_waves": {
        "title": "引力波：时空的涟漪",
        "segments": [
            {"text": "爱因斯坦的广义相对论预言了引力波的存在", "animation": "show_einstein"},
            {"text": "2015年，LIGO首次探测到引力波", "animation": "show_ligo"},
            {"text": "这打开了观测宇宙的新窗口", "animation": "show_universe"},
        ]
    },
}

def main():
    """生成所有音频和字幕文件"""
    for scene_name, script_data in SCRIPTS.items():
        print(f"Generating audio for {scene_name}...")

        # 生成音频
        segments = generate_all_audio(script_data, scene_name)

        # 保存剧本
        save_script(scene_name, {"title": script_data["title"], "segments": segments})

        print(f"  ✓ Generated {len(segments)} audio files")
        for seg in segments:
            print(f"    - {seg['text'][:30]}... ({seg['duration']:.1f}s)")

if __name__ == "__main__":
    main()
