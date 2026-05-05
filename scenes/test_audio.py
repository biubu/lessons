import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from manim import *
from base_scene import *

class TestAudioScene(BaseScene):
    def construct(self):
        # 测试字幕和音频
        self.show_subtitle(
            "这是一段测试音频和字幕",
            audio_path="assets/audio/gravitational_waves_0_3a7b.json.mp3"
        )

        # 测试 explain_step
        self.explain_step(
            "测试标题",
            "这是说明文字，会自动生成音频",
        )
