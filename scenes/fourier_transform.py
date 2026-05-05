import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class FourierTransformScene(BaseScene):
    def construct(self):
        # 标题
        title = self.add_title("傅里叶变换：任意波形都能拆成正弦波")

        # 目标波形：方波
        axes = Axes(
            x_range=[0, 4*PI, PI/2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=4,
            axis_config={"color": BRAND["grid"], "stroke_width": 1},
            tips=False,
        ).shift(DOWN*0.5)

        # 方波函数
        def square_wave(x, n_terms=5):
            result = 0
            for k in range(1, n_terms*2, 2):
                result += (4/(PI*k)) * np.sin(k*x)
            return result

        # 绘制目标方波
        target_wave = axes.plot(
            lambda x: square_wave(x, 50),
            color=BRAND["secondary"],
            stroke_width=3,
        )
        target_label = Text("目标：方波", font=FONT_CN, color=BRAND["secondary"], font_size=24)
        target_label.next_to(axes, UP, buff=0.3).shift(LEFT*4)

        self.play(Create(axes), run_time=0.5)
        self.play(Create(target_wave), FadeIn(target_label), run_time=1.0)
        self.wait(DUR["pause"])

        # 清除，进入分解阶段
        self.play(*[FadeOut(m) for m in [title, axes, target_wave, target_label]], run_time=DUR["fast"])

        # --- 展示傅里叶级数分解 ---
        new_title = Text("任意周期函数 = 正弦波之和", font=FONT_CN, color=BRAND["text"], font_size=34)
        new_title.to_edge(UP, buff=1.2)
        self.play(Write(new_title), run_time=DUR["normal"])

        # 创建坐标系
        axes2 = Axes(
            x_range=[0, 2*PI, PI/2], y_range=[-1.5, 1.5, 0.5],
            x_length=8, y_length=3.5,
            axis_config={"color": BRAND["grid"], "stroke_width": 1},
            tips=False,
        ).shift(DOWN*0.8)

        self.play(Create(axes2), run_time=0.4)

        # 逐步添加正弦波分量
        colors = [BRAND["primary"], BRAND["accent"], "#FF6B6B", "#95E1D3", "#F38181"]

        # 前5个奇次谐波
        for i, k in enumerate(range(1, 11, 2)):
            if i >= 5:
                break
            # 当前项的波形
            def make_wave(x, n=k):
                return (4/(PI*n)) * np.sin(n*x)

            wave = axes2.plot(make_wave, color=colors[i], stroke_width=2.5)

            # 标注
            label = Text(f"sin({k}x)", font=FONT_CN, color=colors[i], font_size=18)
            label.to_edge(RIGHT, buff=1.5).shift(DOWN*(1.5 - i*0.5))

            self.play(Create(wave), Write(label), run_time=0.5)
            self.wait(0.2)

            # 保留在屏幕上
            self.add(wave, label)
            self.wait(0.2)

        self.wait(DUR["pause"])

        # 清除
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=DUR["fast"])

        # --- 合成效果 ---
        final_title = Text("合成后的波形", font=FONT_CN, color=BRAND["text"], font_size=34)
        final_title.to_edge(UP, buff=1.2)
        self.play(Write(final_title), run_time=DUR["normal"])

        axes3 = Axes(
            x_range=[0, 4*PI, PI/2], y_range=[-1.5, 1.5, 0.5],
            x_length=10, y_length=4,
            axis_config={"color": BRAND["grid"], "stroke_width": 1},
            tips=False,
        ).shift(DOWN*0.5)

        self.play(Create(axes3), run_time=0.4)

        # 用3项合成
        wave_3 = axes3.plot(lambda x: square_wave(x, 3), color=BRAND["primary"], stroke_width=2.5)
        label_3 = Text("3项", font=FONT_CN, color=BRAND["primary"], font_size=20)
        label_3.to_edge(UP, buff=2.0).shift(LEFT*3)

        self.play(Create(wave_3), FadeIn(label_3), run_time=0.8)
        self.wait(0.3)

        # 用10项合成
        wave_10 = axes3.plot(lambda x: square_wave(x, 10), color=BRAND["accent"], stroke_width=2.5)
        label_10 = Text("10项", font=FONT_CN, color=BRAND["accent"], font_size=20)
        label_10.to_edge(UP, buff=2.0)

        self.play(Create(wave_10), FadeIn(label_10), run_time=0.8)
        self.wait(0.3)

        # 目标方波
        wave_target = axes3.plot(lambda x: square_wave(x, 50), color=BRAND["secondary"], stroke_width=3)
        label_target = Text("无限项 → 方波", font=FONT_CN, color=BRAND["secondary"], font_size=20)
        label_target.to_edge(UP, buff=2.0).shift(RIGHT*3)

        self.play(Create(wave_target), FadeIn(label_target), run_time=0.8)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=DUR["fast"])
        end = Text("下期：量子力学双缝实验", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
