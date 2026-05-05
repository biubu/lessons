import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class GravitationalWavesScene(BaseScene):
    def construct(self):
        # 标题
        title = self.add_title("引力波：时空的涟漪")

        # 说明1（标题下方，自动避撞）
        info1 = Text("时空像一张弹性薄膜", font=FONT_CN, color=BRAND["text"], font_size=22)
        info1.next_to(title, DOWN, buff=0.5)
        self.play(Write(info1), run_time=DUR["normal"])
        self.auto_place(title, info1, padding=0.2)

        # 网格（居中）
        grid = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_color": BRAND["grid"], "stroke_width": 1, "stroke_opacity": 0.8},
            faded_line_ratio=2,
        ).scale(0.6)

        self.play(Create(grid), run_time=0.8)
        self.wait(DUR["pause"])

        # 黑洞（居中）
        black_hole = Circle(radius=0.4, fill_color=BLACK, fill_opacity=1, stroke_color=BRAND["secondary"], stroke_width=2)
        bh_label = Text("黑洞", font=FONT_CN, color=BRAND["secondary"], font_size=20)
        bh_label.next_to(black_hole, DOWN, buff=0.3)

        self.play(FadeIn(black_hole), Write(bh_label), run_time=0.5)
        # 自动调整黑洞标签位置
        self.auto_place(black_hole, bh_label, padding=0.2)
        self.wait(0.3)

        # 网格弯曲
        self.play(grid.animate.scale(1.2), run_time=1.0)
        self.wait(DUR["pause"])

        # 清除说明
        self.play(FadeOut(info1), run_time=DUR["fast"])

        # 说明2
        info2 = Text("两个黑洞相互旋绕", font=FONT_CN, color=BRAND["text"], font_size=22)
        info2.next_to(title, DOWN, buff=0.5)
        self.play(Write(info2), run_time=DUR["normal"])

        # 两个黑洞（左右）
        bh1 = Circle(radius=0.3, fill_color=BLACK, fill_opacity=1, stroke_color=BRAND["secondary"], stroke_width=2)
        bh2 = Circle(radius=0.3, fill_color=BLACK, fill_opacity=1, stroke_color=BRAND["secondary"], stroke_width=2)
        bh1.move_to(LEFT*2.5)
        bh2.move_to(RIGHT*2.5)

        self.auto_place(title, info2, bh1, bh2, padding=0.2)
        self.play(FadeIn(bh1), FadeIn(bh2), run_time=0.5)

        # 旋绕动画
        tracker = ValueTracker(0)
        orbit_center = ORIGIN
        radius_orbit = 2.5

        bh_group = VGroup(bh1, bh2)

        def update_bh(mob):
            angle = tracker.get_value()
            mob[0].move_to(orbit_center + radius_orbit * np.array([np.cos(angle), np.sin(angle), 0]))
            mob[1].move_to(orbit_center + radius_orbit * np.array([np.cos(angle + PI), np.sin(angle + PI), 0]))

        bh_group.add_updater(update_bh)
        self.add(bh_group)
        self.play(tracker.animate.set_value(4*PI), run_time=3, rate_func=linear)
        bh_group.remove_updater(update_bh)

        self.wait(DUR["pause"])

        # 合并说明
        self.play(FadeOut(info2), FadeOut(grid), run_time=DUR["fast"])
        info3 = Text("合并瞬间：引力波爆发！", font=FONT_CN, color=BRAND["accent"], font_size=22)
        info3.next_to(title, DOWN, buff=0.5)
        self.play(Write(info3), run_time=DUR["normal"])

        # 合并后的黑洞
        merged_bh = Circle(radius=0.5, fill_color=BLACK, fill_opacity=1, stroke_color=BRAND["secondary"], stroke_width=3)
        self.auto_place(title, info3, merged_bh, padding=0.2)
        self.play(FadeIn(merged_bh), run_time=0.6)

        # 涟漪扩散
        ripple1 = Circle(radius=0.5, stroke_color=BRAND["primary"], stroke_width=2, fill_opacity=0)
        ripple2 = Circle(radius=0.5, stroke_color=BRAND["primary"], stroke_width=2, fill_opacity=0)
        ripple3 = Circle(radius=0.5, stroke_color=BRAND["primary"], stroke_width=2, fill_opacity=0)
        self.add(ripple1, ripple2, ripple3)

        self.play(ripple1.animate(rate_func=linear).scale(4).set_stroke(opacity=0), run_time=1.5)
        self.play(ripple2.animate(rate_func=linear).scale(6).set_stroke(opacity=0), run_time=1.5)
        self.play(ripple3.animate(rate_func=linear).scale(8).set_stroke(opacity=0), run_time=1.5)
        self.wait(DUR["pause"] * 1.5)

        # LIGO探测
        self.play(FadeOut(info3), FadeOut(merged_bh), FadeOut(ripple1), FadeOut(ripple2), FadeOut(ripple3), run_time=DUR["fast"])
        final_title = self.add_title("2015年 LIGO 首次探测到引力波")

        # 探测器（下方，自动避撞）
        detector = Rectangle(width=8, height=1.5, fill_color=BRAND["grid"], fill_opacity=0.3, stroke_color=WHITE, stroke_width=1)
        detector.move_to(DOWN*1.8)

        laser = Dot(LEFT*3 + DOWN*1.8, color=RED, radius=0.1)
        laser_label = Text("激光", font=FONT_CN, color=RED, font_size=18)
        laser_label.next_to(laser, DOWN, buff=0.2)

        splitter = Square(0.4, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        splitter.move_to(DOWN*1.8)

        mirror1 = Line(DOWN*1.65 + RIGHT*2, DOWN*1.95 + RIGHT*2, stroke_color=WHITE, stroke_width=3)
        mirror2 = Line(DOWN*1.65 + LEFT*2, DOWN*1.95 + LEFT*2, stroke_color=WHITE, stroke_width=3)

        self.play(Create(detector), run_time=0.4)
        self.play(FadeIn(laser), Write(laser_label), run_time=0.3)
        self.play(FadeIn(splitter), Create(mirror1), Create(mirror2), run_time=0.4)
        # 自动调整探测器组件位置
        self.auto_place(detector, laser, laser_label, splitter, mirror1, mirror2, padding=0.2)

        # 干涉条纹
        interference = VGroup(*[
            Line(LEFT*2.5 + DOWN*(1.8 + i*0.12), RIGHT*2.5 + DOWN*(1.8 + i*0.12),
                 stroke_color=BRAND["accent"], stroke_width=1) for i in range(-5, 6)
        ])
        self.play(Create(interference), run_time=0.6)
        # 自动调整干涉条纹位置
        self.auto_place(interference, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.play(*[FadeOut(m) for m in [final_title, detector, laser, laser_label, splitter, mirror1, mirror2, interference]], run_time=DUR["fast"])
        end = Text("下期：狭义相对论", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
