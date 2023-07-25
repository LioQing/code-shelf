from typing import Sequence, Hashable
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
    ADD_BUFF = 1.3

    def construct(self):
        # Initialize table from 1 to 8 representing f(1) to f(8)
        table = manim.MathTable(
            [
                ["1", "5", "2", "4", "3", ""],
                ["0", "0", "1", "3", "3", "6"],
            ],
            row_labels=[
                SizedContainer(
                    width=1.8,
                    height=0,
                    mobject=manim.MathTex(r"\text{cost}"),
                ),
                SizedContainer(
                    width=1.8,
                    height=0,
                    mobject=manim.MathTex(r"\text{dp}"),
                ),
            ],
            element_to_mobject=lambda el: SizedContainer(
                width=0.8,
                height=0.8,
                mobject=manim.MathTex(el),
            ),
            v_buff=0.6,
            h_buff=0.8,
            include_outer_lines=True,
        )

        # Hide all values
        hidden = manim.VGroup()
        for i in range(2, 3):
            for j in range(2, 8):
                hidden.add(table.get_entries((i, j)))
                table.get_entries((i, j)).set_opacity(0)

        # Show table
        self.play(
            manim.Create(
                manim.VGroup(
                    *[mobj for mobj in table.get_entries() if mobj not in hidden],
                    table.get_horizontal_lines(),
                    table.get_vertical_lines(),
                )
            ),
            run_time=3,
        )

        self.wait()

        # Write base cases
        set_table_mobject(table, (2, 2), manim.MathTex("0"))
        set_table_mobject(table, (2, 3), manim.MathTex("0"))
        self.play(
            manim.Write(table.get_entries((2, 2))),
            manim.Write(table.get_entries((2, 3))),
        )

        # Show addition of cost and dp
        add_label = manim.MathTex(r"\text{cost}+\text{dp}")
        add_label.next_to(table.get_cell((2, 1)), manim.DOWN * self.ADD_BUFF)

        last = manim.MathTex("1")
        last.next_to(table.get_cell((2, 2)), manim.DOWN * self.ADD_BUFF)
        curr = manim.MathTex("5")
        curr.next_to(table.get_cell((2, 3)), manim.DOWN * self.ADD_BUFF)
        self.play(
            manim.AnimationGroup(
                manim.FadeIn(add_label, shift=manim.DOWN),
                manim.AnimationGroup(
                    manim.FadeIn(last, shift=manim.DOWN),
                    manim.FadeIn(curr, shift=manim.DOWN),
                ),
                lag_ratio=0.5,
                run_time=1.5,
            )
        )

        self.wait()

        # Write arrows and recursive cases
        cost = [1, 5, 2, 4, 3]
        values = [0, 0]
        add = [1, 5]
        froms = []
        for i in range(3, 7):
            if i > 3:
                # Show add
                add = [cost[i - 3] + values[-2], cost[i - 2] + values[-1]]

                last = manim.MathTex(f"{add[-2]}")
                last.next_to(table.get_cell((2, i - 1)), manim.DOWN * self.ADD_BUFF)
                curr = manim.MathTex(f"{add[-1]}")
                curr.next_to(table.get_cell((2, i)), manim.DOWN * self.ADD_BUFF)

                self.play(
                    manim.FadeIn(last, shift=manim.DOWN),
                    manim.FadeIn(curr, shift=manim.DOWN),
                )

            # Indicate the two values being compared
            froms.append(-1 if add[-1] <= add[-2] else -2)
            min_add = curr if froms[-1] == -1 else last

            indicate_anim = manim.AnimationGroup(
                manim.Indicate(
                    last, color=manim.GREEN if min_add == last else manim.RED
                ),
                manim.Indicate(
                    curr, color=manim.GREEN if min_add == curr else manim.RED
                ),
            )

            if add[-1] == add[-2]:
                indicate_anim = manim.AnimationGroup(
                    manim.Indicate(last), manim.Indicate(curr)
                )

            self.play(indicate_anim)

            # Write recursive case and delete greater value
            value = min(add[-1], add[-2])
            values.append(value)
            set_table_mobject(table, (2, i + 1), manim.MathTex(f"{value}"))
            self.play(
                manim.FadeOut(last if froms[-1] == -1 else curr),
                manim.Transform(
                    curr if froms[-1] == -1 else last, table.get_entries((2, i + 1))
                ),
            )
            self.wait(0.34)

        self.play(manim.FadeOut(add_label))
        self.wait(2)

        # Trace back
        vbuff = 0.6
        hbuff = 0.6

        def arrow_pos(entry: manim.VMobject, direction: np.ndarray = manim.RIGHT):
            return (
                entry.get_center()
                + (entry.get_width() + hbuff) * direction / 2
                + (entry.get_height() + vbuff) * manim.DOWN / 2
            )

        i = len(values) - 1
        while i > 1:
            # Show arrow from current value to the value it came from
            f = froms[i - 2]
            arrow = manim.CurvedArrow(
                start_point=arrow_pos(
                    table.get_entries((2, i + 2 + f)), manim.RIGHT * 0.5
                ),
                end_point=arrow_pos(table.get_entries((2, i + 2)), manim.LEFT * 0.5),
                angle=manim.PI / 2,
                stroke_width=4,
            )

            self.play(
                manim.Create(arrow),
                manim.FadeToColor(table.get_entries((2, i + 2 + f)), manim.GREEN),
                manim.FadeToColor(table.get_entries((1, i + 2 + f)), manim.GREEN),
            )
            self.wait(0.5)

            i += f

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_05_02(manim.Scene):
    def construct(self):
        # Initialize the cost table
        cost_table = manim.MathTable(
            [["1", "5", "2", "4", "3"]],
            row_labels=[manim.MathTex(r"\text{cost}")],
            element_to_mobject=lambda el: SizedContainer(
                width=0.6,
                height=0.6,
                mobject=manim.MathTex(el),
            ),
            include_outer_lines=True,
        )

        initial_cost_width = cost_table.length_over_dim(0)
        cost_table.scale_to_fit_width(manim.config["frame_width"] * 0.9)  # type: ignore

        self.play(manim.Create(cost_table))
        self.wait()

        # Initialize table
        table = manim.Table(
            [["0", "0", ""]],
            element_to_mobject=lambda el: SizedContainer(
                width=0.6,
                height=0.6,
                mobject=manim.MathTex(el),
            ),
            include_outer_lines=True,
        )

        # Zoom in cost table and align it to first cell
        zoomed_cost_table = cost_table.copy()
        zoomed_cost_table.scale_to_fit_width(initial_cost_width)  # type: ignore

        zoomed_cost_table.shift(
            table.get_cell((1, 1)).get_center()
            + manim.UP * table.get_cell((1, 1)).height
            - zoomed_cost_table.get_cell((1, 2)).get_center()
        )

        self.play(manim.Transform(cost_table, zoomed_cost_table))
        self.play(manim.FadeIn(table))

        # Indicate the two values being compared and show next value
        cost = [1, 5, 2, 4, 3]
        positions = [table.get_cell((1, i)).get_center().copy() for i in range(1, 4)]
        prev = [0, table.get_entries((1, 1))]
        curr = [0, table.get_entries((1, 2))]
        next = [1, table.get_entries((1, 3))]
        for i in range(2, 6):
            # Add cost and prev/curr
            prev_add = prev[0] + cost[i - 2]
            curr_add = curr[0] + cost[i - 1]
            prev_add_mob = manim.MathTex(f"{prev_add}")
            curr_add_mob = manim.MathTex(f"{curr_add}")
            prev_add_mob.next_to(
                positions[0], manim.DOWN * table.get_cell((1, 1)).height * 3.6
            )
            curr_add_mob.next_to(
                positions[1], manim.DOWN * table.get_cell((1, 1)).height * 3.6
            )

            self.play(
                manim.FadeIn(prev_add_mob, shift=manim.DOWN),
                manim.FadeIn(curr_add_mob, shift=manim.DOWN),
            )

            min_add = prev_add_mob if prev_add <= curr_add else curr_add_mob

            # Indicate the two value being compared and show next value
            self.play(
                manim.Indicate(
                    prev_add_mob,
                    color=manim.GREEN if min_add == prev_add_mob else manim.RED,
                ),
                manim.Indicate(
                    curr_add_mob,
                    color=manim.GREEN if min_add == curr_add_mob else manim.RED,
                ),
            )

            min_add.generate_target()
            min_add.target.move_to(table.get_entries((1, 3)).get_center())

            self.play(
                manim.FadeOut(
                    curr_add_mob if min_add == prev_add_mob else prev_add_mob
                ),
                manim.MoveToTarget(min_add),
            )

            next[1] = min_add

            # Move and fade out
            prev[1].generate_target()
            curr[1].generate_target()
            next[1].generate_target()
            cost_table.generate_target()

            prev[1].target.shift(manim.LEFT * table.get_cell((1, 1)).get_width())
            prev[1].target.set_opacity(0)
            curr[1].target.move_to(positions[0])
            next[1].target.move_to(positions[1])
            cost_table.target.shift(manim.LEFT * table.get_cell((1, 1)).get_width())

            self.play(
                manim.MoveToTarget(prev[1]),
                manim.MoveToTarget(curr[1]),
                manim.MoveToTarget(next[1]),
                manim.MoveToTarget(cost_table),
            )

            # Compute next value
            next[0] = min(prev[0] + cost[i - 2], curr[0] + cost[i - 1])

            # Update values
            prev = curr.copy()
            curr = next.copy()

        self.wait(2)

        # Fade out other things except the result and its value
        remain = manim.VGroup()
        remain.add(curr[1])

        target = manim.MathTex(f"{curr[0]}", font_size=72)
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
