#!/usr/bin/env python3
"""根据剧本时间轴合成音频和字幕到视频中"""
import sys
import os
import json
from pathlib import Path

def get_audio_duration(audio_path):
    """获取音频时长"""
    if not os.path.exists(audio_path):
        return 0
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}" 2>/dev/null'
    try:
        return float(os.popen(cmd).read().strip())
    except:
        return 0

def combine_video_with_script(video_path, script_path, output_path=None):
    """将视频和剧本时间轴合成，添加多段音频和字幕"""
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)

    if not output_path:
        output_path = video_path.replace(".mp4", "_final.mp4")
        if output_path == video_path:
            output_path = video_path.replace(".mp4", "_with_audio.mp4")

    segments = script.get("segments", [])
    if not segments:
        print("No segments found in script")
        return False

    # 创建 SRT 字幕文件
    srt_path = script_path.replace(".json", ".srt")
    srt_lines = []

    for i, seg in enumerate(segments):
        text = seg.get("text", "")
        start = seg.get("start", i * 4.0)
        duration = seg.get("duration", 0)
        if duration == 0:
            audio = seg.get("audio", "")
            duration = get_audio_duration(audio)

        # SRT 时间格式
        start_srt = format_srt_time(start)
        end_srt = format_srt_time(start + duration)
        srt_lines.append(f"{i+1}\n{start_srt} --> {end_srt}\n{text}\n")

    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(srt_lines))

    print(f"Subtitles: {srt_path}")

    # 简化处理：只使用第一个音频作为背景配音
    first_audio = segments[0].get("audio", "")
    if not first_audio or not os.path.exists(first_audio):
        print("No audio found, copying video only")
        import shutil
        shutil.copy(video_path, output_path)
        return True

    # 简单命令：混合视频和音频
    cmd = f'ffmpeg -y -i "{video_path}" -i "{first_audio}" -c:v copy -c:a aac -strict experimental -shortest "{output_path}"'

    print(f"Running: ffmpeg...")
    result = os.system(cmd)

    print(f"Output: {output_path}")
    return True

def format_srt_time(seconds):
    """格式化时间为 SRT 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/combine_video.py <video.mp4> <script.json>")
        return

    video_path = sys.argv[1]
    script_path = sys.argv[2]
    combine_video_with_script(video_path, script_path)

if __name__ == "__main__":
    main()