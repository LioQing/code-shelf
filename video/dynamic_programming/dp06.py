from typing import Sequence
import manim
import numpy as np

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.sized_container import SizedContainer
from utils.table_utils import set_table_mobject


class dp_06_01(manim.Scene):
    def construct(self):
        # Initialize table
        table = manim.MathTable(
            [
                ["1", "1", "1", "1", "1", "1", "1"],
                ["1", "2", "3", "4", "5", "6", "7"],
                ["1", "3", "6", "10", "15", "21", "28"],
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
        for i in range(1, 4):
            for j in range(1, 8):
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
        )

        # Show top left
        set_table_mobject(table, (1, 1), manim.MathTex("1"))
        self.play(manim.FadeIn(table.get_entries((1, 1))))

        self.wait()

        # Add the 3 indication box
        box_curr = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((1, 1)).get_width(),
            height=table.get_cell((1, 1)).get_height(),
        )

        box_left = box_curr.copy()
        box_left.shift(manim.LEFT * table.get_cell((1, 1)).get_width())

        box_top = box_curr.copy()
        box_top.shift(manim.UP * table.get_cell((1, 1)).get_height())

        # Loop through everything
        dp = np.zeros((3, 7), dtype=np.int32)
        dp[0][0] = 1
        for i in range(1, 4):
            for j in range(1, 8):
                # Skip
                if i == 1 and j == 1:
                    continue

                # Show current box
                if i == 1 and j == 2:
                    box_curr.move_to(table.get_cell((i, j)).get_center())
                    box_left.next_to(
                        box_curr, manim.LEFT * box_curr.get_width(), buff=0
                    )
                    box_top.next_to(box_curr, manim.UP * box_curr.get_height(), buff=0)
                    self.play(
                        manim.FadeIn(box_curr),
                        manim.FadeIn(box_left),
                        run_time=0.33,
                    )

                    dp[0][1] = 1
                    set_table_mobject(
                        table, (i, j), manim.MathTex(str(dp[i - 1][j - 1]))
                    )
                    self.play(manim.FadeIn(table.get_entries((i, j))), run_time=0.33)

                    self.wait(0.67)

                    continue

                # Move to position
                box_curr.generate_target()
                box_curr.target.move_to(table.get_cell((i, j)).get_center())

                box_left.generate_target()
                box_left.target.next_to(
                    table.get_cell((i, j)),
                    manim.LEFT,
                    buff=0,
                )

                # Include top if not first row
                if i == 2 and j == 1:
                    box_top.generate_target()
                    box_top.target.set_stroke(opacity=1)
                    box_top.target.next_to(
                        table.get_cell((i, j)),
                        manim.UP,
                        buff=0,
                    )
                elif i != 1:
                    box_top.generate_target()
                    box_top.target.next_to(
                        table.get_cell((i, j)),
                        manim.UP,
                        buff=0,
                    )
                elif i == 1 and j == 7:
                    box_top.set_opacity(0)
                    box_top.next_to(
                        table.get_cell((i, j)),
                        manim.UP,
                        buff=0,
                    )

                # Hide left if first column
                if j == 1:
                    box_left.target.set_opacity(0)
                elif j == 2:
                    box_left.target.set_stroke(opacity=1)

                # Play animation
                anim_group = [
                    manim.MoveToTarget(box_curr),
                    manim.MoveToTarget(box_left),
                ]

                if i != 1:
                    anim_group.append(manim.MoveToTarget(box_top))

                self.play(*anim_group, run_time=0.33)

                # Calculate dp
                if i == 1:
                    dp[i - 1][j - 1] = dp[i - 1][j - 2]
                elif j == 1:
                    dp[i - 1][j - 1] = dp[i - 2][j - 1]
                else:
                    dp[i - 1][j - 1] = dp[i - 1][j - 2] + dp[i - 2][j - 1]

                # Show dp
                set_table_mobject(table, (i, j), manim.MathTex(str(dp[i - 1][j - 1])))
                self.play(manim.FadeIn(table.get_entries((i, j))), run_time=0.33)

                self.wait(0.67)

        # Fade out boxes
        self.play(
            manim.FadeOut(box_curr),
            manim.FadeOut(box_left),
            manim.FadeOut(box_top),
        )

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_06_02(manim.Scene):
    def construct(self):
        # Initialize table
        table = manim.MathTable(
            [
                ["0", "1", "0", "0", "0", "0", "0", "0"],
                ["0", "1", "1", "1", "1", "1", "1", "1"],
                ["0", "1", "2", "3", "4", "5", "6", "7"],
                ["0", "1", "3", "6", "10", "15", "21", "28"],
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
        for i in range(1, 5):
            for j in range(1, 9):
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
        )

        # Show top left
        anim_group = []
        for i, c in enumerate(["0", "1", "0", "0", "0", "0", "0", "0"]):
            set_table_mobject(table, (1, i + 1), manim.MathTex(c))
            anim_group.append(manim.FadeIn(table.get_entries((1, i + 1))))

        for j in range(2, 5):
            set_table_mobject(table, (j, 1), manim.MathTex("0"))
            anim_group.append(manim.FadeIn(table.get_entries((j, 1))))

        self.play(*anim_group)

        self.wait()

        # Add the 3 indication box
        box_curr = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((1, 1)).get_width(),
            height=table.get_cell((1, 1)).get_height(),
        )

        box_left = box_curr.copy()
        box_left.shift(manim.LEFT * table.get_cell((1, 1)).get_width())

        box_top = box_curr.copy()
        box_top.shift(manim.UP * table.get_cell((1, 1)).get_height())

        # Loop through everything
        dp = np.zeros((4, 8), dtype=np.int32)
        dp[0][1] = 1
        for i in range(2, 5):
            for j in range(2, 9):
                # Show current box
                if i == 2 and j == 2:
                    box_curr.move_to(table.get_cell((i, j)).get_center())
                    box_left.next_to(
                        box_curr, manim.LEFT * box_curr.get_width(), buff=0
                    )
                    box_top.next_to(box_curr, manim.UP * box_curr.get_height(), buff=0)
                    self.play(
                        manim.FadeIn(box_curr),
                        manim.FadeIn(box_left),
                        manim.FadeIn(box_top),
                        run_time=0.33,
                    )

                    dp[i - 1][j - 1] = dp[i - 1][j - 2] + dp[i - 2][j - 1]
                    set_table_mobject(
                        table, (i, j), manim.MathTex(str(dp[i - 1][j - 1]))
                    )
                    self.play(manim.FadeIn(table.get_entries((i, j))), run_time=0.33)

                    self.wait(0.67)

                    continue

                # Move to position
                box_curr.generate_target()
                box_curr.target.move_to(table.get_cell((i, j)).get_center())

                box_left.generate_target()
                box_left.target.next_to(
                    table.get_cell((i, j)),
                    manim.LEFT,
                    buff=0,
                )

                box_top.generate_target()
                box_top.target.next_to(
                    table.get_cell((i, j)),
                    manim.UP,
                    buff=0,
                )

                # Play animation
                anim_group = [
                    manim.MoveToTarget(box_curr),
                    manim.MoveToTarget(box_left),
                    manim.MoveToTarget(box_top),
                ]

                self.play(*anim_group, run_time=0.33)

                # Calculate dp
                dp[i - 1][j - 1] = dp[i - 1][j - 2] + dp[i - 2][j - 1]

                # Show dp
                set_table_mobject(table, (i, j), manim.MathTex(str(dp[i - 1][j - 1])))
                self.play(manim.FadeIn(table.get_entries((i, j))), run_time=0.33)

                self.wait(0.67)

        # Fade out boxes
        self.play(
            manim.FadeOut(box_curr),
            manim.FadeOut(box_left),
            manim.FadeOut(box_top),
        )

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_06_03(manim.Scene):
    def construct(self):
        # Initialize table
        table = manim.MathTable(
            [
                ["0", "1", "0", "0", "0", "0", "0", "0"],
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
        for j in range(1, 9):
            hidden.add(table.get_entries((1, j)))
            table.get_entries((1, j)).set_opacity(0)

        # Show table
        self.play(
            manim.Create(
                manim.VGroup(
                    *[mobj for mobj in table.get_entries() if mobj not in hidden],
                    table.get_horizontal_lines(),
                    table.get_vertical_lines(),
                )
            ),
        )

        # Show top
        anim_group = []
        for i, c in enumerate(["0", "1", "0", "0", "0", "0", "0", "0"]):
            set_table_mobject(table, (1, i + 1), manim.MathTex(c))
            anim_group.append(manim.FadeIn(table.get_entries((1, i + 1))))

        self.play(*anim_group)

        self.wait()

        # Add the 3 indication box
        box_curr = manim.Rectangle(
            color=manim.YELLOW,
            width=table.get_cell((1, 1)).get_width(),
            height=table.get_cell((1, 1)).get_height(),
        )

        box_left = box_curr.copy()
        box_left.shift(manim.LEFT * table.get_cell((1, 1)).get_width())

        box_top = box_curr.copy()
        box_top.shift(manim.UP * table.get_cell((1, 1)).get_height())

        # Loop through everything
        dp = np.zeros((8,), dtype=np.int32)
        dp[1] = 1
        i_label = manim.MathTex("i=", str(1))
        for i in range(2, 5):
            for j in range(2, 9):
                # Show current box
                if i == 2 and j == 2:
                    # Boxes
                    box_top.move_to(table.get_cell((1, j)).get_center())
                    box_left.next_to(box_top, manim.LEFT * box_top.get_width(), buff=0)

                    # i label
                    i_label.move_to(
                        table.get_cell((1, 1)).get_left()
                        + manim.RIGHT * i_label.width / 2
                        + manim.UP * box_top.height
                    )

                    self.play(
                        manim.FadeIn(box_left),
                        manim.FadeIn(box_top),
                        manim.FadeIn(i_label),
                        run_time=0.33,
                    )

                    dp[j - 1] = dp[j - 2] + dp[j - 1]

                    # Show new value
                    value = manim.MathTex(str(dp[j - 1]))
                    value.next_to(
                        table.get_cell((1, j)),
                        manim.DOWN * table.get_cell((1, j)).get_height(),
                    )

                    self.play(manim.FadeIn(value, shift=manim.DOWN), run_time=0.33)

                    self.wait(0.67)

                    # Overwrite value
                    value.generate_target()
                    value.target.move_to(table.get_cell((1, j)).get_center())
                    self.play(
                        manim.FadeOut(table.get_entries((1, j)), shift=manim.UP),
                        manim.MoveToTarget(value),
                        run_time=0.33,
                    )
                    set_table_mobject(table, (1, j), value)

                    continue

                # Move to position
                box_top.generate_target()
                box_top.target.move_to(table.get_cell((1, j)).get_center())

                box_left.generate_target()
                box_left.target.next_to(
                    table.get_cell((1, j)),
                    manim.LEFT,
                    buff=0,
                )

                # i label
                new_i_label = manim.MathTex("i=", str(i - 1))
                new_i_label.move_to(
                    table.get_cell((1, 1)).get_left()
                    + manim.RIGHT * new_i_label.width / 2
                    + manim.UP * box_top.height
                )

                # Play animation
                anim_group = [
                    manim.MoveToTarget(box_left),
                    manim.MoveToTarget(box_top),
                    manim.Transform(
                        i_label, new_i_label, replace_mobject_with_target_in_scene=True
                    ),
                ]

                self.play(*anim_group, run_time=0.33)

                i_label = new_i_label

                # Calculate dp
                dp[j - 1] = dp[j - 2] + dp[j - 1]

                # Show new value
                value = manim.MathTex(str(dp[j - 1]))
                value.next_to(
                    table.get_cell((1, j)),
                    manim.DOWN * table.get_cell((1, j)).get_height(),
                )

                self.play(manim.FadeIn(value, shift=manim.DOWN), run_time=0.33)

                self.wait(0.67)

                # Overwrite value
                value.generate_target()
                value.target.move_to(table.get_cell((1, j)).get_center())
                self.play(
                    manim.FadeOut(table.get_entries((1, j)), shift=manim.UP),
                    manim.MoveToTarget(value),
                    run_time=0.33,
                )
                set_table_mobject(table, (1, j), value)

        # Fade out boxes
        self.play(
            manim.FadeOut(box_left),
            manim.FadeOut(box_top),
        )

        self.wait(2)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])
