import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class MaxwellEquationsScene(BaseScene):
    def construct(self):
        # 标题
        title = self.add_title("麦克斯韦方程组：电与磁的统一")

        # 说明1（标题下方）
        info1 = Text("静电场：电荷产生电场", font=FONT_CN, color=BRAND["text"], font_size=22)
        info1.next_to(title, DOWN, buff=0.5)
        self.play(Write(info1), run_time=DUR["normal"])

        # 左侧：正负电荷
        charge_plus = Dot(LEFT*3 + UP*0.5, color=RED, radius=0.15)
        charge_minus = Dot(LEFT*3 + DOWN*0.5, color=BLUE, radius=0.15)
        plus_label = Text("+", font_size=24, color=WHITE).move_to(charge_plus)
        minus_label = Text("-", font_size=24, color=WHITE).move_to(charge_minus)

        # 电场线
        field_lines_left = VGroup()
        for angle in np.linspace(-PI/3, PI/3, 5):
            line = Arrow(charge_plus.get_center() + 0.2*RIGHT, charge_minus.get_center() + 0.2*RIGHT,
                        buff=0.2, stroke_color=BRAND["primary"], stroke_width=1.5)
            field_lines_left.add(line)

        label_electric = Text("静电场", font=FONT_CN, color=BRAND["primary"], font_size=20)
        label_electric.next_to(charge_plus, UP, buff=0.3)

        self.play(FadeIn(charge_plus), FadeIn(charge_minus), Write(plus_label), Write(minus_label), run_time=0.4)
        self.play(Create(field_lines_left), Write(label_electric), run_time=0.6)
        self.wait(DUR["pause"])

        # 右侧：电流产生磁场
        wire = Line(RIGHT*2 + UP*1, RIGHT*2 + DOWN*1, stroke_color=BRAND["accent"], stroke_width=3)
        wire_label = Text("电流", font=FONT_CN, color=BRAND["accent"], font_size=20)
        wire_label.next_to(wire, RIGHT, buff=0.3)

        field_lines_right = VGroup()
        for angle in np.linspace(0, 2*PI, 8, endpoint=False):
            arc = Arc(radius=0.5, angle=PI/4, start_angle=angle, stroke_color=BRAND["secondary"], stroke_width=1.5).move_to(wire.get_center() + RIGHT*2)
            field_lines_right.add(arc)

        label_magnetic = Text("静磁场", font=FONT_CN, color=BRAND["secondary"], font_size=20)
        label_magnetic.next_to(wire, UP, buff=0.3)

        self.play(Create(wire), Write(wire_label), run_time=0.4)
        self.play(Create(field_lines_right), Write(label_magnetic), run_time=0.6)
        self.wait(DUR["pause"])

        # 清除第一部分
        self.play(*[FadeOut(m) for m in [info1, charge_plus, charge_minus, plus_label, minus_label,
                                         field_lines_left, label_electric, wire, wire_label,
                                         field_lines_right, label_magnetic]], run_time=DUR["fast"])

        # 变化的电场产生磁场
        new_title = self.add_title("变化的电场 → 磁场")

        info2 = Text("电容器充电时电场变化", font=FONT_CN, color=BRAND["text"], font_size=22)
        info2.next_to(new_title, DOWN, buff=0.5)
        self.play(Write(info2), run_time=DUR["normal"])

        # 电容器
        plate_left = Line(LEFT*2 + UP*1, LEFT*2 + DOWN*1, stroke_color=BRAND["primary"], stroke_width=4)
        plate_right = Line(LEFT*0.5 + UP*1, LEFT*0.5 + DOWN*1, stroke_color=BRAND["primary"], stroke_width=4)

        # 板间电场
        field_between = VGroup()
        for y in np.linspace(-0.8, 0.8, 5):
            line = Arrow(plate_left.get_center() + 0.2*RIGHT, plate_right.get_center() + 0.2*LEFT,
                        buff=0, stroke_color=BRAND["primary"], stroke_width=2).shift(UP*y)
            field_between.add(line)

        self.play(Create(plate_left), Create(plate_right), run_time=0.4)
        self.play(Create(field_between), run_time=0.5)

        # 产生的磁场
        magnetic_field = VGroup()
        for angle in np.linspace(0, 2*PI, 6, endpoint=False):
            arc = Arc(radius=0.8, angle=PI/3, start_angle=angle, stroke_color=BRAND["secondary"], stroke_width=2).move_to(LEFT*1.25)
            magnetic_field.add(arc)

        info3 = Text("变化的电场\n产生磁场！", font=FONT_CN, color=BRAND["secondary"], font_size=20)
        info3.to_edge(RIGHT, buff=0.8).shift(UP*0.5)
        self.play(Create(magnetic_field), Write(info3), run_time=0.8)
        self.wait(DUR["pause"])

        # 变化的磁场产生电场
        self.play(*[FadeOut(m) for m in [info2, plate_left, plate_right, field_between, magnetic_field, info3]], run_time=DUR["fast"])
        new_title2 = self.add_title("变化的磁场 → 电场")

        info4 = Text("磁铁移动时磁场变化", font=FONT_CN, color=BRAND["text"], font_size=22)
        info4.next_to(new_title2, DOWN, buff=0.5)
        self.play(Write(info4), run_time=DUR["normal"])

        # 线圈和磁铁
        coil = ParametricFunction(lambda t: np.array([np.cos(t), np.sin(t), 0]) * 1.0 + RIGHT*2,
                                 t_range=[0, 2*PI, 0.1], stroke_color=BRAND["accent"], stroke_width=2)
        magnet = Rectangle(width=0.4, height=1.5, fill_color=RED, fill_opacity=0.6, stroke_width=0).move_to(LEFT*2)

        self.play(Create(coil), FadeIn(magnet), run_time=0.5)
        self.play(magnet.animate.shift(RIGHT*1), run_time=1.0, rate_func=linear)

        # 感应电场
        induced_field = VGroup()
        for angle in np.linspace(0, 2*PI, 8, endpoint=False):
            arc = Arc(radius=0.6, angle=PI/4, start_angle=angle, stroke_color=BRAND["primary"], stroke_width=2).move_to(RIGHT*2)
            induced_field.add(arc)

        info5 = Text("变化的磁场\n产生电场！", font=FONT_CN, color=BRAND["primary"], font_size=20)
        info5.to_edge(RIGHT, buff=0.8).shift(UP*0.5)
        self.play(Create(induced_field), Write(info5), run_time=0.8)
        self.wait(DUR["pause"])

        # 电磁波
        self.play(*[FadeOut(m) for m in [info4, coil, magnet, induced_field, info5]], run_time=DUR["fast"])
        final_title = self.add_title("电磁波由此诞生！")

        # 电磁波图示
        axes_wave = Axes(x_range=[0, 4*PI, PI], y_range=[-1.5, 1.5, 1], x_length=10, y_length=3,
                         axis_config={"color": BRAND["grid"], "stroke_width": 1}, tips=False).shift(DOWN*0.8)

        e_wave = axes_wave.plot(lambda x: np.sin(x), color=BRAND["primary"], stroke_width=2.5)
        e_label = Text("E", font=FONT_CN, color=BRAND["primary"], font_size=20)
        e_label.next_to(e_wave, LEFT, buff=0.3)

        b_wave = axes_wave.plot(lambda x: np.sin(x + PI/2), color=BRAND["secondary"], stroke_width=2.5)
        b_label = Text("B", font=FONT_CN, color=BRAND["secondary"], font_size=20)
        b_label.next_to(b_wave, RIGHT, buff=0.3)

        self.play(Create(axes_wave), run_time=0.4)
        self.play(Create(e_wave), Write(e_label), run_time=0.6)
        self.play(Create(b_wave), Write(b_label), run_time=0.6)
        self.wait(DUR["pause"] * 1.5)

        # 公式
        self.play(*[FadeOut(m) for m in [final_title, axes_wave, e_wave, b_wave, e_label, b_label]], run_time=DUR["fast"])
        formula_title = self.add_title("麦克斯韦方程组")

        formula = MathTex(
            r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
            r"\nabla \times \mathbf{B} = \mu_0\mathbf{J} + \mu_0\epsilon_0\frac{\partial \mathbf{E}}{\partial t}",
            font_size=26, color=BRAND["text"]
        ).arrange(DOWN, buff=0.5).shift(UP*0.3)

        self.play(Write(formula), run_time=DUR["slow"] * 1.5)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.play(*[FadeOut(m) for m in [formula_title, formula]], run_time=DUR["fast"])
        end = Text("下期：引力波的涟漪", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
