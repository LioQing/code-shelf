import manim
import numpy as np

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.sized_container import SizedContainer
from utils.table_utils import set_table_mobject


class dp_08_01(manim.Scene):
    CAPACITY: int = 5
    WEIGHTS: list = [2, 1, 4, 3]
    VALUES: list = [20, 10, 30, 15]
    LINE_BUFFER: float = 0.32
    OVERSET_BUFFER: float = 0.32

    @staticmethod
    def contained_element(element: manim.VMobject) -> manim.VMobject:
        return SizedContainer(
            width=0.4,
            height=0.6,
            mobject=element,
        )

    def construct(self):
        # Initialize table
        table = manim.MathTable(
            [
                ["0", "0", "0", "0", "0", "0"],
                ["0", "0", "20", "20", "20", "20"],
                ["0", "10", "20", "30", "30", "30"],
                ["0", "10", "20", "30", "30", "40"],
                ["0", "10", "20", "30", "30", "40"],
            ],
            row_labels=[
                SizedContainer(
                    width=0.8,
                    height=0.6,
                    mobject=manim.Tex(""),
                ),
                *[
                    SizedContainer(
                        width=0.8,
                        height=0.6,
                        mobject=manim.Tex("(", f"{w}", ", ", f"{v}", ")"),
                    )
                    for w, v in zip(self.WEIGHTS, self.VALUES)
                ],
            ],
            col_labels=[
                self.contained_element(manim.Tex(i))
                for i in range(self.CAPACITY + 1)
            ],
            element_to_mobject=lambda el: self.contained_element(
                manim.MathTex(el)
            ),
            v_buff=0.4,
            h_buff=0.8,
            include_outer_lines=True,
        )

        # Hide all values
        hidden = manim.VGroup()
        for i in range(1, len(self.WEIGHTS) + 2):
            for j in range(1, self.CAPACITY + 2):
                hidden.add(table.get_entries((1 + i, 1 + j)))
                table.get_entries((1 + i, 1 + j)).set_opacity(0)

        # Show table
        self.play(
            manim.FadeIn(
                manim.VGroup(
                    *[
                        mobj
                        for mobj in table.get_entries()
                        if mobj not in hidden
                    ],
                    table.get_horizontal_lines(),
                    table.get_vertical_lines(),
                )
            ),
        )

        # Show all base cases
        mobjects = []
        lines = [
            [None] * (self.CAPACITY + 1) for _ in range(len(self.WEIGHTS) + 1)
        ]
        for i in range(1, len(self.WEIGHTS) + 2):
            mob = manim.MathTex("0")
            set_table_mobject(table, (1 + i, 2), mob)
            mobjects.append(mob)

            if i == 1:
                continue

            lines[i - 1][0] = manim.Line(
                table.get_cell((1 + i - 1, 2)).get_center(),
                table.get_cell((1 + i, 2)).get_center(),
                buff=self.LINE_BUFFER,
                color=manim.GREY,
            )
            mobjects.append(lines[i - 1][0])

        for i in range(2, self.CAPACITY + 2):
            mob = manim.MathTex("0")
            set_table_mobject(table, (2, 1 + i), mob)
            mobjects.append(mob)

            lines[0][i - 1] = manim.Line(
                table.get_cell((2, 1 + i - 1)).get_center(),
                table.get_cell((2, 1 + i)).get_center(),
                buff=self.LINE_BUFFER,
                color=manim.GREY,
            )
            mobjects.append(lines[0][i - 1])

        self.play(
            *[manim.FadeIn(mob) for mob in mobjects],
        )

        self.wait()

        # Add the indication boxes
        box_curr = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((2, 2)).get_width(),
            height=table.get_cell((2, 2)).get_height(),
        )
        box_top = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((2, 2)).get_width(),
            height=table.get_cell((2, 2)).get_height(),
        )
        box_left = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((2, 2)).get_width(),
            height=table.get_cell((2, 2)).get_height(),
        )
        v_left = None
        prev_entry_restore = None

        # Loop through everything
        dp = np.zeros(
            (len(self.WEIGHTS) + 1, self.CAPACITY + 1), dtype=np.int32
        )
        for i in range(2, len(self.WEIGHTS) + 2):
            for j in range(2, self.CAPACITY + 2):
                # Current weight and value
                curr_weight = self.WEIGHTS[i - 2]
                curr_value = self.VALUES[i - 2]
                curr_capacity = j - 1

                # Skip
                if i == 1 and j == 1:
                    continue

                # Show current box
                if i == 2 and j == 2:
                    box_curr.move_to(
                        table.get_cell((1 + i, 1 + j)).get_center()
                    )
                    box_top.move_to(
                        table.get_cell((1 + i - 1, 1 + j)).get_center()
                    )
                    self.play(
                        manim.FadeIn(box_curr),
                        manim.FadeIn(box_top),
                        run_time=0.33,
                    )

                    # Add a line from previous to curr
                    lines[i - 1][j - 1] = manim.Line(
                        box_top.get_center(),
                        box_curr.get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )

                    dp[0][1] = 0
                    set_table_mobject(
                        table,
                        (1 + i, 1 + j),
                        manim.MathTex(str(dp[i - 1][curr_capacity])),
                    )

                    self.play(
                        manim.Create(lines[i - 1][j - 1]),
                        manim.Indicate(
                            table.get_entries((1 + i - 1, 1 + j)),
                            color=manim.GREEN,
                        ),
                        run_time=0.67,
                    )

                    self.play(
                        manim.FadeIn(table.get_entries((1 + i, 1 + j))),
                        run_time=0.67,
                    )

                    self.wait(0.33)

                    continue

                # Move to position
                anim_group = []
                delay_anim_group = []

                box_curr.generate_target()
                box_curr.target.move_to(
                    table.get_cell((1 + i, 1 + j)).get_center()
                )

                box_top.generate_target()
                box_top.target.move_to(
                    table.get_cell((1 + i - 1, 1 + j)).get_center()
                )

                # Restore previous entry left
                if prev_entry_restore is not None:
                    anim_group.append(
                        manim.Transform(
                            table.get_entries(prev_entry_restore[0]),
                            prev_entry_restore[1],
                        )
                    )
                    prev_entry_restore = None

                if j == 2:
                    # Fade out old value left and restore value
                    anim_group.append(manim.FadeOut(v_left))

                    if curr_weight <= curr_capacity:
                        entry_left = table.get_entries(
                            (1 + i - 1, 1 + j - curr_weight)
                        )

                        # Box left
                        box_left.generate_target()
                        box_left.target.move_to(entry_left.get_center())

                        (
                            v_left,
                            prev_entry_restore,
                        ) = self.animate_value_and_entry_left(
                            delay_anim_group,
                            dp,
                            curr_value,
                            curr_capacity,
                            curr_weight,
                            table,
                            entry_left,
                            i,
                            j,
                        )
                    else:
                        box_left.generate_target()
                        box_left.target.set_opacity(0)
                else:
                    if curr_weight == curr_capacity:
                        entry_left = table.get_entries(
                            (1 + i - 1, 1 + j - curr_weight)
                        )

                        # Box left
                        box_left.move_to(entry_left.get_center())
                        box_left.generate_target()
                        box_left.target.set_stroke(opacity=1)

                        (
                            v_left,
                            prev_entry_restore,
                        ) = self.animate_value_and_entry_left(
                            anim_group,
                            dp,
                            curr_value,
                            curr_capacity,
                            curr_weight,
                            table,
                            entry_left,
                            i,
                            j,
                        )
                    elif curr_weight < curr_capacity:
                        entry_left = table.get_entries(
                            (1 + i - 1, 1 + j - curr_weight)
                        )

                        # Box left
                        box_left.generate_target()
                        box_left.target.move_to(entry_left.get_center())

                        (
                            v_left,
                            prev_entry_restore,
                        ) = self.animate_value_and_entry_left(
                            anim_group,
                            dp,
                            curr_value,
                            curr_capacity,
                            curr_weight,
                            table,
                            entry_left,
                            i,
                            j,
                            v_left,
                        )

                self.play(
                    *anim_group,
                    manim.MoveToTarget(box_curr),
                    manim.MoveToTarget(box_top),
                    manim.MoveToTarget(box_left),
                    run_time=0.33,
                )

                if len(delay_anim_group) > 0:
                    self.play(
                        *delay_anim_group,
                        run_time=0.33,
                    )

                anim_group = []

                # Calculate dp
                if curr_weight <= curr_capacity:
                    not_take = dp[i - 2][curr_capacity]
                    take = dp[i - 2][curr_capacity - curr_weight] + curr_value

                    if take > not_take:
                        dp[i - 1][curr_capacity] = take
                        anim_group.append(
                            manim.Indicate(
                                manim.VGroup(
                                    v_left,
                                    table.get_entries(
                                        (1 + i - 1, 1 + j - curr_weight)
                                    ),
                                ),
                                color=manim.GREEN,
                            ),
                        )
                        anim_group.append(
                            manim.FadeToColor(
                                table.get_entries((1 + i, 1 + j)),
                                manim.GREEN,
                            ),
                        )
                        anim_group.append(
                            manim.Indicate(
                                table.get_entries((1 + i - 1, 1 + j)),
                                color=manim.RED,
                            )
                        )

                        # Add a line from previous to curr
                        lines[i - 1][j - 1] = manim.Line(
                            box_left.get_center(),
                            box_curr.get_center(),
                            buff=self.LINE_BUFFER,
                            color=manim.GREY,
                        )
                    else:
                        dp[i - 1][curr_capacity] = not_take
                        anim_group.append(
                            manim.Indicate(
                                manim.VGroup(
                                    v_left,
                                    table.get_entries(
                                        (1 + i - 1, 1 + j - curr_weight)
                                    ),
                                ),
                                color=manim.RED,
                            )
                        )
                        anim_group.append(
                            manim.Indicate(
                                table.get_entries((1 + i - 1, 1 + j)),
                                color=manim.GREEN,
                            )
                        )

                        # Add a line from previous to curr
                        lines[i - 1][j - 1] = manim.Line(
                            box_top.get_center(),
                            box_curr.get_center(),
                            buff=self.LINE_BUFFER,
                            color=manim.GREY,
                        )
                else:
                    dp[i - 1][curr_capacity] = dp[i - 2][curr_capacity]
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i - 1, 1 + j)),
                            color=manim.GREEN,
                        )
                    )

                    # Add a line from previous to curr
                    lines[i - 1][j - 1] = manim.Line(
                        box_top.get_center(),
                        box_curr.get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )

                # Show dp
                set_table_mobject(
                    table,
                    (1 + i, 1 + j),
                    manim.MathTex(str(dp[i - 1][curr_capacity])),
                )
                self.play(
                    manim.Create(lines[i - 1][j - 1]),
                    *anim_group,
                    run_time=0.67,
                )

                self.play(
                    manim.FadeIn(table.get_entries((1 + i, 1 + j))),
                    run_time=0.67,
                )

                self.wait(0.33)

        # Fade out boxes
        self.play(
            manim.FadeOut(v_left),
            manim.FadeOut(box_curr),
            manim.FadeOut(box_top),
            manim.FadeOut(box_left),
        )

        # Backtrack
        anim_group = []
        i = len(self.WEIGHTS)
        j = self.CAPACITY
        while i > 0:
            anim_group.append(
                manim.FadeToColor(
                    table.get_entries((2 + i, 2 + j)),
                    color=manim.GREEN,
                )
            )
            anim_group.append(
                manim.FadeToColor(
                    lines[i][j],
                    color=manim.GREEN,
                )
            )
            if dp[i][j] != dp[i - 1][j]:
                j -= self.WEIGHTS[i - 1]
            i -= 1

        anim_group.append(
            manim.FadeToColor(
                table.get_entries((2, 2)),
                color=manim.GREEN,
            )
        )

        self.play(
            *anim_group,
        )

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])

    def animate_value_and_entry_left(
        self,
        anim_group,
        dp,
        curr_value,
        curr_capacity,
        curr_weight,
        table,
        entry_left,
        i,
        j,
        old_v_left=None,
    ):
        target_v_left = manim.MathTex(
            f"{curr_value}",
            "+",
            f"{dp[i - 2][curr_capacity - curr_weight]}",
            font_size=24,
        )
        target_v_left.move_to(
            entry_left.get_center() + self.OVERSET_BUFFER * manim.UP
        )

        if old_v_left is None:
            value = table.get_entries((1 + i, 1))
            value.__class__ = SizedContainer
            v_left = value.element[3].copy()
        else:
            v_left = old_v_left

        anim_group.append(
            manim.Transform(
                v_left,
                target_v_left,
            )
        )

        # Entry left
        prev_entry_restore = (
            (1 + i - 1, 1 + j - curr_weight),
            entry_left.copy(),
        )
        target_entry_left = manim.MathTex(
            f"{dp[i - 2][curr_capacity - curr_weight] + curr_value}",
        )
        target_entry_left.move_to(entry_left.get_center())
        anim_group.append(
            manim.Transform(
                entry_left,
                target_entry_left,
            )
        )

        return v_left, prev_entry_restore


# class dp_07_02(manim.Scene):
#     WORD_X: str = "sunny"
#     WORD_Y: str = "snowy"
#     LINE_BUFFER: float = 0.25

#     @staticmethod
#     def contained_element(element: manim.VMobject) -> manim.VMobject:
#         return SizedContainer(
#             width=0.8,
#             height=0.8,
#             mobject=element,
#         )

#     def construct(self):
#         # Initialize table
#         table = manim.MathTable(
#             [
#                 ["0", "1", "2", "3", "4", "5"],
#                 # ["1", "0", "1", "2", "3", "4"],
#                 # ["2", "1", "1", "2", "3", "4"],
#                 # ["3", "2", "1", "2", "3", "4"],
#                 # ["4", "3", "2", "2", "3", "4"],
#                 # ["5", "4", "3", "3", "3", "3"],
#             ],
#             col_labels=[
#                 self.contained_element(manim.Tex(c)) for c in ["", *self.WORD_Y]
#             ],
#             element_to_mobject=lambda el: self.contained_element(manim.MathTex(el)),
#             v_buff=0.4,
#             h_buff=0.8,
#             include_outer_lines=True,
#         )

#         # Initialize word x table
#         word_x_table = manim.MathTable(
#             [[""]] + [[c] for c in self.WORD_X],
#             element_to_mobject=lambda el: self.contained_element(manim.MathTex(el)),
#             v_buff=0.4,
#             h_buff=0.8,
#             include_outer_lines=True,
#         )

#         word_x_table.move_to(
#             table.get_cell((2, 1)).get_corner(manim.UP + manim.LEFT)
#             + word_x_table.width * 0.5 * manim.LEFT
#             + word_x_table.height * 0.5 * manim.DOWN
#         )

#         # Center
#         group = manim.VGroup(table, word_x_table)
#         group.shift(group.get_center() * manim.LEFT)

#         # Hide all values
#         hidden = manim.VGroup()
#         for j in range(1, len(self.WORD_Y) + 2):
#             hidden.add(table.get_entries((2, j)))
#             table.get_entries((2, j)).set_opacity(0)

#         # Show table
#         top_left_label = manim.MathTex(r"\text{top left}", "=", "0")
#         top_left_label.move_to(
#             table.get_cell((1, 1)).get_left()
#             + table.get_cell((1, 1)).height * manim.UP
#             + (top_left_label.width / 2 + 0.4) * manim.RIGHT
#         )
#         self.play(
#             manim.FadeIn(
#                 manim.VGroup(
#                     *[mobj for mobj in table.get_entries() if mobj not in hidden],
#                     table.get_horizontal_lines(),
#                     table.get_vertical_lines(),
#                 ),
#                 top_left_label,
#                 word_x_table,
#             ),
#         )

#         # Show (0, 0)
#         set_table_mobject(table, (2, 1), manim.MathTex("0"))
#         self.play(manim.FadeIn(table.get_entries((2, 1))))

#         # Add the 3 indication box
#         box_curr = manim.Rectangle(
#             color=manim.YELLOW,
#             width=table.get_cell((2, 1)).get_width(),
#             height=table.get_cell((2, 1)).get_height(),
#         )

#         # Loop through everything
#         top_left = 0
#         dp = [0] * 6
#         dp[0] = 0
#         for i in range(1, len(self.WORD_X) + 2):
#             for j in range(1, len(self.WORD_Y) + 2):
#                 # Skip
#                 if i == 1 and j == 1:
#                     continue

#                 # Show current box
#                 if i == 1:
#                     if j == 2:
#                         box_curr.move_to(table.get_cell((2, j)).get_center())
#                         self.play(
#                             manim.FadeIn(box_curr),
#                             run_time=0.33,
#                         )
#                     else:
#                         box_curr.generate_target()
#                         box_curr.target.move_to(table.get_cell((2, j)).get_center())
#                         self.play(manim.MoveToTarget(box_curr), run_time=0.33)

#                     dp[j - 1] = j - 1
#                     set_table_mobject(table, (2, j), manim.MathTex(str(dp[j - 1])))

#                     self.play(
#                         manim.FadeIn(table.get_entries((2, j))),
#                         run_time=0.67,
#                     )

#                     self.wait(0.33)

#                     continue

#                 anim_group = []
#                 # Move to position
#                 box_curr.generate_target()
#                 box_curr.target.move_to(table.get_cell((2, j)).get_center())

#                 anim_group.append(manim.MoveToTarget(box_curr))

#                 if j == 1:
#                     # Move word X table
#                     word_x_table.generate_target()
#                     word_x_table.target.shift(table.get_cell((1, 1)).height * manim.UP)

#                     anim_group.append(manim.MoveToTarget(word_x_table))

#                 self.play(*anim_group, run_time=0.33)

#                 anim_group = []

#                 # Calculate dp
#                 from_mob = None
#                 new_top_left = dp[j - 1]
#                 if i == 1:
#                     dp[j - 1] = dp[j - 2] + 1

#                     # Indicate the previous box
#                     anim_group.append(
#                         manim.Indicate(
#                             table.get_entries((2, j - 1)),
#                             color=manim.GREEN,
#                         )
#                     )

#                     from_mob = table.get_entries((2, j - 1))
#                 elif j == 1:
#                     dp[j - 1] = dp[j - 1] + 1

#                     # Indicate the previous box
#                     anim_group.append(
#                         manim.Indicate(
#                             table.get_entries((2, j)),
#                             color=manim.GREEN,
#                         )
#                     )

#                     from_mob = table.get_entries((2, j))
#                 elif self.WORD_X[i - 2] == self.WORD_Y[j - 2]:
#                     dp[j - 1] = top_left

#                     # Indicate the previous box
#                     anim_group.append(
#                         manim.Indicate(
#                             top_left_label[2],
#                             color=manim.GREEN,
#                         )
#                     )

#                     # Indicate the words
#                     anim_group.append(
#                         manim.Indicate(
#                             word_x_table.get_entries((i, 1)),
#                             color=manim.GREEN,
#                         )
#                     )
#                     anim_group.append(
#                         manim.Indicate(
#                             table.get_entries((1, j)),
#                             color=manim.GREEN,
#                         )
#                     )

#                     from_mob = top_left_label[2]
#                 else:
#                     # Indicate the word
#                     anim_group.append(
#                         manim.Indicate(
#                             word_x_table.get_entries((i, 1)),
#                             color=manim.RED,
#                         )
#                     )
#                     anim_group.append(
#                         manim.Indicate(
#                             table.get_entries((1, j)),
#                             color=manim.RED,
#                         )
#                     )

#                     prev_mob = [
#                         top_left_label[2],
#                         table.get_entries((2, j)),
#                         table.get_entries((2, j - 1)),
#                     ]
#                     prev_colors = [manim.RED, manim.RED, manim.RED]
#                     if dp[j - 2] <= top_left and dp[j - 2] <= dp[j - 1]:
#                         dp[j - 1] = dp[j - 2] + 1
#                         prev_colors[2] = manim.YELLOW
#                     elif top_left <= dp[j - 1] and top_left <= dp[j - 2]:
#                         dp[j - 1] = top_left + 1
#                         prev_colors[0] = manim.YELLOW
#                     elif dp[j - 1] <= top_left and dp[j - 1] <= dp[j - 2]:
#                         dp[j - 1] = dp[j - 1] + 1
#                         prev_colors[1] = manim.YELLOW

#                     # Indicate the previous boxes
#                     for k in range(3):
#                         anim_group.append(
#                             manim.Indicate(
#                                 prev_mob[k],
#                                 color=prev_colors[k],
#                             )
#                         )

#                     from_mob = prev_mob[prev_colors.index(manim.YELLOW)]

#                 top_left = new_top_left

#                 # Show dp
#                 original = table.get_entries((2, j))
#                 new_dp = manim.MathTex(str(dp[j - 1]))
#                 new_dp.move_to(
#                     original.get_center() + table.get_cell((2, j)).height * manim.DOWN,
#                 )

#                 self.play(
#                     *anim_group,
#                     manim.ReplacementTransform(from_mob.copy(), new_dp),
#                     run_time=0.67,
#                 )

#                 # Update top_left and dp mobjects
#                 new_top_left_label = manim.MathTex(
#                     r"\text{top left}", "=", str(top_left)
#                 )
#                 new_top_left_label.move_to(top_left_label)

#                 new_dp.generate_target()
#                 new_dp.target.move_to(original.get_center())

#                 self.remove(original)

#                 moved_original = original.copy()
#                 self.play(
#                     manim.Transform(moved_original, new_top_left_label[2]),
#                     manim.Transform(top_left_label, new_top_left_label),
#                     manim.MoveToTarget(new_dp),
#                     run_time=0.33,
#                 )
#                 self.remove(moved_original)

#                 set_table_mobject(table, (2, j), new_dp)
#                 self.remove(top_left_label)
#                 top_left_label = new_top_left_label.copy()
#                 self.add(top_left_label)

#                 self.wait(0.33)

#         # Fade out boxes
#         self.play(
#             manim.FadeOut(box_curr),
#         )

#         self.wait(2)
#         self.play(*[manim.FadeOut(mob) for mob in self.mobjects])
