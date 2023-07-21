from typing import Sequence
import manim
import numpy as np

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.btree import BTree, BNode
from utils.sized_container import SizedContainer


class dp_04_01(manim.Scene):
    def construct(self):
        # Initialize table from 1 to 5 representing f(1) to f(5)
        table = manim.MathTable(
            [["1", "2", "3", "5", "8"]],
            row_labels=[manim.MathTex(r"\text{dp}")],
            col_labels=[
                SizedContainer(
                    width=1,
                    height=0,
                    mobject=manim.MathTex(f"f({i})"),
                )
                for i in range(1, 6)
            ],
            include_outer_lines=True,
        )

        # Hide all values
        for i in range(2, 7):
            table.get_entries((2, i)).set_opacity(0)

        # Show table
        self.play(manim.Create(table), run_time=2)

        self.wait()

        # Write base cases
        set_table_mobject(table, (2, 2), manim.MathTex("1"))
        set_table_mobject(table, (2, 3), manim.MathTex("2"))
        self.play(
            manim.Write(table.get_entries((2, 2))),
            manim.Write(table.get_entries((2, 3))),
        )
        self.wait()

        # Write arrows and recursive cases
        values = [1, 2]
        for i in range(3, 6):
            # Write curved arrows and indicate the two values being added
            sec_last = table.get_entries((2, i - 1))
            last = table.get_entries((2, i))
            curr = table.get_entries((2, i + 1))
            vbuff = 0.4
            hbuff = 0.4

            def arrow_pos(entry: manim.VMobject, direction: np.ndarray = manim.RIGHT):
                return (
                    entry.get_center()
                    + (entry.get_width() + hbuff) * direction / 2
                    + (entry.get_height() + vbuff) * manim.DOWN / 2
                )

            arrow_1 = manim.CurvedArrow(
                start_point=arrow_pos(sec_last),
                end_point=arrow_pos(curr, manim.LEFT),
                angle=manim.PI / 2,
                stroke_width=4,
            )
            arrow_2 = manim.CurvedArrow(
                start_point=arrow_pos(last),
                end_point=arrow_pos(curr, manim.LEFT),
                angle=manim.PI / 2,
                stroke_width=4,
            )

            self.play(
                manim.AnimationGroup(
                    manim.AnimationGroup(
                        manim.Indicate(sec_last), manim.Indicate(last)
                    ),
                    manim.AnimationGroup(manim.Create(arrow_1), manim.Create(arrow_2)),
                    lag_ratio=0.5,
                    run_time=1.5,
                )
            )

            # Write recursive case
            value = values[i - 3] + values[i - 2]
            values.append(value)
            set_table_mobject(table, (2, i + 1), manim.MathTex(f"{value}"))
            self.play(manim.Write(table.get_entries((2, i + 1))))
            self.wait(0.34)

            # Fade out arrows
            self.play(
                manim.FadeOut(arrow_1),
                manim.FadeOut(arrow_2),
            )

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_04_02(manim.Scene):
    def construct(self):
        # Initialize table
        table = manim.Table(
            [
                ["f(1)", "f(2)", "f(3)"],
                ["1", "2", "3"],
            ],
            col_labels=[
                manim.Tex("prev"),
                manim.Tex("curr"),
                manim.MathTex(r"\text{next} = \text{prev} + \text{curr}"),
            ],
            element_to_mobject=lambda el: SizedContainer(
                width=1,
                height=1,
                mobject=manim.MathTex(el),
            ),
            include_outer_lines=True,
        )

        # Show only f(0) and f(1) values
        vgroup = manim.VGroup()
        vgroup.add(table.get_entries((2, 1)))
        vgroup.add(table.get_entries((2, 2)))
        vgroup.add(table.get_entries((3, 1)))
        vgroup.add(table.get_entries((3, 2)))
        original_position = vgroup.get_center()
        vgroup.move_to(manim.ORIGIN)

        self.play(manim.Write(vgroup))
        self.wait(2)

        # Show col labels
        self.play(vgroup.animate.move_to(original_position))
        self.play(
            manim.AnimationGroup(
                manim.Create(table.get_col_labels()),
                manim.Create(table.get_horizontal_lines()),
                manim.Create(table.get_vertical_lines()),
                lag_ratio=0.5,
                run_time=1.5,
            )
        )
        self.wait(2)

        # Indicate the two values being added and show next value
        positions = [
            [table.get_cell((2, i)).get_center().copy() for i in range(1, 4)],
            [table.get_cell((3, i)).get_center().copy() for i in range(1, 4)],
        ]
        prev = [1, table.get_entries((2, 1)), table.get_entries((3, 1))]
        curr = [2, table.get_entries((2, 2)), table.get_entries((3, 2))]
        next = [prev[0] + curr[0], table.get_entries((2, 3)), table.get_entries((3, 3))]
        for i in range(4, 7):
            # Indicate the two value and show next value
            self.play(
                manim.AnimationGroup(
                    manim.AnimationGroup(
                        manim.Indicate(prev[1]),
                        manim.Indicate(prev[2]),
                        manim.Indicate(curr[1]),
                        manim.Indicate(curr[2]),
                    ),
                    manim.AnimationGroup(
                        manim.Write(next[1]),
                        manim.Write(next[2]),
                    ),
                    lag_ratio=0.5,
                    run_time=1.5,
                )
            )
            self.wait()

            # Move and fade out
            prev[1].generate_target()
            prev[2].generate_target()
            curr[1].generate_target()
            curr[2].generate_target()
            next[1].generate_target()
            next[2].generate_target()

            prev[1].target.shift(manim.LEFT * table.get_cell((2, 1)).get_width())
            prev[2].target.shift(manim.LEFT * table.get_cell((3, 1)).get_width())
            prev[1].target.set_opacity(0)
            prev[2].target.set_opacity(0)
            curr[1].target.move_to(positions[0][0])
            curr[2].target.move_to(positions[1][0])
            next[1].target.move_to(positions[0][1])
            next[2].target.move_to(positions[1][1])

            self.play(
                manim.MoveToTarget(prev[1]),
                manim.MoveToTarget(prev[2]),
                manim.MoveToTarget(curr[1]),
                manim.MoveToTarget(curr[2]),
                manim.MoveToTarget(next[1]),
                manim.MoveToTarget(next[2]),
            )

            # Update values
            prev = curr.copy()
            curr = next.copy()

            # Compute next value
            next[0] = prev[0] + curr[0]

            # Set next
            next[1] = SizedContainer(
                width=1,
                height=1,
                mobject=manim.MathTex(f"f({i})"),
            )
            next[2] = SizedContainer(
                width=1,
                height=1,
                mobject=manim.MathTex(f"{next[0]}"),
            )
            next[1].move_to(positions[0][2])
            next[2].move_to(positions[1][2])

        self.wait(2)

        # Fade out other things except f(4) and its value
        remain = manim.VGroup()
        remain.add(curr[1][0])
        remain.add(curr[2][0])

        target = manim.MathTex(f"f(5)", "=", f"{curr[0]}", font_size=72)
        target.center()

        self.play(
            *[manim.FadeOut(mob) for mob in self.mobjects if mob not in remain],
            manim.Transform(remain, target),
        )

        self.wait(2)

        # Fade out everything
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


def set_table_mobject(table: manim.Table, pos: Sequence[int], mobject: manim.VMobject):
    """
    Set the mobject at the given position in the table.

    Arguments:
        table: the table to set the mobject in
        pos: the position of the mobject in the table, array of shape (2,)
        mobject: the mobject to set
    """
    mobject.move_to(table.get_entries(pos))
    if (
        table.row_labels is not None
        and table.col_labels is not None
        and table.top_left_entry is None
    ):
        index = len(table.mob_table[0]) * (pos[0] - 1) + pos[1] - 2
        table.elements[index] = mobject
    else:
        index = len(table.mob_table[0]) * (pos[0] - 1) + pos[1] - 1
        table.elements[index] = mobject
