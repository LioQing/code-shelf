from typing import Iterable
from manim import *

class LinkedList(VGroup):
    def __init__(
        self,
        data: Iterable[str],
        element_to_mobject: Callable = Paragraph,
        element_to_mobject_config: dict = {},
        buff: float = 6,
        circle_buffer_factor: float = 2,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.data = data
        self.element_to_mobject = element_to_mobject
        self.element_to_mobject_config = element_to_mobject_config
        self.buff = buff
        self.circle_buffer_factor = circle_buffer_factor
        self.nodes = VGroup()
        self.circles = VGroup()
        self.arrows = VGroup()
        self.setup()
    
    def setup(self):
        # nodes
        self.nodes = VGroup()
        self.circles = VGroup()
        for i, data in enumerate(self.data):
            node: VMobject = self.element_to_mobject(data, **self.element_to_mobject_config)
            if i > 0:
                node.next_to(self.nodes[i - 1], RIGHT * self.buff)
            self.nodes.add(node)

            circle = Circle(
                radius=node.get_height(),
                stroke_color=WHITE,
                fill_color=BLACK,
                fill_opacity=1,
            )
            circle.surround(node, buffer_factor=self.circle_buffer_factor)
            self.circles.add(circle)
        self.add(self.circles, self.nodes)
        
        # arrows
        self.arrows = VGroup()
        for i in range(len(self.nodes) - 1):
            arrow = Arrow(
                self.circles[i].get_right(),
                self.circles[i + 1].get_left(),
                buff=0,
            )
            self.arrows.add(arrow)
        self.add(self.arrows)

        # origin to center
        self.center()