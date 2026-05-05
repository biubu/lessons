# 待实现课题列表

> 基于 Manim 的炫酷物理/数学动画课题，按优先级排序

---

## 🔴 高优先级（视觉效果极佳）

### 物理类

- [ ] **量子隧穿** - 经典粒子撞墙反弹 vs 量子粒子概率穿透，波函数指数衰减动画
  - 文件: `scenes/quantum_tunneling.py`
  - 关键效果: 势垒穿透、波函数叠加、透射/反射概率对比

- [ ] **麦克斯韦方程组** - 动态电场/磁场线互生，电磁波从振荡中诞生并向外传播
  - 文件: `scenes/maxwell_equations.py`
  - 关键效果: 右手定则动画、电磁波3D传播、法拉第电磁感应

- [ ] **引力波** - 两个黑洞螺旋合并，时空网格像水面涟漪一样荡漾开来
  - 文件: `scenes/gravitational_waves.py`
  - 关键效果: 时空网格形变、螺旋轨道衰减、涟漪向外传播

- [ ] **狭义相对论** - 光速飞船上的钟变慢、尺缩效应，双生子佯谬的时间对比动画
  - 文件: `scenes/special_relativity.py`
  - 关键效果: 洛伦兹变换可视化、时空图、世界线对比

### 数学类

- [ ] **欧拉公式** - e^iπ+1=0，复平面上单位圆旋转，五个常数神奇相遇
  - 文件: `scenes/euler_formula.py`
  - 关键效果: 复平面旋转、指数与三角函数联系、公式推导动画

- [ ] **曼德博分形** - 无限缩放，色彩斑斓的 fractal 花火，每一层都有新细节
  - 文件: `scenes/mandelbrot.py`
  - 关键效果: 实时缩放、色彩映射、Julia 集对比

- [ ] **莫比乌斯带** - 蚂蚁在单侧曲面上无限爬行，剪刀剪开瞬间拓扑变换
  - 文件: `scenes/mobius_strip.py`
  - 关键效果: 3D曲面构建、蚂蚁路径动画、剪开拓扑变换

### 化学类

- [ ] **分子轨道** - 原子轨道叠加成 σ/π 键，电子云密度实时渲染
  - 文件: `scenes/molecular_orbitals.py`
  - 关键效果: 轨道混合、电子云密度、键级可视化

- [ ] **B-Z 化学振荡** - 溶液颜色周期性红蓝变换，化学时钟的视觉冲击
  - 文件: `scenes/bz_oscillation.py`
  - 关键效果: 颜色渐变、波传播、非线性动力学

---

## 🟡 中优先级

- [ ] **梯度下降** - 3D 损失景观，小球在鞍点/局部最优间的挣扎滚落
  - 文件: `scenes/gradient_descent.py`
  - 关键效果: 3D曲面、优化路径、动量/Adam对比

---

## ✅ 已完成

- [x] **傅里叶变换** - 旋转圆叠加（epicycles）生成任意波形
  - 文件: `scenes/fourier_transform.py`

- [x] **双缝实验** - 单粒子逐个打屏，干涉条纹浮现，观测导致坍缩
  - 文件: `scenes/double_slit.py`

- [x] **洛伦兹吸引子** - 混沌蝴蝶轨迹，初始值微小差异导致天壤之别
  - 文件: `scenes/lorenz_attractor.py`

---

## 使用说明

每个场景继承 `BaseScene`，使用统一的品牌色和动画时长：

```python
from base_scene import *

class NewScene(BaseScene):
    def construct(self):
        title = self.add_title("标题")
        # ... 实现动画
        self.wait(0.5)
```

渲染单个场景：
```bash
uv run manim -qh -c config/manim.cfg scenes/new_scene.py NewScene
```
