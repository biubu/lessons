import platform
from manim import *
import itertools
import numpy as np
import os
from pathlib import Path

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

BRAND = {
    "bg": "#111111", "primary": "#00D4FF", "secondary": "#FF6B6B",
    "text": "#F5F5F5", "grid": "#2A2A2A", "accent": "#FFD166",
}
DUR = {"fast": 0.3, "normal": 0.6, "slow": 1.0, "pause": 0.4}

_FONT_MAP = {
    "Darwin": "PingFang SC",
    "Windows": "Microsoft YaHei",
    "Linux": "Noto Sans CJK SC",
}
FONT_CN = _FONT_MAP.get(platform.system(), "Noto Sans CJK SC")

X_MIN, X_MAX = -7.1, 7.1
Y_MIN, Y_MAX = -4, 4

SUBTITLE_STYLE = {
    "font": FONT_CN,
    "font_size": 28,
    "color": BRAND["text"],
    "fill_opacity": 0.9,
}


def get_mobject_bbox(mob):
    try:
        c1 = mob.get_critical_point(UL)
        c2 = mob.get_critical_point(DR)
        return (c1[0], c2[0], c1[1], c2[1])
    except Exception:
        p = mob.get_center()
        return (p[0]-0.1, p[0]+0.1, p[1]-0.1, p[1]+0.1)


def aabboxes_overlap(box1, box2, padding=0.05):
    x1_min, x1_max, y1_min, y1_max = box1
    x2_min, x2_max, y2_min, y2_max = box2
    if x1_max + padding < x2_min - padding or x2_max + padding < x1_min - padding:
        return False
    if y1_max + padding < y2_min - padding or y2_max + padding < y1_min - padding:
        return False
    return True


def resolve_overlaps(mobjects, max_iters=500, step=0.15):
    positions = [m.get_center().copy() for m in mobjects]
    for _ in range(max_iters):
        moved = False
        for i, j in itertools.combinations(range(len(mobjects)), 2):
            box_i = get_mobject_bbox(mobjects[i])
            box_j = get_mobject_bbox(mobjects[j])
            if not aabboxes_overlap(box_i, box_j, 0.1):
                continue
            center_i = positions[i]
            center_j = positions[j]
            diff = center_j - center_i
            if diff[0] == 0 and diff[1] == 0:
                diff = np.array([0.1, 0.1, 0])
            dist = np.linalg.norm(diff)
            if dist == 0:
                continue
            normal = diff / dist
            positions[i] -= normal * step
            positions[j] += normal * step
            positions[i][0] = np.clip(positions[i][0], X_MIN, X_MAX)
            positions[i][1] = np.clip(positions[i][1], Y_MIN, Y_MAX)
            positions[j][0] = np.clip(positions[j][0], X_MIN, X_MAX)
            positions[j][1] = np.clip(positions[j][1], Y_MIN, Y_MAX)
            moved = True
        if not moved:
            break
    return positions


class BaseScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_title = None
        self._current_subtitle = None
        self._audio_enabled = True
        self._subtitle_enabled = True

    def play_audio(self, audio_path, animation=None, wait_time=None):
        duration = wait_time
        if duration is None and os.path.exists(audio_path):
            try:
                from mutagen.mp3 import MP3
                duration = MP3(audio_path).info.length
            except Exception:
                duration = DUR["normal"]
        duration = duration or DUR["normal"]
        if self._audio_enabled and os.path.exists(audio_path):
            self.add_sound(audio_path)
        if animation:
            self.play(animation, run_time=duration)
        else:
            self.wait(duration)

    def show_subtitle(self, text, duration=None, audio_path=None, position=DOWN):
        if self._current_subtitle and self._current_subtitle in self.mobjects:
            self.remove(self._current_subtitle)
        subtitle = Text(text, **SUBTITLE_STYLE)
        subtitle.to_edge(position, buff=0.3)
        self._current_subtitle = subtitle
        if duration is None and audio_path and os.path.exists(audio_path):
            try:
                from mutagen.mp3 import MP3
                duration = MP3(audio_path).info.length
            except Exception:
                duration = DUR["normal"]
        elif duration is None:
            duration = DUR["normal"]
        self.add(subtitle)
        if audio_path and self._audio_enabled and os.path.exists(audio_path):
            self.play_audio(audio_path, wait_time=duration)
        else:
            self.wait(duration)
        self.remove(subtitle)
        self._current_subtitle = None

    def play_with_narration(self, script_path=None):
        import json
        if script_path is None:
            scene_name = self.__class__.__name__.replace("Scene", "").lower()
            script_path = f"assets/subtitles/{scene_name}.json"
        if not os.path.exists(script_path):
            print(f"Script not found: {script_path}")
            return
        with open(script_path, 'r', encoding='utf-8') as f:
            script = json.load(f)
        title_text = script.get("title", "")
        if title_text:
            self.add_title(title_text)
        segments = script.get("segments", [])
        for i, seg in enumerate(segments):
            text = seg.get("text", "")
            audio = seg.get("audio", "")
            duration = seg.get("duration") or self._get_audio_duration(audio)
            if audio and os.path.exists(audio):
                self.add_sound(audio)
            subtitle = Text(text, **SUBTITLE_STYLE)
            subtitle.to_edge(DOWN, buff=0.3)
            self.add(subtitle)
            self.wait(duration)
            self.remove(subtitle)
            extra = duration * 0.3
            self.wait(extra)

    def _get_audio_duration(self, audio_path):
        if not audio_path or not os.path.exists(audio_path):
            return DUR["normal"]
        try:
            from mutagen.mp3 import MP3
            return MP3(audio_path).info.length
        except:
            return DUR["normal"]

    def safe_place(self, mob, *preferred_positions, padding=0.15):
        existing = [m for m in self.mobjects if m is not mob]
        for pos in preferred_positions:
            if isinstance(pos, str):
                if pos == "UP":
                    mob.to_edge(UP, buff=1.2)
                elif pos == "DOWN":
                    mob.to_edge(DOWN, buff=0.8)
                elif pos == "LEFT_UP":
                    mob.to_corner(UL, buff=0.8)
                elif pos == "RIGHT_UP":
                    mob.to_corner(UR, buff=0.8)
                elif pos == "LEFT_DOWN":
                    mob.to_corner(DL, buff=0.8)
                elif pos == "RIGHT_DOWN":
                    mob.to_corner(DR, buff=0.8)
                else:
                    mob.move_to(ORIGIN)
            else:
                mob.move_to(np.array([pos[0], pos[1], 0]))
            mob_box = get_mobject_bbox(mob)
            overlap = False
            for ex in existing:
                ex_box = get_mobject_bbox(ex)
                if aabboxes_overlap(mob_box, ex_box, padding):
                    overlap = True
                    break
            if not overlap:
                return
        all_mobs = existing + [mob]
        new_positions = resolve_overlaps(all_mobs, max_iters=300, step=0.2)
        mob.move_to(new_positions[-1])

    def add_title(self, text, scale=1.1):
        if self._current_title and self._current_title in self.mobjects:
            self.play(FadeOut(self._current_title, run_time=DUR["fast"]))
        t = Text(text, font=FONT_CN, color=BRAND["text"], font_size=40)
        t.scale(scale)
        self.safe_place(t, "UP", "LEFT_UP", "RIGHT_UP", "LEFT_DOWN", "RIGHT_DOWN")
        self.play(Write(t, run_time=DUR["normal"]))
        self.wait(DUR["pause"] * 0.5)
        self._current_title = t
        return t

    def quick_clear(self, *mobs, duration=None):
        dur = duration if duration is not None else DUR["fast"]
        if not mobs:
            mobs = self.mobjects
        self.play(*[FadeOut(m) for m in mobs], run_time=dur)

    def auto_place(self, *mobjects, padding=0.15, max_iters=300):
        mlist = list(mobjects)
        new_positions = resolve_overlaps(mlist, max_iters=max_iters, step=padding)
        for mob, pos in zip(mlist, new_positions):
            mob.move_to(pos)