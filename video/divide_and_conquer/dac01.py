import manim

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


class dac_01_01(manim.Scene):
    WIDTH: int = 3

    def construct(self):
        circle = manim.Circle(
            radius=2.5,
            color=manim.RED,
            fill_opacity=1,
        )

        self.play(manim.FadeIn(circle))

        # Divide
        for layer in self.split_circle(circle, 3, self.WIDTH):
            self.play(manim.Transform(circle, manim.VGroup(*layer)))

        # Solve
        circles = circle
        anim_group = []
        for circle in circles:
            anim_group.append(manim.FadeToColor(circle, color=manim.GREEN))

        self.play(*anim_group, run_time=2, lag_ratio=0.25)

        # Combine
        for layer in self.combine_circles(circles):
            self.play(manim.Transform(circles, manim.VGroup(*layer)))

        self.wait(2)

        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])

    def split_circle(
        self, circle: manim.VMobject, n: int, width: float
    ) -> list[list[manim.VMobject]]:
        """
        Split a circle into 2 parts for n times recursively.

        Arguments:
            circle: The circle to split.
            n: The number of times to split the circle.

        Returns:
            A list of list of circles, each list of circles is a layer of circle.
        """
        if n == 0:
            return []

        # Split the circle into 2 circles
        circle1 = circle.copy()
        circle2 = circle.copy()

        circle1.move_to(circle.get_center() + width * manim.LEFT)
        circle2.move_to(circle.get_center() + width * manim.RIGHT)

        circle1.scale(0.5)
        circle2.scale(0.5)

        circle_group = [[circle1, circle2]]

        # Recursively split the circles
        next_circle_group = self.split_circle(circle1, n - 1, width / 2)
        for i, layer in enumerate(
            self.split_circle(circle2, n - 1, width / 2)
        ):
            next_circle_group[i].extend(layer)

        circle_group.extend(next_circle_group)

        return circle_group

    def combine_circles(
        self, circles: list[manim.VMobject]
    ) -> list[list[manim.VMobject]]:
        """
        Combine every 2 circles until there is only 1 circle left.

        Arguments:
            circles: The circles to combine.

        Returns:
            A list of list of circles, eahc list of circles is a layer.
        """
        if len(circles) == 1:
            return []

        circle_group = []
        for i in range(0, len(circles), 2):
            circle1 = circles[i]
            circle2 = circles[i + 1]

            circle = circle1.copy()
            circle.move_to((circle1.get_center() + circle2.get_center()) / 2)
            circle.scale(2)

            circle_group.append(circle)

        next_circle_group = self.combine_circles(circle_group)
        circle_group = [circle_group]
        circle_group.extend(next_circle_group)

        return circle_group
