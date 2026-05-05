import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
from manim import *
from base_scene import *

class LorenzAttractorScene(BaseScene):
    def construct(self):
        # 标题
        title = self.add_title("洛伦兹吸引子：蝴蝶效应")

        # 洛伦兹方程参数
        sigma = 10.0
        rho = 28.0
        beta = 8.0/3.0
        dt = 0.005
        steps = 2000

        # 数值积分函数
        def lorenz_deriv(x, y, z):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return dx, dy, dz

        # 生成轨迹1：初始点 (0.1, 0, 0)
        def generate_trajectory(x0, y0, z0):
            points = [(x0, y0, z0)]
            x, y, z = x0, y0, z0
            for _ in range(steps):
                dx, dy, dz = lorenz_deriv(x, y, z)
                x += dx * dt
                y += dy * dt
                z += dz * dt
                points.append((x, y, z))
            return points

        # 轨迹1
        traj1 = generate_trajectory(0.1, 0.0, 0.0)
        # 轨迹2：微小差异 (0.1001, 0, 0)
        traj2 = generate_trajectory(0.1001, 0.0, 0.0)

        # 转换为2D投影（透视投影，从斜上方看）
        def project_3d_to_2d(points_3d, scale=0.15, center=ORIGIN):
            # 简单的正交投影 + 斜向视角
            result = []
            for x, y, z in points_3d:
                # 调整坐标，使轨迹在屏幕中央
                px = x * scale - y * scale * 0.5 + center[0]
                py = z * scale + y * scale * 0.3 + center[1]
                result.append([px, py, 0])
            return result

        proj1 = project_3d_to_2d(traj1, scale=0.3, center=DOWN*1)
        proj2 = project_3d_to_2d(traj2, scale=0.3, center=DOWN*1)

        # 创建轨迹曲线1（渐变色：从青色到品红）
        path1 = VMobject()
        path1.set_points_smoothly([np.array(p) for p in proj1])
        path1.set_stroke(width=2.5)

        # 设置渐变色
        colors1 = color_gradient([BRAND["primary"], BRAND["secondary"]], len(proj1))
        path1.set_color_by_gradient(*colors1)

        # 创建轨迹曲线2
        path2 = VMobject()
        path2.set_points_smoothly([np.array(p) for p in proj2])
        path2.set_stroke(width=2.5, opacity=0.6)
        path2.set_color_by_gradient(BRAND["accent"], YELLOW)

        # 显示轨迹
        info1 = Text("初始值仅差 0.0001", font=FONT_CN, color=BRAND["text"], font_size=24)
        info1.next_to(title, DOWN, buff=0.4)
        self.play(Write(info1), run_time=DUR["normal"])
        self.auto_place(title, info1, padding=0.2)

        # 动画：逐段绘制轨迹1
        self.play(Create(path1), run_time=2.5, rate_func=linear)
        self.wait(0.3)

        # 显示轨迹2
        info2 = Text("轨迹却天差地别！", font=FONT_CN, color=BRAND["accent"], font_size=24)
        info2.next_to(info1, DOWN, buff=0.3)
        self.play(ReplacementTransform(info1, info2), run_time=DUR["normal"])
        self.auto_place(title, info2, padding=0.2)

        self.play(Create(path2), run_time=2.5, rate_func=linear)
        self.wait(DUR["pause"] * 1.5)

        # 添加混沌说明
        self.quick_clear(title, path1, path2, duration=DUR["fast"])

        new_title = Text("混沌系统：初始条件的微小差异", font=FONT_CN, color=BRAND["text"], font_size=30)
        new_title.to_edge(UP, buff=1.2)
        self.play(Write(new_title), run_time=DUR["normal"])

        # 重新绘制两条轨迹（缩小版，在上方）
        path1_small = path1.copy().scale(0.4).shift(UP*1.5)
        path2_small = path2.copy().scale(0.4).shift(UP*1.5)
        self.add(path1_small, path2_small)

        # 公式卡片
        formula = MathTex(
            r"\begin{cases} \dot{x} = \sigma(y-x) \\ \dot{y} = x(\rho-z)-y \\ \dot{z} = xy-\beta z \end{cases}",
            font_size=28,
            color=BRAND["text"]
        ).shift(DOWN*0.5)

        chaos_text = Text(
            "天气预报、股价波动、湍流...\n一切混沌系统都有此特性",
            font=FONT_CN, color=BRAND["secondary"], font_size=22
        ).shift(DOWN*2)

        self.play(Write(formula), run_time=DUR["slow"])
        self.wait(0.3)
        self.play(FadeIn(chaos_text), run_time=DUR["normal"])
        # 自动调整位置
        self.auto_place(formula, chaos_text, path1_small, path2_small, padding=0.2)
        self.wait(DUR["pause"] * 1.5)

        # 结尾
        self.quick_clear(new_title, path1_small, path2_small, formula, chaos_text, duration=DUR["fast"])
        end = Text("更多炫酷物理动画，请关注更新", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)
