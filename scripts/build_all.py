#!/usr/bin/env python3
"""简化批量构建：直接让视频循环配合音频"""
import sys
import os
import glob
from pathlib import Path

SCENES = ["fourier_transform", "double_slit", "gravitational_waves"]

def get_dur(path):
    if not os.path.exists(path): return 0
    try:
        return float(os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"').read().strip())
    except: return 0

def build_one(scene):
    print(f"\n{'='*40}\n{scene}")
    print('='*40)
    
    # 音频
    apath = f"assets/audio/{scene}_all.mp3"
    if not os.path.exists(apath):
        print("No audio"); return False
    ad = get_dur(apath)
    print(f"Audio: {ad:.1f}s")
    
    # 视频
    vpat = f"media/videos/{scene}/480p15/*Scene.mp4"
    vs = [f for f in glob.glob(vpat) if "partial" not in f]
    if not vs: print("No video"); return False
    vpath = max(vs, key=os.path.getmtime)
    vd = get_dur(vpath)
    print(f"Video: {vd:.1f}s")
    
    # 让视频循环配合音频
    out = vpath.replace(".mp4", "_final.mp4")
    loops = max(1, int(ad/vd) + 1)
    
    # 用concat循环
    print(f"Looping video {loops}x...")
    list_file = "/tmp/vlist.txt"
    with open(list_file, "w") as f:
        for _ in range(loops):
            f.write(f"file '{os.path.abspath(vpath)}'\n")
    
    # 先拼接视频
    vcat = vpath.replace(".mp4", "_looped.mp4")
    os.system(f'ffmpeg -y -f concat -safe 0 -i "{list_file}" -c copy -shortest "{vcat}"')
    
    # 再合成音频
    print("Combining...")
    os.system(f'ffmpeg -y -i "{vcat}" -i "{apath}" -c:v copy -c:a aac -strict experimental "{out}"')
    
    fd = get_dur(out)
    print(f"✓ Final: {fd:.1f}s")

for s in SCENES:
    build_one(s)

print("\nDone!")