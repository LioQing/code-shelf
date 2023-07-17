import manim
from typing import Generator, Tuple, List

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.btree import BTree, BNode

class dp_01_01(manim.Scene):
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
        tree.shift(manim.DOWN * 0.5)

        # Show tree
        stack: List[int | Tuple[BNode, manim.Line | None]] = []
        for group, node, arrow in dfs_groups(tree):
            stack.append((node, arrow))
            self.play(manim.Create(group))

            # Function to reduce and show the value
            def reduce_and_show(fib: int):
                fib_node, fib_arrow = stack.pop()
                stack.append(fib)
                value_label = manim.MathTex(f"{fib}")
                value_label.move_to(fib_node.get_mobject())
                value_label.set_color(manim.GREEN)

                self.play(
                    manim.Transform(fib_node.get_mobject(), value_label),
                    manim.FadeToColor(fib_node.get_circle(), manim.GREEN),
                    *(manim.FadeToColor(arrow, manim.GREEN) for arrow in [fib_arrow] if arrow is not None),
                )

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

        self.wait()

        # Set one subproblem to be wrong
        wrong_path = [
            # node, value, arrow
            (tree.root.left.right, 0, tree.root.left.get_right_arrow()),
            (tree.root.left, 1, tree.root.get_left_arrow()),
            (tree.root, 2, None),
        ]
        for node, value, arrow in wrong_path:
            wrong_label = manim.MathTex(f"{value}")
            wrong_label.move_to(node.get_mobject())
            wrong_label.set_color(manim.RED)

            error_label = manim.MathTex(
                r"\text{Error} \implies \text{Wrong!}" if value == 0 else r"\text{Wrong!}",
                font_size=(28 if value == 0 else manim.DEFAULT_FONT_SIZE)
            )
            error_label.next_to(node.get_circle(), manim.DOWN if value == 0 else manim.UP)
            error_label.set_color(manim.RED)

            self.play(
                manim.Transform(node.get_mobject(), wrong_label),
                manim.FadeToColor(node.get_circle(), manim.RED),
                *(manim.FadeToColor(arrow, manim.RED) for arrow in [arrow] if arrow is not None),
            )

            if value == 0 or value == 2:
                self.play(manim.Write(error_label))
                self.wait(2)

        self.play(*[manim.FadeOut(mob)for mob in self.mobjects])

class dp_01_02(manim.Scene):
    def construct(self):
        config = {
            "font_size": 30,
        }

        # Initialize fib(5) tree
        tree = BTree(
            build_fib_tree(5),
            hbuff=0.9,
            vbuff=1.4,
            element_to_mobject=manim.MathTex,
            element_to_mobject_config=config,
            circle_buffer_factor=1.2,
        )

        # Show tree
        vgroup = manim.VGroup()
        arrows = []
        for layers in BTree.bfs_layer_by_layer(tree.root):
            subtree_layer = manim.VGroup()
            subtree_layer.add(*arrows)

            for node in layers:
                subtree_layer.add(node.get_mobject())
                subtree_layer.add(node.get_circle())
            
            vgroup.add(subtree_layer)

            arrows = []
            for node in layers:
                if node.left is not None:
                    arrows.append(node.get_left_arrow())
                if node.right is not None:
                    arrows.append(node.get_right_arrow())

        self.play(manim.Create(vgroup))
        self.wait()

        # Highlight all same subproblems with same color
        for i in range(6):
            color = manim.color.Color(hue=(i / 6), saturation=0.6, luminance=0.6)
            self.play(manim.AnimationGroup(
                *(
                    manim.AnimationGroup(
                        manim.FadeToColor(node.get_circle(), color),
                        manim.FadeToColor(node.get_mobject(), color),
                    )
                    for node in get_all_nodes(tree.root, i)
                ),
                lag_ratio=0.5,
                run_time=0.5 + len(list(get_all_nodes(tree.root, i))) * 0.5,
            ))
            self.wait()
        self.wait()

        self.play(*[manim.FadeOut(mob)for mob in self.mobjects])

def get_all_nodes(root: BNode, n: int) -> Generator[BNode, None, None]:
    """
    Get all nodes of fib(n) in the tree using DFS.

    Arguments:
        root: The tree root to get nodes from.
        n: The Fibonacci number.

    Returns:
        nodes: The generator of nodes.
    """
    return (node for node in BTree.dfs(root) if node.label == f"f({n})")

def dfs_groups(tree: BTree) -> Generator[Tuple[manim.VGroup, BNode, manim.Line | None], None, None]:
    """
    Depth-first search (DFS) on a binary tree.

    Arguments:
        tree: the binary tree

    Returns:
        group: a group of nodes and arrows
        node: the current node
        arrow: the arrow pointing to the current node
    """
    parent_arrow = {}
    for node in BTree.dfs(tree.root):
        # Add nodes and arrows
        vgroup = manim.VGroup()
        if node != tree.root:
            vgroup.add(parent_arrow[node])
        vgroup.add(node.get_circle())
        vgroup.add(node.get_mobject())

        yield vgroup, node, parent_arrow[node] if node != tree.root else None
    
        if node.left is not None:
            parent_arrow[node.left] = node.get_left_arrow()
        if node.right is not None:
            parent_arrow[node.right] = node.get_right_arrow()

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
        root.left = build_fib_tree(n-1)
        root.right = build_fib_tree(n-2)
        return root