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


class dp_05_01(manim.Scene):
    def construct(self):
        # Initialize table from 1 to 8 representing f(1) to f(8)
        table = manim.MathTable(
            [
                ["0", "0", "1", "5", "2", "4", "3", r"\text{end}"],
                ["0", "0", "0", "0", "1", "3", "3", "6"],
                ["0", "0", "1", "5", "3", "7", "6", ""],
            ],
            row_labels=[
                manim.MathTex(r"\text{cost}"),
                manim.MathTex(r"\text{dp}"),
                manim.MathTex(r"\text{cost} + \text{dp}"),
            ],
            element_to_mobject=lambda el: SizedContainer(
                width=0.4,
                height=0.4,
                mobject=manim.MathTex(el),
            ),
            v_buff=0.6,
            h_buff=0.8,
            include_outer_lines=True,
        )

        # Hide all values
        for i in range(2, 4):
            for j in range(2, 10):
                table.get_entries((i, j)).set_opacity(0)

        # Show table
        self.play(manim.Create(get_opaque_vmobjects(table)), run_time=4)

        self.wait()

        # Write base cases
        set_table_mobject(table, (2, 2), manim.MathTex("0"))
        set_table_mobject(table, (2, 3), manim.MathTex("0"))
        self.play(
            manim.Write(table.get_entries((2, 2))),
            manim.Write(table.get_entries((2, 3))),
        )

        set_table_mobject(table, (3, 2), manim.MathTex("0"))
        set_table_mobject(table, (3, 3), manim.MathTex("0"))
        self.play(
            manim.FadeIn(table.get_entries((3, 2)), shift=manim.DOWN),
            manim.FadeIn(table.get_entries((3, 3)), shift=manim.DOWN),
        )

        self.wait()

        def arrow_pos(entry: manim.VMobject, direction: np.ndarray = manim.RIGHT):
            return (
                entry.get_center()
                + (entry.get_width() + hbuff) * direction / 2
                + (entry.get_height() + vbuff) * manim.DOWN / 2
            )

        # Write arrows and recursive cases
        cost = [0, 0, 1, 5, 2, 4, 3]
        values = [0, 0]
        add = [0, 0]
        froms = []
        for i in range(3, 9):
            if i > 3:
                # Show add
                add.append(cost[i - 2] + values[-1])
                set_table_mobject(table, (3, i), manim.MathTex(f"{add[-1]}"))
                self.play(
                    manim.FadeIn(table.get_entries((3, i)), shift=manim.DOWN),
                )

            # Write curved arrows and indicate the two values being compared
            sec_last = table.get_entries((3, i - 1))
            last = table.get_entries((3, i))
            min_add = last if add[-1] <= add[-2] else sec_last
            curr = table.get_entries((2, i + 1))
            vbuff = 0.4
            hbuff = 0.4
            froms.append(-1 if add[-1] <= add[-2] else -2)

            arrow = manim.CurvedArrow(
                start_point=arrow_pos(min_add),
                end_point=arrow_pos(curr, manim.ORIGIN),
                angle=manim.PI / 2,
                stroke_width=4,
            )

            indicate_anim = manim.AnimationGroup(
                manim.Indicate(
                    sec_last, color=manim.GREEN if min_add == sec_last else manim.RED
                ),
                manim.Indicate(
                    last, color=manim.GREEN if min_add == last else manim.RED
                ),
            )

            if add[-1] == add[-2]:
                indicate_anim = manim.AnimationGroup(
                    manim.Indicate(sec_last), manim.Indicate(last)
                )

            self.play(
                manim.AnimationGroup(
                    indicate_anim,
                    manim.AnimationGroup(manim.Create(arrow)),
                    lag_ratio=0.5,
                    run_time=1.5,
                )
            )

            # Write recursive case
            value = min(add[-1], add[-2])
            values.append(value)
            set_table_mobject(table, (2, i + 1), manim.MathTex(f"{value}"))
            self.play(manim.Write(table.get_entries((2, i + 1))))
            self.wait(0.34)

            # Fade out arrows
            self.play(manim.FadeOut(arrow))

        self.wait()

        # Trace back arrow
        gen = reversed(list(enumerate(froms)))
        i = len(froms) - 1
        while i > 0:
            try:
                i, f = next(gen)
                arrow = manim.CurvedArrow(
                    start_point=arrow_pos(
                        table.get_entries((2, 4 + i + f)), manim.RIGHT * 0.5
                    ),
                    end_point=arrow_pos(
                        table.get_entries((2, 4 + i)), manim.LEFT * 0.5
                    ),
                    angle=manim.PI / 2,
                    stroke_width=4,
                )
                if f == -2:
                    next(gen)
            except StopIteration:
                break
            self.play(manim.Create(arrow))

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_05_02(manim.Scene):
    def construct(self):
        # # Initialize table
        # table = manim.Table(
        #     [
        #         ["f(1)", "f(2)", "f(3)"],
        #         ["1", "2", "3"],
        #     ],
        #     col_labels=[manim.Tex("prev"), manim.Tex("curr"), manim.MathTex(r"\text{next} = \text{prev} + \text{curr}")],
        #     element_to_mobject=lambda el: SizedContainer(
        #         width=1,
        #         height=1,
        #         mobject=manim.MathTex(el),
        #     ),
        #     include_outer_lines=True,
        # )

        # # Show only f(0) and f(1) values
        # vgroup = manim.VGroup()
        # vgroup.add(table.get_entries((2, 1)))
        # vgroup.add(table.get_entries((2, 2)))
        # vgroup.add(table.get_entries((3, 1)))
        # vgroup.add(table.get_entries((3, 2)))
        # original_position = vgroup.get_center()
        # vgroup.move_to(manim.ORIGIN)

        # self.play(manim.Write(vgroup))
        # self.wait(2)

        # # Show col labels
        # self.play(vgroup.animate.move_to(original_position))
        # self.play(manim.AnimationGroup(
        #     manim.Create(table.get_col_labels()),
        #     manim.Create(table.get_horizontal_lines()),
        #     manim.Create(table.get_vertical_lines()),
        #     lag_ratio=0.5,
        #     run_time=1.5,
        # ))
        # self.wait(2)

        # # Indicate the two values being added and show next value
        # positions = [
        #     [table.get_cell((2, i)).get_center().copy() for i in range(1, 4)],
        #     [table.get_cell((3, i)).get_center().copy() for i in range(1, 4)],
        # ]
        # prev = [1, table.get_entries((2, 1)), table.get_entries((3, 1))]
        # curr = [2, table.get_entries((2, 2)), table.get_entries((3, 2))]
        # next = [prev[0] + curr[0], table.get_entries((2, 3)), table.get_entries((3, 3))]
        # for i in range(4, 7):
        #     # Indicate the two value and show next value
        #     self.play(manim.AnimationGroup(
        #         manim.AnimationGroup(
        #             manim.Indicate(prev[1]),
        #             manim.Indicate(prev[2]),
        #             manim.Indicate(curr[1]),
        #             manim.Indicate(curr[2]),
        #         ),
        #         manim.AnimationGroup(
        #             manim.Write(next[1]),
        #             manim.Write(next[2]),
        #         ),
        #         lag_ratio=0.5,
        #         run_time=1.5,
        #     ))
        #     self.wait()

        #     # Move and fade out
        #     prev[1].generate_target()
        #     prev[2].generate_target()
        #     curr[1].generate_target()
        #     curr[2].generate_target()
        #     next[1].generate_target()
        #     next[2].generate_target()

        #     prev[1].target.shift(manim.LEFT * table.get_cell((2, 1)).get_width())
        #     prev[2].target.shift(manim.LEFT * table.get_cell((3, 1)).get_width())
        #     prev[1].target.set_opacity(0)
        #     prev[2].target.set_opacity(0)
        #     curr[1].target.move_to(positions[0][0])
        #     curr[2].target.move_to(positions[1][0])
        #     next[1].target.move_to(positions[0][1])
        #     next[2].target.move_to(positions[1][1])

        #     self.play(
        #         manim.MoveToTarget(prev[1]),
        #         manim.MoveToTarget(prev[2]),
        #         manim.MoveToTarget(curr[1]),
        #         manim.MoveToTarget(curr[2]),
        #         manim.MoveToTarget(next[1]),
        #         manim.MoveToTarget(next[2]),
        #     )

        #     # Update values
        #     prev = curr.copy()
        #     curr = next.copy()

        #     # Compute next value
        #     next[0] = prev[0] + curr[0]

        #     # Set next
        #     next[1] = SizedContainer(
        #         width=1,
        #         height=1,
        #         mobject=manim.MathTex(f"f({i})"),
        #     )
        #     next[2] = SizedContainer(
        #         width=1,
        #         height=1,
        #         mobject=manim.MathTex(f"{next[0]}"),
        #     )
        #     next[1].move_to(positions[0][2])
        #     next[2].move_to(positions[1][2])

        # self.wait(2)

        # # Fade out other things except f(4) and its value
        # remain = manim.VGroup()
        # remain.add(curr[1][0])
        # remain.add(curr[2][0])

        # target = manim.MathTex(f"f(5)", "=", f"{curr[0]}", font_size=72)
        # target.center()

        # self.play(
        #     *[manim.FadeOut(mob) for mob in self.mobjects if mob not in remain],
        #     manim.Transform(remain, target),
        # )

        # self.wait(2)

        # # Fade out everything
        # self.play(*[manim.FadeOut(mob) for mob in self.mobjects])
        pass  # TODO: implement


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


def get_opaque_vmobjects(group: manim.VGroup) -> manim.VGroup:
    """
    Get everything in VGroup except for mobjects with opacity = 0.

    Arguments:
        group: the VGroup to get the opaque mobjects from
    """
    ogorup = manim.VGroup()
    for mob in group:
        if isinstance(mob, manim.VGroup):
            ogorup.add(get_opaque_vmobjects(mob))
        elif hasattr(mob, "opacity") and mob.get_opacity() != 0:
            ogorup.add(mob)
        else:
            ogorup.add(mob)
    return ogorup
