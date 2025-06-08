from manim import *
from typing import Optional, Callable, Any
from enum import IntEnum
from functools import wraps

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
  def __init__(self):
    self._scenes = []
  
  def add_scenes(self, scene_name: Optional[str] = None):
    def add_scenes_func(func: Callable):
      @wraps(func)
      def wrap():
        self._scenes.append((scene_name or func.__name__, func))
      return wrap()
    return add_scenes_func
  
  @property
  def output_scene(self):
    return type(
        "OutputScene",
        (self.OutputScene,),
        {
            "scene_setter": self
        }
    )
  
  class OutputScene(SceneSetup):
    def construct(self):
      for scene in self.scene_setter._scenes:
        scene[1](self)
        self.wait()

scene_setter = SceneSetter()

@scene_setter.add_scenes("begin")
def scene1(scene: Scene):
  title = Text("Python 程式設計技巧", font_size=Size.h1).shift(UP*1.4)
  subtitle = Text("ACM 輸入處理", font_size=Size.h2).next_to(title, DOWN, buff=0.5)
  author = Text("CXPh03n1x | 陳晉 @ FHSH").next_to(subtitle, DOWN*2.5)
  begin_group = VGroup(title, subtitle, author)
  
  scene.add_sound("audios/begin.wav")
  scene.play(Write(title))
  scene.play(FadeIn(subtitle, shift=UP))
  scene.play(FadeIn(author))
  scene.wait(10)
  
  scene.play(FadeOut(begin_group))
  scene.remove(begin_group)

@scene_setter.add_scenes("intro")
def scene2(scene: Scene):
  t1 = Text("輸入兩個整數")
  t2 = MathTex(f"a, b\ (1 \le a, b \le 100)").next_to(t1, RIGHT)

  line1 = VGroup(t1, t2).shift(LEFT*3)

  scene.wait(1)
  logger.info("加入 audios/intro.wav")
  scene.add_sound("audios/intro.wav")
  scene.wait(6) # 等剛好唸到
  scene.play(Write(line1))
  scene.wait(4)

  scene.remove(line1)

  img1 = ImageMobject('images/scene1-1.png')
  scene.add(img1)

OutputScene = scene_setter.output_scene