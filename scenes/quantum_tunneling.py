import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class QuantumTunnelingScene(BaseScene):
    def construct(self):
        # 标题
        title = self.add_title("量子隧穿：粒子如何穿墙？")

        # 创建势能阱场景（缩小，为文字留空间）
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 3, 1],
            x_length=8, y_length=3.5,
            axis_config={"color": BRAND["grid"], "stroke_width": 1},
            tips=False,
        ).shift(DOWN*1)

        # 势能垒（墙）居中偏右
        barrier = Rectangle(
            width=1.5, height=2.5,
            fill_color=BRAND["secondary"], fill_opacity=0.6,
            stroke_color=BRAND["secondary"], stroke_width=2
        ).move_to(RIGHT*0.5 + DOWN*1)

        barrier_label = Text("势垒", font=FONT_CN, color=BRAND["secondary"], font_size=22)
        barrier_label.next_to(barrier, DOWN, buff=0.3)

        # 经典粒子（左侧）
        classic_particle = Dot(LEFT*3 + DOWN*1, color=BRAND["primary"], radius=0.15)
        classic_label = Text("经典粒子", font=FONT_CN, color=BRAND["primary"], font_size=20)
        classic_label.next_to(classic_particle, DOWN, buff=0.3)

        # 量子粒子（左侧上方）
        quantum_particle = Dot(LEFT*3 + UP*0.3, color=BRAND["accent"], radius=0.15)
        quantum_label = Text("量子粒子", font=FONT_CN, color=BRAND["accent"], font_size=20)
        quantum_label.next_to(quantum_particle, UP, buff=0.3)

        self.play(Create(axes), run_time=0.4)
        self.play(FadeIn(barrier), Write(barrier_label), run_time=0.5)
        self.wait(DUR["pause"])

        # 经典粒子撞墙反弹
        self.play(FadeIn(classic_particle), Write(classic_label), run_time=0.3)
        self.play(
            classic_particle.animate.move_to(LEFT*0.75 + DOWN*1),
            run_time=0.5,
            rate_func=linear
        )
        # 反弹
        self.play(
            classic_particle.animate.move_to(LEFT*2 + DOWN*1),
            run_time=0.5,
            rate_func=linear
        )
        self.wait(DUR["pause"])

        # 清除经典粒子
        self.play(FadeOut(classic_particle), FadeOut(classic_label), run_time=DUR["fast"])

        # 量子粒子：波函数扩散
        self.play(FadeIn(quantum_particle), Write(quantum_label), run_time=0.3)

        # 说明文字（标题下方，自动避撞）
        info = Text("量子粒子以概率波形式存在", font=FONT_CN, color=BRAND["text"], font_size=22)
        info.next_to(title, DOWN, buff=0.4)
        self.play(Write(info), run_time=DUR["normal"])
        self.auto_place(title, info, padding=0.2)

        # 显示波函数扩散（横向排列）
        wave_front = VGroup()
        colors = color_gradient([BRAND["accent"], YELLOW], 8)
        for i, color in enumerate(colors):
            wave_dot = Dot(
                LEFT*3 + RIGHT*(3+i*0.7) + UP*0.3,
                color=color,
                radius=0.1 + (i/7.0)*0.05
            )
            wave_front.add(wave_dot)

        self.play(FadeIn(wave_front), run_time=0.8)

        # 波函数穿过势垒
        self.play(
            wave_front.animate.shift(RIGHT*4),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.3)

        # 显示穿透概率
        self.play(FadeOut(info), run_time=DUR["fast"])

        # 在势垒右侧显示穿透的波
        tunneled_wave = Dot(RIGHT*3 + UP*0.3, color=BRAND["accent"], radius=0.12)
        tunnel_label = Text("有概率穿透！", font=FONT_CN, color=BRAND["accent"], font_size=22)
        tunnel_label.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(tunneled_wave), Write(tunnel_label), run_time=0.6)
        self.auto_place(title, tunnel_label, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 显示公式
        self.quick_clear(
            title, axes, barrier, barrier_label,
            quantum_particle, quantum_label, wave_front,
            tunneled_wave, tunnel_label,
        )

        new_title = self.add_title("隧穿概率：指数衰减")

        # 公式（居中）
        formula = MathTex(
            r"T \approx e^{-2\kappa a}, \quad \kappa = \sqrt{\frac{2m(V_0-E)}{\hbar^2}}",
            font_size=28,
            color=BRAND["text"]
        ).shift(UP*0.3)

        # 解释（公式下方，自动避撞）
        explanation = Text(
            "势垒越宽、越高\n隧穿概率越小",
            font=FONT_CN, color=BRAND["secondary"], font_size=22,
            line_spacing=1.5
        ).next_to(formula, DOWN, buff=0.8)
        self.play(Write(formula), run_time=DUR["slow"])
        self.wait(0.3)
        self.play(FadeIn(explanation), run_time=DUR["normal"])
        self.auto_place(formula, explanation, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.quick_clear(new_title, formula, explanation)
        end = Text("下期：麦克斯韦方程组", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
