#!/usr/bin/env python3
"""渲染高质量视频"""
import os

SCENES = [
    "fourier_transform",
    "double_slit",
    "gravitational_waves", 
    "quantum_tunneling",
    "maxwell_equations",
    "special_relativity",
    "lorenz_attractor"
]

for scene in SCENES:
    print(f"\n{'='*40}\n{scene}")
    
    cls = ''.join(w.capitalize() for w in scene.split('_')) + 'Scene'
    print(f"Rendering HQ...")
    os.system(f'.venv/bin/manim -qh --format=mp4 scenes/{scene}.py {cls} 2>&1 | grep -E "Rendered|ERROR"')

print("\nMixing audio...")

# 混合音频
import json

TIMELINES = {
    "fourier_transform": [
        ("assets/audio/fourier_transform_0.mp3", 0),
        ("assets/audio/fourier_transform_1.mp3", 5.1),
        ("assets/audio/fourier_transform_2.mp3", 8.3),
    ],
    "double_slit": [
        ("assets/audio/double_slit_0.mp3", 0),
        ("assets/audio/double_slit_1.mp3", 4.3),
        ("assets/audio/double_slit_2.mp3", 7.5),
    ],
    "gravitational_waves": [
        ("assets/audio/gravitational_waves_0.mp3", 0),
        ("assets/audio/gravitational_waves_1.mp3", 4.3),
        ("assets/audio/gravitational_waves_2.mp3", 8.0),
        ("assets/audio/gravitational_waves_3.mp3", 11.5),
    ],
    "quantum_tunneling": [
        ("assets/audio/quantum_tunneling_0.mp3", 0),
        ("assets/audio/quantum_tunneling_1.mp3", 3.5),
        ("assets/audio/quantum_tunneling_2.mp3", 6.1),
    ],
    "maxwell_equations": [
        ("assets/audio/maxwell_equations_0.mp3", 0),
        ("assets/audio/maxwell_equations_1.mp3", 3.5),
        ("assets/audio/maxwell_equations_2.mp3", 6.3),
    ],
    "special_relativity": [
        ("assets/audio/special_relativity_0.mp3", 0),
        ("assets/audio/special_relativity_1.mp3", 3.3),
        ("assets/audio/special_relativity_2.mp3", 5.3),
    ],
    "lorenz_attractor": [
        ("assets/audio/lorenz_attractor_0.mp3", 0),
        ("assets/audio/lorenz_attractor_1.mp3", 3.5),
        ("assets/audio/lorenz_attractor_2.mp3", 7.8),
    ],
}

for scene, segments in TIMELINES.items():
    video = f"media/videos/{scene}/1080p60/{scene.title().replace('_','')}Scene.mp4"
    if not os.path.exists(video):
        video = f"media/videos/{scene}/720p60/{scene.title().replace('_','')}Scene.mp4"
    if not os.path.exists(video):
        video = f"media/videos/{scene}/480p15/{scene.title().replace('_','')}Scene.mp4"
    if not os.path.exists(video):
        print(f"No video: {scene}")
        continue
    
    # 混合音频
    inputs = []
    filters = []
    for i, (audio, start) in enumerate(segments):
        if not os.path.exists(audio):
            continue
        ms = int(start * 1000)
        inputs.extend(["-i", audio])
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    
    if not filters:
        continue
    
    fc = ";".join(filters) + ";"
    labels = "".join([f"[a{i}]" for i in range(len(segments))])
    fc += f"{labels}amix=inputs={len(segments)}:duration=longest[aout]"
    
    mixed = f"assets/audio/{scene}_timeline.mp3"
    os.system(f'ffmpeg -y {" ".join(inputs)} -filter_complex "{fc}" -map "[aout]" -c:a mp3 "{mixed}" 2>/dev/null')
    
    out = video.replace(".mp4", "_final.mp4")
    os.system(f'ffmpeg -y -i "{video}" -i "{mixed}" -c:v copy -c:a aac -strict experimental "{out}"')
    print(f"  ✓ {scene}")

print("\n" + "="*40)
print("ALL HQ DONE!")
print("="*40)