from __future__ import annotations
import manim

class SizedContainer(manim.VGroup):
    def __init__(
            self,
            width: int,
            height: int,
            mobject: manim.VMobject,
            show_outline: bool = False,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.target_width = width
        self.target_height = height
        self.element = mobject
        self.outline = 1 if show_outline else 0
        self.setup()
    
    def setup(self):
        self.add(self.element)
        self.add(manim.Rectangle(
            width=self.target_width,
            height=self.target_height,
            stroke_width=self.outline,
            stroke_opacity=self.outline,
        ))

        self.center()

    def set_opacity(self, opacity: float):
        self.element.set_opacity(opacity)
        return self
