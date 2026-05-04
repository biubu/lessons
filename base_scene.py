import platform
from manim import *

# 分辨率与帧率由 config/manim.cfg 统一管理

# 🎨 品牌参数（改此处即可全局换肤）
BRAND = {
    "bg": "#111111", "primary": "#00D4FF", "secondary": "#FF6B6B",
    "text": "#F5F5F5", "grid": "#2A2A2A", "accent": "#FFD166",
}
DUR = {"fast": 0.3, "normal": 0.6, "slow": 1.0, "pause": 0.4}

# 中文字体：按系统自动选择
_FONT_MAP = {
    "Darwin": "PingFang SC",
    "Windows": "Microsoft YaHei",
    "Linux": "Noto Sans CJK SC",
}
FONT_CN = _FONT_MAP.get(platform.system(), "Noto Sans CJK SC")


class BaseScene(Scene):
    def setup(self):
        self.grid = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-10, 10, 1],
            background_line_style={"stroke_color": BRAND["grid"], "stroke_width": 0.4},
            faded_line_ratio=2,
        )
        self.add(self.grid)

        self.safe_top = Line(LEFT * 5 + UP * 8.2, RIGHT * 5 + UP * 8.2,
                             stroke_color=RED, stroke_opacity=0.2)
        self.safe_bot = Line(LEFT * 5 + DOWN * 8.2, RIGHT * 5 + DOWN * 8.2,
                             stroke_color=RED, stroke_opacity=0.2)
        self.add(self.safe_top, self.safe_bot)

    def add_title(self, text: str, scale: float = 1.1) -> Text:
        t = Text(text, font=FONT_CN, color=BRAND["text"], font_size=40)
        t.scale(scale).to_edge(UP, buff=1.2)
        self.play(Write(t, run_time=DUR["normal"]))
        self.wait(DUR["pause"] * 0.5)
        return t

    def add_card(self, text: str, pos: list | None = None, scale: float = 1.0) -> VGroup:
        if pos is None:
            pos = ORIGIN
        bg = RoundedRectangle(
            corner_radius=0.15, width=6.5, height=1.2,
            fill_color=BRAND["primary"], fill_opacity=0.12,
            stroke_color=BRAND["primary"],
        )
        tx = Text(text, font=FONT_CN, color=BRAND["secondary"], font_size=34)
        card = VGroup(bg, tx).move_to(pos).scale(scale)
        self.play(FadeIn(card, shift=UP * 0.4), run_time=DUR["slow"])
        return card

    def quick_clear(self, *mobs, duration: float | None = None):
        dur = duration or DUR["fast"]
        if not mobs:
            mobs = self.mobjects
        self.play(*[FadeOut(m) for m in mobs], run_time=dur)
