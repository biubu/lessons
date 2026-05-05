"""音频生成和管理"""
import asyncio
import json
import os
import glob
from pathlib import Path
import edge_tts

AUDIO_DIR = Path(__file__).parent / "assets" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

SCRIPTS = {
    "fourier_transform": [
        "任何复杂的波形，都可以分解成一系列正弦波的叠加",
        "这就是傅里叶变换的核心思想",
        "从时域到频域，我们看到信号的另一面"
    ],
    "double_slit": [
        "电子既不是波也不是粒子，而是量子物体",
        "当我们观察时，它才变成粒子",
        "这就是量子力学的测量问题"
    ],
    "gravitational_waves": [
        "时空像一张弹性薄膜，质量会使它弯曲",
        "两个黑洞相互旋绕，释放引力波",
        "它们最终合并成一个更大的黑洞",
        "2015年，LIGO首次探测到引力波"
    ],
    "quantum_tunneling": [
        "量子隧穿是一种神奇的量子效应",
        "粒子可以穿过能量壁垒",
        "这在半导体和核聚变中非常重要"
    ],
    "maxwell_equations": [
        "麦克斯韦方程组统一了电和磁",
        "变化的电场产生磁场",
        "变化的磁场产生电场"
    ],
    "special_relativity": [
        "光速对任何观察者都是不变的",
        "时间是相对的",
        "质能等价"
    ],
    "lorenz_attractor": [
        "洛伦兹吸引子展示了混沌的本质",
        "初始条件的微小差异会导致结果的巨大不同",
        "这就是蝴蝶效应"
    ],
}


async def _generate_async(text, output_path, voice=DEFAULT_VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_one(text, output_path, voice=DEFAULT_VOICE):
    if os.path.exists(output_path):
        return get_duration(output_path)
    asyncio.run(_generate_async(text, output_path, voice))
    return get_duration(output_path)


def get_duration(audio_path):
    if not os.path.exists(audio_path):
        return 0
    try:
        from mutagen.mp3 import MP3
        return MP3(audio_path).info.length
    except:
        return 0


def generate_all():
    """生成所有场景音频"""
    for scene_name, texts in SCRIPTS.items():
        for i, text in enumerate(texts):
            audio_path = AUDIO_DIR / f"{scene_name}_{i}.mp3"
            duration = generate_one(text, str(audio_path))
            print(f"  [{i}] {text[:25]}... ({duration:.1f}s)")
    print(f"\n✓ Generated {sum(len(v) for v in SCRIPTS.values())} audio files")


def load_script(scene_name):
    """加载剧本"""
    script_path = Path("assets/subtitles") / f"{scene_name}.json"
    if not script_path.exists():
        return None
    with open(script_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    print("Generating all audio files...")
    generate_all()