from manim import *
from manim_data_structures import *
from typing import Optional, Callable, Any
from enum import IntEnum
from functools import wraps
import os
from pathlib import Path
import re

import logging

LOGGING_CONFIG: dict[str, Any] = {
    "formatters": {
        "default": {
            "fmt": "%(message)s",
        },
    },
    "handlers": {
        "access": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "manim": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}

logger = logging.getLogger("manim")


class Size(IntEnum):
    h1 = 52
    h2 = 40
    h3 = 32
    p = 28


class SceneSetup(Scene):
    def setup(self):
        Text.set_default(font="Noto Sans CJK TC", font_size=Size.p)


class SceneSetter:
    def __init__(self, sound_track_path: Optional[os.PathLike | str] = None):
        self._scenes = []
        self._sound_track_path = sound_track_path

    def add_scenes(self, scene_name: Optional[str] = None):
        def add_scenes_func(func: Callable):
            @wraps(func)
            def wrap():
                self._scenes.append((scene_name or func.__name__, func))

            return wrap()

        return add_scenes_func

    def get_target_code_strings(
        self,
        code_obj: Code,
        code_srcs: list[str] | str,
        re_string: str,
        added_line_number: bool = True,
    ) -> Code:
        code_lines_paragraph_index = 2
        if not added_line_number:
            code_lines_paragraph_index -= 1
        if isinstance(code_srcs, str):
            code_srcs = code_srcs.split("\n")
        for idx in range(len(code_obj[code_lines_paragraph_index])):
            matching = re.search(re_string, code_srcs[idx])
            if matching:
                return code_obj[code_lines_paragraph_index][idx][
                    matching.span()[0] : matching.span()[1]
                ]
        return code_obj[code_lines_paragraph_index]  # 表示沒有找到

    @property
    def output_scene(self):
        return type("OutputScene", (self.OutputScene,), {"scene_setter": self})

    class OutputScene(SceneSetup):
        def construct(self):
            self.add_sound(self.scene_setter._sound_track_path)
            for scene in self.scene_setter._scenes:
                self.next_section(scene[0])
                scene[1](self)
                self.wait()


scene_setter = SceneSetter(Path("audio/all-v1.wav"))


@scene_setter.add_scenes("begin")
def begin(scene: Scene):
    title = Text("Python 程式設計技巧", font_size=Size.h1).shift(UP * 1.4)
    subtitle = Text("ACM 輸入處理", font_size=Size.h2).next_to(title, DOWN, buff=0.5)
    author = Text("CXPh03n1x | 陳晉 @ FHSH").next_to(subtitle, DOWN * 2.5)
    begin_group = VGroup(title, subtitle, author)

    scene.play(Write(title))
    scene.play(FadeIn(subtitle, shift=UP))
    scene.play(FadeIn(author))
    scene.wait(13)

    scene.play(FadeOut(begin_group))
    scene.remove(begin_group)


@scene_setter.add_scenes("question description")
def question_desc(scene: Scene):
    t1 = Text("輸入兩個整數")
    t2 = MathTex(f"a, b\ (1 \le a, b \le 100)").next_to(t1, RIGHT)

    line1 = VGroup(t1, t2).shift(LEFT * 3)

    scene.wait(7)  # 等剛好唸到
    scene.play(Write(line1))
    scene.wait(9)
    scene.remove(line1)
    img_panic = ImageMobject("images/meme-panic.png")
    scene.add(img_panic)
    scene.wait(6)
    scene.remove(img_panic)
    scene.wait(1)


@scene_setter.add_scenes("basic flow")
def basic_flow(scene: Scene):
    flow = Paragraph(
      "1. 將資料讀入程式中",
      "2. 以空格為指定切分點，將資料變成串列"
    )
    scene.wait(6)
    scene.play(Write(flow, run_time=10))
    scene.wait(4)

    code = """
your_input = input()
input_split_list = input().split()
  """.strip()

    code_string = Code(code_string=code, language="python", background="window")
    scene.play(ReplacementTransform(flow, code_string))

    box1 = SurroundingRectangle(
        scene_setter.get_target_code_strings(
            code_string, code.split("\n"), r".split\(\)"
        )
    )

    scene.wait(1)
    scene.play(Create(box1))
    scene.wait(2)
    scene.remove(code_string, box1)


OutputScene = scene_setter.output_scene
