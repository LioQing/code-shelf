from typing import Generator, Tuple, List, Sequence
import numpy as np
import math
import manim

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.btree import BTree, BNode
from utils.sized_container import SizedContainer
from utils.table import set_table_mobject


class dp_03_01(manim.Scene):
    def construct(self):
        config = {
            "font_size": 36,
        }

        # Initialize fib(4) tree
        tree = BTree(
            build_fib_tree(4),
            hbuff=1.2,
            vbuff=1.5,
            element_to_mobject=manim.MathTex,
            element_to_mobject_config=config,
            circle_buffer_factor=1.2,
        )

        # Show tree
        stack: List[int | Tuple[BNode, manim.Line | None, BNode | None]] = []
        for group, node, arrow, parent_node in dfs_groups(tree):
            stack.append((node, arrow, parent_node))
            self.play(manim.Create(group))

            # Function to reduce and show the value and show return arrow
            def reduce_and_show(fib):
                fib_node, fib_arrow, fib_parent = stack.pop()

                # Reduce and show value
                stack.append(fib)
                value_label = manim.MathTex(f"{fib}")
                value_label.move_to(fib_node.get_mobject())

                self.play(
                    manim.Transform(fib_node.get_mobject(), value_label), run_time=0.66
                )

                # Create return arrow
                if fib_arrow is not None:
                    direction = 1 if fib_node is fib_parent.left else -1
                    return_arrow = manim.ArcBetweenPoints(
                        start=(
                            *rotate(
                                fib_node.get_mobject().get_center(),
                                fib_arrow.get_end(),
                                manim.PI / 12 * direction,
                            ),
                            0,
                        ),
                        end=(
                            *rotate(
                                fib_parent.get_mobject().get_center(),
                                fib_arrow.get_start(),
                                -manim.PI / 12 * direction,
                            ),
                            0,
                        ),
                        stroke_width=4,
                        angle=-manim.PI / 2 * direction,
                    )
                    return_arrow.add_tip(
                        tip_shape=manim.ArrowTriangleFilledTip,
                        tip_length=0.2,
                        tip_width=0.2,
                        at_start=False,
                    )
                    self.play(manim.Create(return_arrow), run_time=0.34)

            # Base cases
            if node.label == "f(0)":
                reduce_and_show(0)
            elif node.label == "f(1)":
                reduce_and_show(1)
            else:
                continue

            # Reduction
            while len(stack) >= 3:
                if isinstance(stack[-1], int) and isinstance(stack[-2], int):
                    fib = stack.pop() + stack.pop()
                    reduce_and_show(fib)
                else:
                    break

        self.wait(3)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_03_02(manim.Scene):
    def construct(self):
        config = {
            "font_size": 36,
        }

        # Initialize fib(4) tree
        tree = BTree(
            build_fib_tree(4),
            hbuff=1.2,
            vbuff=1.5,
            element_to_mobject=manim.MathTex,
            element_to_mobject_config=config,
            circle_buffer_factor=1.2,
        )

        # Show tree from bottom to top
        for node in reversed(list(BTree.dfs_right_to_left(tree.root))):
            # Show arrow
            for arrow in [node.left_arrow, node.right_arrow]:
                if arrow is not None:
                    start, end = arrow.get_start_and_end()
                    arrow.put_start_and_end_on(end, start)

            if node.left_arrow is not None and node.right_arrow is not None:
                self.play(
                    *(
                        manim.Create(arrow)
                        for arrow in [node.left_arrow, node.right_arrow]
                        if arrow is not None
                    ),
                    run_time=0.34,
                )

            # Show node
            self.play(
                manim.Create(node.get_circle()),
                manim.Create(node.get_mobject()),
                run_time=0.66,
            )

            # Show value
            def show_value(value):
                value_label = manim.MathTex(f"{value}")
                value_label.move_to(node.get_mobject())
                self.play(
                    manim.Transform(node.get_mobject(), value_label), run_time=0.66
                )
                node.mobject = value_label

            # Base cases
            if node.label == "f(0)":
                show_value(0)
            elif node.label == "f(1)":
                show_value(1)
            else:
                value = int(node.left.get_mobject().tex_string) + int(
                    node.right.get_mobject().tex_string
                )
                show_value(value)

        self.wait(3)
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


class dp_03_03(manim.Scene):
    def construct(self):
        # Initialize table from 0 to 4 representing fib(0) to fib(4)
        table = manim.MathTable(
            [["0", "1", "1", "2", "3"]],
            row_labels=[manim.MathTex(r"\text{dp}")],
            col_labels=[
                SizedContainer(
                    width=1,
                    height=0,
                    mobject=manim.MathTex(f"f({i})"),
                )
                for i in range(5)
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
        set_table_mobject(table, (2, 2), manim.MathTex("0"))
        set_table_mobject(table, (2, 3), manim.MathTex("1"))
        self.play(
            manim.Write(table.get_entries((2, 2))),
            manim.Write(table.get_entries((2, 3))),
        )
        self.wait()

        # Write arrows and recursive cases
        values = [0, 1]
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


class dp_03_04(manim.Scene):
    def construct(self):
        # Initialize table
        table = manim.Table(
            [
                ["f(0)", "f(1)", "f(2)"],
                ["0", "1", "1"],
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
        prev = [0, table.get_entries((2, 1)), table.get_entries((3, 1))]
        curr = [1, table.get_entries((2, 2)), table.get_entries((3, 2))]
        next = [prev[0] + curr[0], table.get_entries((2, 3)), table.get_entries((3, 3))]
        for i in range(3, 6):
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

        target = manim.MathTex(f"f(4)", "=", f"{curr[0]}", font_size=72)
        target.center()

        self.play(
            *[manim.FadeOut(mob) for mob in self.mobjects if mob not in remain],
            manim.Transform(remain, target),
        )

        self.wait(2)

        # Fade out everything
        self.play(*[manim.FadeOut(mob) for mob in self.mobjects])


def rotate(origin: Sequence, point: Sequence, angle: float) -> Tuple[float, float]:
    """
    Rotate a 2D point counterclockwise by a given angle around a given 2D origin.

    Arguments:
        origin: the origin of the rotation, array of shape (2,)
        point: the point to rotate, array of shape (2,)
        angle: the angle of rotation in radians
    """
    ox, oy = origin[:2]
    px, py = point[:2]

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def dfs_groups(
    tree: BTree,
) -> Generator[
    Tuple[
        manim.VGroup,
        BNode,
        manim.Line | None,
        BNode | None,
    ],
    None,
    None,
]:
    """
    Depth-first search (DFS) on a binary tree.

    Arguments:
        tree: the binary tree

    Returns:
        group: a group of nodes and arrows
        node: the current node
        parent: the parent of the current node
    """
    parent_arrow = {}
    parent = {}
    for node in BTree.dfs(tree.root):
        # Add nodes and arrows
        vgroup = manim.VGroup()
        if node != tree.root:
            vgroup.add(parent_arrow[node])
        vgroup.add(node.get_circle())
        vgroup.add(node.get_mobject())

        yield (
            vgroup,
            node,
            parent_arrow[node] if node != tree.root else None,
            parent[node] if node != tree.root else None,
        )

        if node.left is not None:
            parent_arrow[node.left] = node.get_left_arrow()
            parent[node.left] = node
        if node.right is not None:
            parent_arrow[node.right] = node.get_right_arrow()
            parent[node.right] = node


def build_fib_tree(n: int) -> BNode:
    """
    Build a Fibonacci tree with `f(n)` as root.

    Arguments:
        n: the Fibonacci number
    Returns:
        root: root of the tree
    """
    if n == 0:
        return BNode(f"f({n})")
    elif n == 1:
        return BNode(f"f({n})")
    else:
        root = BNode(f"f({n})")
        root.left = build_fib_tree(n - 1)
        root.right = build_fib_tree(n - 2)
        return root
