#!/usr/bin/env python3
"""用 ffmpeg 将音频合成到视频中"""
import sys
import os
from pathlib import Path

def combine_audio_video(video_path, audio_path, output_path=None):
    """将音频合成到视频中"""
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"Audio not found: {audio_path}")
        return False
    
    if output_path is None:
        output_path = video_path.replace(".mp4", "_with_audio.mp4")
    
    # 用 ffmpeg 合成
    cmd = f'ffmpeg -y -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_path}"'
    print(f"Running: {cmd}")
    os.system(cmd)
    
    print(f"Output: {output_path}")
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/combine_audio.py <video.mp4> <audio.mp3>")
        return
    
    video_path = sys.argv[1]
    audio_path = sys.argv[2]
    combine_audio_video(video_path, audio_path)

if __name__ == "__main__":
    main()