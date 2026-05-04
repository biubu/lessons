# Lessons

高中数理化 Manim 自媒体动画项目（9:16 竖屏，30fps）。

## 环境要求

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip
- FFmpeg（Manim 渲染视频必需）

## 安装

```bash
uv sync
```

## 使用

```bash
# 批量渲染所有场景
uv run python main.py
# 或
uv run python scripts/batch_render.py

# 单个场景预览渲染
uv run manim -ql -c config/manim.cfg force_decomposition.py ForceDecompositionScene

# 单个场景高质量渲染
uv run manim -qh -c config/manim.cfg force_decomposition.py ForceDecompositionScene
```

## 项目结构

```
├── config/
│   ├── manim.cfg           # 渲染配置（分辨率、帧率、背景色）
│   └── render_queue.json   # 渲染队列（可选，为空则自动扫描 scenes/）
├── scripts/
│   └── batch_render.py     # 批量渲染脚本（含进度条、错误处理、输出归档）
├── scenes/                 # 场景文件目录
├── base_scene.py           # 基础场景类（品牌色、中文字体、常用动画方法）
├── force_decomposition.py  # 示例场景：力的分解
├── main.py                 # 入口脚本（调用 batch_render.py）
├── output/                 # 渲染成品视频（已 gitignore）
└── media/                  # Manim 缓存（已 gitignore）
```

## 自定义

编辑 `base_scene.py`：

| 参数 | 说明 |
|------|------|
| `BRAND` | 全局色板（背景、主色、辅色、文字色等） |
| `DUR` | 动画时长预设（fast/normal/slow/pause） |
| `FONT_CN` | 中文字体，已按 macOS/Windows/Linux 自动检测 |

## 新增场景

1. 在 `scenes/` 下创建 Python 文件，继承 `BaseScene`
2. 运行 `uv run python main.py` 自动扫描并渲染

也可在 `config/render_queue.json` 中手动指定渲染队列。
