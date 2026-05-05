import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class DoubleSlitScene(BaseScene):
    def construct(self):
        # 标题（会自动避免与后续元素重叠）
        title = self.add_title("双缝实验：一个电子如何同时通过两条缝？")

        # 设置场景布局
        # 电子源（左侧）
        source = Dot(LEFT*6, color=BRAND["primary"], radius=0.15)
        source_label = Text("电子源", font=FONT_CN, color=BRAND["primary"], font_size=22)
        source_label.next_to(source, DOWN, buff=0.3)

        # 双缝（中间）
        barrier = Rectangle(width=0.3, height=4, fill_color=GRAY, fill_opacity=0.8, stroke_width=0)
        barrier.move_to(ORIGIN)
        slit1 = Rectangle(width=0.4, height=0.3, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        slit2 = Rectangle(width=0.4, height=0.3, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        slit1.move_to(barrier.get_center() + UP*0.8)
        slit2.move_to(barrier.get_center() + DOWN*0.8)
        slits = VGroup(barrier, slit1, slit2)

        slit_label = Text("双缝", font=FONT_CN, color=WHITE, font_size=22)
        slit_label.next_to(barrier, DOWN, buff=0.3)

        # 屏幕（右侧）
        screen = Line(RIGHT*4 + UP*3, RIGHT*4 + DOWN*3, stroke_color=BRAND["grid"], stroke_width=2)
        screen_label = Text("探测屏", font=FONT_CN, color=BRAND["grid"], font_size=22)
        screen_label.next_to(screen, RIGHT, buff=0.3)

        # 显示装置
        self.play(FadeIn(source), Write(source_label), run_time=0.4)
        self.play(Create(barrier), Create(slit1), Create(slit2), Write(slit_label), run_time=0.5)
        self.play(Create(screen), Write(screen_label), run_time=0.4)
        # 自动调整标签位置，避免重叠
        self.auto_place(source, source_label, barrier, slit1, slit2, screen, screen_label, padding=0.2)
        self.wait(DUR["pause"])

        # 清除标签
        self.play(FadeOut(source_label), FadeOut(slit_label), FadeOut(screen_label), run_time=DUR["fast"])

        # --- 第一阶段：逐个发射电子，累积干涉条纹 ---
        info1 = Text("单个电子逐一发射...", font=FONT_CN, color=BRAND["text"], font_size=26)
        info1.next_to(title, DOWN, buff=0.3)
        self.play(Write(info1), run_time=DUR["normal"])
        # 自动调整 info1 位置，避免与标题重叠
        self.auto_place(title, info1, padding=0.2)

        # 在屏幕上累积点
        screen_points = VGroup()
        np.random.seed(42)

        for i in range(50):
            # 创建电子
            electron = Dot(source.get_center(), color=BRAND["accent"], radius=0.06)

            # 随机选择一个缝
            if np.random.random() > 0.5:
                target_slit = slit1.get_center()
            else:
                target_slit = slit2.get_center()

            # 计算最终落点（干涉图案的随机分布）
            # 使用双缝干涉概率分布
            x_screen = 4
            y_screen = np.random.normal(0, 0.8)  # 高斯分布模拟干涉
            # 加上干涉调制
            interference = np.cos(y_screen * 3)**2
            if np.random.random() > interference * 0.7:
                y_screen = np.random.uniform(-2.5, 2.5)

            final_pos = RIGHT*4 + UP*y_screen

            # 动画：电子移动到缝，然后到屏幕
            self.play(
                electron.animate.move_to(target_slit),
                run_time=0.15,
                rate_func=linear,
            )
            self.play(
                electron.animate.move_to(final_pos),
                run_time=0.15,
                rate_func=linear,
            )
            # 保留痕迹
            hit = Dot(final_pos, color=BRAND["secondary"], radius=0.05, stroke_opacity=0)
            screen_points.add(hit)
            self.add(hit)
            self.remove(electron)

            if i == 15:
                info2 = Text("干涉条纹开始显现！", font=FONT_CN, color=BRAND["accent"], font_size=26)
                info2.next_to(info1, DOWN, buff=0.3)
                self.play(ReplacementTransform(info1, info2), run_time=DUR["normal"])
                self.auto_place(title, info2, padding=0.2)

        self.wait(DUR["pause"])

        # 显示干涉条纹曲线
        info_to_clear = info1 if 'info2' not in locals() else info2
        self.play(FadeOut(info_to_clear), run_time=DUR["fast"])

        # 绘制干涉图案曲线
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 1.2, 0.5],
            x_length=3, y_length=2.5,
            axis_config={"color": BRAND["grid"], "stroke_width": 1},
            tips=False,
        ).move_to(RIGHT*4 + DOWN*0.5)

        def interference_pattern(y):
            return 0.8 * np.cos(y * 3)**2 + 0.2

        pattern = axes.plot(interference_pattern, color=BRAND["primary"], stroke_width=2.5)
        pattern_label = Text("干涉条纹", font=FONT_CN, color=BRAND["primary"], font_size=20)
        pattern_label.next_to(axes, UP, buff=0.2)

        self.play(Create(axes), run_time=0.3)
        self.play(Create(pattern), Write(pattern_label), run_time=0.6)
        # 自动调整图案位置
        self.auto_place(axes, pattern, pattern_label, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # --- 第二阶段：观测缝时，干涉消失 ---
        self.quick_clear(title, source, slits, screen, screen_points, axes, pattern, pattern_label, duration=DUR["fast"])

        # 新标题（自动避免重叠）
        new_title = Text("如果观测电子通过哪条缝...", font=FONT_CN, color=BRAND["text"], font_size=34)
        new_title.to_edge(UP, buff=1.2)
        self.play(ReplacementTransform(title, new_title), run_time=DUR["normal"])
        # 自动调整 new_title 位置
        self.auto_place(new_title, padding=0.2)

        # 重新绘制装置，加上探测器
        self.play(FadeIn(source), Create(barrier), Create(slit1), Create(slit2), Create(screen), run_time=0.5)

        # 添加探测器
        detector1 = Circle(radius=0.2, fill_color=RED, fill_opacity=0.6, stroke_width=0).move_to(slit1.get_center())
        detector2 = Circle(radius=0.2, fill_color=RED, fill_opacity=0.6, stroke_width=0).move_to(slit2.get_center())
        detector_label = Text("探测器", font=FONT_CN, color=RED, font_size=22)
        detector_label.next_to(detector1, UP, buff=0.3)

        self.play(FadeIn(detector1), FadeIn(detector2), Write(detector_label), run_time=0.5)

        info3 = Text("粒子性显现，干涉消失", font=FONT_CN, color=BRAND["secondary"], font_size=26)
        info3.next_to(new_title, DOWN, buff=0.3)
        self.play(Write(info3), run_time=DUR["normal"])
        # 自动调整 info3 位置
        self.auto_place(new_title, info3, padding=0.2)

        # 发射电子，这次没有干涉图案
        screen_points2 = VGroup()
        for i in range(30):
            electron = Dot(source.get_center(), color=BRAND["accent"], radius=0.06)

            # 观测后，电子只通过一条缝，随机均匀分布
            if np.random.random() > 0.5:
                target_slit = slit1.get_center()
                final_y = np.random.uniform(-1.2, -0.3)
            else:
                target_slit = slit2.get_center()
                final_y = np.random.uniform(0.3, 1.2)

            final_pos = RIGHT*4 + UP*final_y

            self.play(
                electron.animate.move_to(target_slit),
                run_time=0.12,
                rate_func=linear,
            )
            # 探测器闪烁
            if target_slit[1] > 0:
                self.play(Flash(detector2, color=RED, flash_radius=0.3), run_time=0.05)
            else:
                self.play(Flash(detector1, color=RED, flash_radius=0.3), run_time=0.05)

            self.play(
                electron.animate.move_to(final_pos),
                run_time=0.12,
                rate_func=linear,
            )
            hit = Dot(final_pos, color=BRAND["secondary"], radius=0.05, stroke_opacity=0)
            screen_points2.add(hit)
            self.add(hit)
            self.remove(electron)

        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.quick_clear(new_title, source, slits, screen, screen_points2, detector1, detector2, detector_label, info3, duration=DUR["fast"])
        end = Text("下期：混沌之父洛伦兹吸引子", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
