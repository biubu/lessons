from base_scene import *

class ForceDecompositionScene(BaseScene):
    def construct(self):
        # 1. [0-3s] 钩子标题
        title = self.add_title("斜面上的物体为何会下滑？")

        # 2. [3-8s] 斜面与滑块
        ramp = Polygon(LEFT*5, RIGHT*3, LEFT*5 + DOWN*3, 
                       fill_color=BRAND["grid"], fill_opacity=0.4, stroke_color=WHITE, stroke_width=1)
        ramp.rotate(-0.45, about_point=LEFT*5)  # 约26度角
        
        block = Square(0.7, fill_color=BRAND["primary"], fill_opacity=0.9, stroke_width=0)
        block.move_to(ramp.get_center() + UP*0.4)
        block.rotate(-0.45)
        
        self.play(Create(ramp), run_time=0.4)
        self.play(DrawBorderThenFill(block), run_time=0.4)
        self.wait(DUR["pause"]*0.5)

        # 3. [8-15s] 重力 G 与分解辅助线
        g_arrow = Arrow(block.get_center(), block.get_center() + DOWN*2.2, buff=0, color=RED, stroke_width=4)
        g_label = Text("G", font=FONT_CN, color=RED, font_size=30).next_to(g_arrow, DOWN, buff=0.1)
        
        # 虚线平行四边形
        dash_parallel = DashedLine(g_arrow.get_start(), g_arrow.get_start() + LEFT*2.2 + DOWN*0.9, color=GRAY, stroke_width=2)
        dash_perp = DashedLine(g_arrow.get_start(), g_arrow.get_start() + DOWN*0.9 + RIGHT*0.8, color=GRAY, stroke_width=2)
        
        self.play(GrowArrow(g_arrow), FadeIn(g_label), run_time=0.5)
        self.play(Create(dash_parallel), Create(dash_perp), run_time=0.5)
        self.wait(DUR["pause"]*0.5)

        # 4. [15-22s] 分力箭头浮现
        gx = Arrow(block.get_center(), block.get_center() + LEFT*2.2 + DOWN*0.9, buff=0, color=BRAND["primary"], stroke_width=3)
        gy = Arrow(block.get_center(), block.get_center() + DOWN*0.9 + RIGHT*0.8, buff=0, color=BRAND["accent"], stroke_width=3)
        
        self.play(Create(gx), Create(gy), run_time=0.6)
        self.wait(DUR["pause"]*0.3)

        # 5. [22-27s] 公式卡片
        formula = MathTex(r"G_{\parallel} = mg\sin\theta", r"G_{\perp} = mg\cos\theta", font_size=32, color=BRAND["text"])
        formula.arrange(DOWN, buff=0.35).to_edge(DOWN, buff=1.8)
        self.play(Write(formula), run_time=DUR["slow"])
        self.wait(DUR["pause"]*0.5)

        # 6. [27-30s] 结尾引导
        self.quick_clear(title, dash_parallel, dash_perp, gx, gy, formula, duration=DUR["fast"])
        end = Text("点赞收藏，下期讲：临界角与摩擦力", font=FONT_CN, font_size=28, color=BRAND["text"])
        end.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(end), run_time=DUR["normal"])
        self.wait(0.5)