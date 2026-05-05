import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class SpecialRelativityScene(BaseScene):
    def construct(self):
        # ========== 第一部分：经典速度叠加 ==========
        title = self.add_title("狭义相对论：光速不变")

        # 说明文字（标题正下方）
        info1 = Text("经典物理：速度直接相加", font=FONT_CN, color=BRAND["text"], font_size=24)
        info1.next_to(title, DOWN, buff=0.4)
        self.play(Write(info1), run_time=DUR["normal"])
        self.auto_place(title, info1, padding=0.2)

        # 地面（底部区域）
        ground = Line(LEFT*6, RIGHT*6, stroke_color=GRAY, stroke_width=2)
        ground.shift(DOWN*2.8)

        # 火车（中下方）
        train = Rectangle(width=2.5, height=1, fill_color=BRAND["primary"], fill_opacity=0.6, stroke_width=0)
        train.move_to(DOWN*1.8)
        train_label = Text("火车 10m/s", font=FONT_CN, color=BRAND["primary"], font_size=18)
        train_label.next_to(train, UP, buff=0.15)

        # 人（在火车上）
        person = Dot(train.get_center() + UP*0.8, color=BRAND["accent"], radius=0.1)
        person_label = Text("人 2m/s", font=FONT_CN, color=BRAND["accent"], font_size=18)
        person_label.next_to(person, UP, buff=0.15)

        # 结果（左下角，自动避撞）
        result_classic = Text("相对速度 = 12m/s", font=FONT_CN, color=BRAND["secondary"], font_size=20)

        self.play(Create(ground), run_time=0.3)
        self.play(FadeIn(train), Write(train_label), run_time=0.4)
        self.play(FadeIn(person), Write(person_label), run_time=0.4)
        self.wait(0.3)
        self.play(Write(result_classic), run_time=0.5)
        # 自动调整结果文字位置
        self.auto_place(title, info1, ground, train, train_label, person, person_label, result_classic, padding=0.2)
        self.wait(DUR["pause"])

        # 清除
        self.quick_clear(title, info1, ground, train, train_label, person, person_label, result_classic)

        # ========== 第二部分：光速不变 ==========
        new_title = self.add_title("但光速对任何观察者都不变！")

        # 说明（标题下方，自动避撞）
        info2 = Text("光速是宇宙速度极限", font=FONT_CN, color=BRAND["text"], font_size=22)
        info2.next_to(new_title, DOWN, buff=0.4)
        self.play(Write(info2), run_time=DUR["normal"])
        self.auto_place(new_title, info2, padding=0.2)

        # 火车（左侧中间）
        light_train = Rectangle(width=2, height=1, fill_color=BRAND["primary"], fill_opacity=0.4, stroke_width=1)
        light_train.move_to(LEFT*3 + DOWN*0.3)
        light_label = Text("火车 (v=0.5c)", font=FONT_CN, color=BRAND["primary"], font_size=18)
        light_label.next_to(light_train, DOWN, buff=0.2)

        flash_train = Dot(light_train.get_center(), color=YELLOW, radius=0.15)

        self.play(FadeIn(light_train), Write(light_label), FadeIn(flash_train), run_time=0.5)

        # 光向两个方向传播
        light_right = Arrow(light_train.get_center(), RIGHT*5 + DOWN*0.3, buff=0, stroke_color=YELLOW, stroke_width=3)
        light_left = Arrow(light_train.get_center(), LEFT*5 + DOWN*0.3, buff=0, stroke_color=YELLOW, stroke_width=3)

        self.play(GrowArrow(light_right), GrowArrow(light_left), run_time=0.8)
        self.wait(0.3)

        # 地面观察者（右侧）
        ground_obs = Text("地面观察者：\n光速仍是 c！", font=FONT_CN, color=BRAND["accent"], font_size=20)
        ground_obs.to_corner(DR, buff=0.8)

        # 公式（正下方）
        formula = MathTex(
            r"c = \frac{c + v}{1 + \frac{cv}{c^2}} = c",
            font_size=24,
            color=BRAND["text"]
        ).shift(DOWN*1.5)

        self.play(Write(ground_obs), run_time=0.5)
        self.play(Write(formula), run_time=DUR["slow"])
        # 自动调整位置
        self.auto_place(new_title, info2, light_train, light_label, flash_train, light_right, light_left, ground_obs, formula, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 清除
        self.quick_clear(new_title, info2, light_train, light_label, flash_train, light_right, light_left, ground_obs, formula)

        # ========== 第三部分：时间膨胀 ==========
        time_title = self.add_title("时间膨胀：运动的钟变慢")

        # 说明
        info3 = Text("高速运动的时间流逝更慢", font=FONT_CN, color=BRAND["text"], font_size=22)
        info3.next_to(time_title, DOWN, buff=0.4)
        self.play(Write(info3), run_time=DUR["normal"])
        self.auto_place(time_title, info3, padding=0.2)

        # 左侧：地球
        earth = Dot(LEFT*3.5 + DOWN*0.5, color=BLUE, radius=0.2)
        earth_label = Text("地球", font=FONT_CN, color=BLUE, font_size=20)
        earth_label.next_to(earth, DOWN, buff=0.3)

        # 右侧：飞船
        spaceship = Dot(RIGHT*3.5 + DOWN*0.5, color=BRAND["accent"], radius=0.15)
        ship_label = Text("飞船 (高速)", font=FONT_CN, color=BRAND["accent"], font_size=20)
        ship_label.next_to(spaceship, DOWN, buff=0.3)

        # 时间对比（在物体上方）
        earth_time = Text("10年", font=FONT_CN, color=BLUE, font_size=22)
        earth_time.next_to(earth, UP, buff=0.4)

        ship_time = Text("5年", font=FONT_CN, color=BRAND["accent"], font_size=22)
        ship_time.next_to(spaceship, UP, buff=0.4)

        # 连接线
        compare_line = DashedLine(earth, spaceship, stroke_color=GRAY, stroke_width=1)

        self.play(FadeIn(earth), Write(earth_label), run_time=0.3)
        self.play(FadeIn(spaceship), Write(ship_label), run_time=0.3)
        self.play(Create(compare_line), run_time=0.4)
        self.wait(0.3)
        self.play(Write(earth_time), Write(ship_time), run_time=0.6)
        # 自动调整位置
        self.auto_place(time_title, info3, earth, earth_label, spaceship, ship_label, earth_time, ship_time, compare_line, padding=0.2)
        self.wait(DUR["pause"])

        # 清除
        self.quick_clear(time_title, info3, earth, earth_label, spaceship, ship_label, earth_time, ship_time, compare_line)

        # ========== 第四部分：洛伦兹因子 ==========
        formula_title = self.add_title("洛伦兹因子")

        # 公式（居中）
        lorentz = MathTex(
            r"\gamma = \frac{1}{\sqrt{1-\frac{v^2}{c^2}}}",
            font_size=36,
            color=BRAND["primary"]
        )

        # 解释（公式下方）
        explanation = Text(
            "速度越接近光速\n时间越慢、长度越短",
            font=FONT_CN, color=BRAND["secondary"], font_size=22,
            line_spacing=1.5
        ).next_to(lorentz, DOWN, buff=0.8)

        self.play(Write(lorentz), run_time=DUR["slow"])
        self.wait(0.3)
        self.play(FadeIn(explanation), run_time=DUR["normal"])
        # 自动调整位置
        self.auto_place(formula_title, lorentz, explanation, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.quick_clear(formula_title, lorentz, explanation)
        end = Text("相对论改变我们对时空的认知", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
