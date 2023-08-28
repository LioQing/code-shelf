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
    LINE_BUFFER: float = 0.25

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
                ["0", "1", "2", "3", "4", "5"],
                ["1", "0", "1", "2", "3", "4"],
                ["2", "1", "1", "2", "3", "4"],
                ["3", "2", "1", "2", "3", "4"],
                ["4", "3", "2", "2", "3", "4"],
                ["5", "4", "3", "3", "3", "3"],
            ],
            row_labels=[
                self.contained_element(manim.Tex(c))
                for c in ["", *self.WORD_X]
            ],
            col_labels=[
                self.contained_element(manim.Tex(c))
                for c in ["", *self.WORD_Y]
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
        for i in range(1, len(self.WORD_X) + 2):
            for j in range(1, len(self.WORD_Y) + 2):
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

        # Show top left
        set_table_mobject(table, (2, 2), manim.MathTex("0"))
        self.play(manim.FadeIn(table.get_entries((2, 2))))

        self.wait()

        # Add the 3 indication box
        box_curr = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((2, 2)).get_width(),
            height=table.get_cell((2, 2)).get_height(),
        )

        # Loop through everything
        dp = np.zeros((6, 6), dtype=np.int32)
        lines = [[None] * 6 for _ in range(6)]
        dp[0][0] = 0
        for i in range(1, len(self.WORD_X) + 2):
            for j in range(1, len(self.WORD_Y) + 2):
                # Skip
                if i == 1 and j == 1:
                    continue

                # Show current box
                if i == 1 and j == 2:
                    box_curr.move_to(
                        table.get_cell((1 + i, 1 + j)).get_center()
                    )
                    self.play(
                        manim.FadeIn(box_curr),
                        run_time=0.33,
                    )

                    # Add a line from previous to curr
                    lines[i - 1][j - 1] = manim.Line(
                        table.get_cell((1 + i, 1 + j - 1)).get_center(),
                        table.get_cell((1 + i, 1 + j)).get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )

                    dp[0][1] = 1
                    set_table_mobject(
                        table,
                        (1 + i, 1 + j),
                        manim.MathTex(str(dp[i - 1][j - 1])),
                    )

                    self.play(
                        manim.Create(lines[i - 1][j - 1]),
                        manim.FadeIn(table.get_entries((1 + i, 1 + j))),
                        manim.Indicate(
                            table.get_entries((1 + i, j)), color=manim.GREEN
                        ),
                        run_time=0.66,
                    )

                    self.wait(0.33)

                    continue

                # Move to position
                box_curr.generate_target()
                box_curr.target.move_to(
                    table.get_cell((1 + i, 1 + j)).get_center()
                )

                self.play(manim.MoveToTarget(box_curr), run_time=0.33)

                anim_group = []

                # Calculate dp
                if i == 1:
                    dp[i - 1][j - 1] = dp[i - 1][j - 2] + 1

                    # Indicate the previous box
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i, 1 + j - 1)),
                            color=manim.GREEN,
                        )
                    )

                    # Add line
                    lines[i - 1][j - 1] = manim.Line(
                        table.get_cell((1 + i, 1 + j - 1)).get_center(),
                        table.get_cell((1 + i, 1 + j)).get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )
                    anim_group.append(manim.Create(lines[i - 1][j - 1]))
                elif j == 1:
                    dp[i - 1][j - 1] = dp[i - 2][j - 1] + 1

                    # Indicate the previous box
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i - 1, 1 + j)),
                            color=manim.GREEN,
                        )
                    )

                    # Add line
                    lines[i - 1][j - 1] = manim.Line(
                        table.get_cell((1 + i - 1, 1 + j)).get_center(),
                        table.get_cell((1 + i, 1 + j)).get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )
                    anim_group.append(manim.Create(lines[i - 1][j - 1]))
                elif self.WORD_X[i - 2] == self.WORD_Y[j - 2]:
                    dp[i - 1][j - 1] = dp[i - 2][j - 2]

                    # Indicate the previous box
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i - 1, 1 + j - 1)),
                            color=manim.GREEN,
                        )
                    )

                    # Indicate the words
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i, 1)),
                            color=manim.GREEN,
                        )
                    )
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1, 1 + j)),
                            color=manim.GREEN,
                        )
                    )

                    # Add line
                    lines[i - 1][j - 1] = manim.Line(
                        table.get_cell((1 + i - 1, 1 + j - 1)).get_center(),
                        table.get_cell((1 + i, 1 + j)).get_center(),
                        buff=self.LINE_BUFFER,
                        color=manim.GREY,
                    )
                    anim_group.append(manim.Create(lines[i - 1][j - 1]))
                else:
                    # Indicate the word
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1 + i, 1)),
                            color=manim.RED,
                        )
                    )
                    anim_group.append(
                        manim.Indicate(
                            table.get_entries((1, 1 + j)),
                            color=manim.RED,
                        )
                    )

                    prev_pos = [
                        (1 + i - 1, 1 + j - 1),
                        (1 + i - 1, 1 + j),
                        (1 + i, 1 + j - 1),
                    ]
                    prev_colors = [manim.RED, manim.RED, manim.RED]
                    if (
                        dp[i - 1][j - 2] <= dp[i - 2][j - 2]
                        and dp[i - 1][j - 2] <= dp[i - 2][j - 1]
                    ):
                        dp[i - 1][j - 1] = dp[i - 1][j - 2] + 1
                        prev_colors[2] = manim.YELLOW

                        # Add line
                        lines[i - 1][j - 1] = manim.Line(
                            table.get_cell((1 + i, 1 + j - 1)).get_center(),
                            table.get_cell((1 + i, 1 + j)).get_center(),
                            buff=self.LINE_BUFFER,
                            color=manim.GREY,
                        )
                        anim_group.append(manim.Create(lines[i - 1][j - 1]))
                    elif (
                        dp[i - 2][j - 2] <= dp[i - 2][j - 1]
                        and dp[i - 2][j - 2] <= dp[i - 1][j - 2]
                    ):
                        dp[i - 1][j - 1] = dp[i - 2][j - 2] + 1
                        prev_colors[0] = manim.YELLOW

                        # Add line
                        lines[i - 1][j - 1] = manim.Line(
                            table.get_cell(
                                (1 + i - 1, 1 + j - 1)
                            ).get_center(),
                            table.get_cell((1 + i, 1 + j)).get_center(),
                            buff=self.LINE_BUFFER,
                            color=manim.GREY,
                        )
                        anim_group.append(manim.Create(lines[i - 1][j - 1]))
                    elif (
                        dp[i - 2][j - 1] <= dp[i - 2][j - 2]
                        and dp[i - 2][j - 1] <= dp[i - 1][j - 2]
                    ):
                        dp[i - 1][j - 1] = dp[i - 2][j - 1] + 1
                        prev_colors[1] = manim.YELLOW

                        # Add line
                        lines[i - 1][j - 1] = manim.Line(
                            table.get_cell((1 + i - 1, 1 + j)).get_center(),
                            table.get_cell((1 + i, 1 + j)).get_center(),
                            buff=self.LINE_BUFFER,
                            color=manim.GREY,
                        )
                        anim_group.append(manim.Create(lines[i - 1][j - 1]))

                    # Indicate the previous boxes
                    for k in range(3):
                        anim_group.append(
                            manim.Indicate(
                                table.get_entries(prev_pos[k]),
                                color=prev_colors[k],
                            )
                        )

                # Show dp
                set_table_mobject(
                    table, (1 + i, 1 + j), manim.MathTex(str(dp[i - 1][j - 1]))
                )
                self.play(
                    manim.FadeIn(table.get_entries((1 + i, 1 + j))),
                    *anim_group,
                    run_time=0.67,
                )

                self.wait(0.33)

        # Fade out boxes
        self.play(
            manim.FadeOut(box_curr),
        )

        # Backtrack
        i = dp.shape[0] - 1
        j = dp.shape[1] - 1
        path = [(i, j)]
        while i > 0 and j > 0:
            if self.WORD_X[i - 1] == self.WORD_Y[j - 1]:
                path.append((i - 1, j - 1))
                i -= 1
                j -= 1
            elif (
                dp[i][j - 1] <= dp[i - 1][j]
                and dp[i][j - 1] <= dp[i - 1][j - 1]
            ):
                path.append((i, j - 1))
                j -= 1
            elif (
                dp[i - 1][j - 1] <= dp[i - 1][j]
                and dp[i - 1][j - 1] <= dp[i][j - 1]
            ):
                path.append((i - 1, j - 1))
                i -= 1
                j -= 1
            elif (
                dp[i - 1][j] <= dp[i][j - 1]
                and dp[i - 1][j] <= dp[i - 1][j - 1]
            ):
                path.append((i - 1, j))
                i -= 1

        path.reverse()

        # Highlight path
        anim_group = []
        for i, j in path[1:]:
            lines[i][j].generate_target()
            lines[i][j].target.set_color(manim.GREEN)
            anim_group.append(
                manim.MoveToTarget(lines[i][j]),
            )

        for i, j in path:
            table.get_entries((i + 2, j + 2)).generate_target()
            table.get_entries((i + 2, j + 2)).target.set_color(manim.GREEN)
            anim_group.append(
                manim.MoveToTarget(table.get_entries((i + 2, j + 2))),
            )

        self.play(*anim_group)

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


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
