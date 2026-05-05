import platform
from manim import *
import itertools
import numpy as np

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
    def safe_place(self, mob, *preferred_positions, padding=0.15):
        """
        将 mob 放到第一个不与现有元素重叠的位置。
        preferred_positions: 一系列 (x, y) 或 'UP', 'DOWN', 'LEFT', 'RIGHT' 等字符串。
        用法：self.safe_place(title, UP, LEFT+UP, RIGHT+UP)
        """
        existing = [m for m in self.mobjects if m is not mob]

        for pos in preferred_positions:
            if isinstance(pos, str):
                # 处理方向字符串
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

            # 检查是否和现有元素重叠
            mob_box = get_mobject_bbox(mob)
            overlap = False
            for ex in existing:
                ex_box = get_mobject_bbox(ex)
                if aabboxes_overlap(mob_box, ex_box, padding):
                    overlap = True
                    break
            if not overlap:
                return  # 找到安全位置，返回

        # 如果所有首选位置都不行，用迭代推开
        all_mobs = existing + [mob]
        new_positions = resolve_overlaps(all_mobs, max_iters=300, step=0.2)
        mob.move_to(new_positions[-1])

    def add_title(self, text, scale=1.1):
        t = Text(text, font=FONT_CN, color=BRAND["text"], font_size=40)
        t.scale(scale)

        # 尝试一系列位置，避免与现有元素重叠
        self.safe_place(
            t,
            "UP",          # 默认顶部
            "LEFT_UP",   # 左上角
            "RIGHT_UP",  # 右上角
            "LEFT_DOWN", # 左下角
            "RIGHT_DOWN", # 右下角
        )

        self.play(Write(t, run_time=DUR["normal"]))
        self.wait(DUR["pause"] * 0.5)
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
