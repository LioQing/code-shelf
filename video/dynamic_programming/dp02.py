from typing import Generator
import numpy as np
import manim

# Needed to have relative import
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.btree import BTree, BNode

class dp_02_01(manim.Scene):
    def construct(self):
        config = {
            "font_size": 36,
        }

        # Initialize fib(12)
        tree = BTree(
            build_fib_tree(12),
            hbuff=1.2,
            vbuff=1.5,
            element_to_mobject=manim.MathTex,
            element_to_mobject_config=config,
            circle_buffer_factor=1.2,
        )

        # Play subtree
        subtree_root = next(get_all_nodes(tree.root, 4))
        subtree = self._play_subtree(tree, subtree_root)
        self.wait()

        label = manim.MathTex(r"n = 4 \implies \text{No. of nodes} = 9")
        label.next_to(subtree_root.get_mobject().get_center(), manim.UP * 4)
        self.play(manim.Write(label))

        # Show overlapping subproblems for subtree
        overlapping_subproblems = manim.VGroup()
        encountered = set()
        for node in BTree.dfs(subtree_root):
            if node.label in encountered:
                overlapping_subproblems.add(node.get_circle())
                overlapping_subproblems.add(node.get_mobject())
            else:
                encountered.add(node.label)
        
        self.play(manim.FadeToColor(overlapping_subproblems, manim.YELLOW))
        self.wait(2)
        self.play(manim.Unwrite(label))

        # Set color for overlapping subproblems for tree
        encountered = set()
        for node in BTree.dfs(tree.root):
            if node.label in encountered:
                node.get_circle().set_color(manim.YELLOW) # type: ignore
                node.get_mobject().set_color(manim.YELLOW) # type: ignore
            else:
                encountered.add(node.label)

        # Show remaining tree
        self._play_except_subtree(tree, subtree_root)
        
        tree.generate_target()
        tree.target.center() # type: ignore
        tree.target.shift(manim.DOWN) # type: ignore
        tree.target.set_fill(opacity=1) # type: ignore
        tree.target.set_vbuff(32) # type: ignore
        tree.target.scale_to_fit_width(manim.config["frame_width"] * 0.9) # type: ignore

        self.play(manim.MoveToTarget(
            tree,
            run_time=5,
            rate_func=manim.rate_functions.ease_in_out_sine,
        ))

        label = manim.MathTex(r"n \implies \text{No. of nodes} = O(2^n)")
        label.next_to(tree.root.get_mobject().get_center(), manim.UP * 2)
        self.play(manim.Write(label))
        self.wait(3)
        time_label = manim.MathTex(r"\text{Time complexity} = O(2^n)")
        time_label.next_to(tree.root.get_mobject().get_center(), manim.UP * 2)
        self.play(manim.Transform(label, time_label))
        self.wait(3)
        self.play(manim.Unwrite(label))

        self.play(manim.ShrinkToCenter(
            tree,
            run_time=2,
            rate_func=manim.rate_functions.ease_in_sine,
        ))
        self.wait()

    def _play_subtree(self, tree: BTree, subtree_root: BNode) -> manim.VGroup:
        """
        Play the subtree rooted at `f(n)`.

        Arguments:
            tree: The tree to find the subtree.
            subtree_root: The root node of the subtree.
        
        Returns:
            subtree: The VGroup of nodes of subtree rooted at `f(n)`, by layers.
        """
        # BFS fib(n)
        subtree = manim.VGroup()

        arrows = []
        for layers in BTree.bfs_layer_by_layer(subtree_root):
            subtree_layer = manim.VGroup()
            subtree_layer.add(*arrows)

            for node in layers:
                subtree_layer.add(node.get_mobject())
                subtree_layer.add(node.get_circle())
            
            subtree.add(subtree_layer)

            arrows = []
            for node in layers:
                if node.left is not None:
                    arrows.append(node.get_left_arrow())
                if node.right is not None:
                    arrows.append(node.get_right_arrow())

        tree.shift(-subtree.get_center())
        tree.shift(manim.DOWN * 0.5)

        self.play(manim.Create(subtree))
        
        return subtree
    
    def _play_except_subtree(self, tree: BTree, subtree: BNode) -> manim.VGroup:
        """
        Play the tree except the subtree rooted at `subtree`, using DFS.

        Arguments:
            tree: The tree to play.
            subtree: The subtree to exclude.

        Returns:
            vgroup: The VGroup of nodes of the tree.
        """
        # DFS
        vgroup = manim.VGroup()
        stack = [tree.root]
        while stack:
            node = stack.pop()

            if node == subtree:
                continue

            vgroup.add(node.get_circle())
            vgroup.add(node.get_mobject())

            if node.right is not None:
                vgroup.add(node.get_right_arrow())
                stack.append(node.right)
            if node.left is not None:
                vgroup.add(node.get_left_arrow())
                stack.append(node.left)

        self.play(manim.FadeIn(vgroup))
        
        return vgroup

class dp_02_02(manim.Scene):
    def construct(self):
        config = {
            "font_size": 28,
        }

        # Initialize fib(5)
        tree = BTree(
            build_fib_tree(5),
            hbuff=1,
            vbuff=1.2,
            element_to_mobject=manim.MathTex,
            element_to_mobject_config=config,
            circle_buffer_factor=1.2,
        )

        # Adjust position of the tree
        vgroup = manim.VGroup()
        node = tree.root
        while node is not None:
            vgroup.add(node.get_mobject())
            vgroup.add(node.get_circle())
            node = node.left
        vgroup.add(tree.root.right.get_mobject())
        vgroup.add(tree.root.right.get_circle())
        tree.shift(-vgroup.get_center())
        tree.shift(manim.DOWN * 0.5)

        # Show nodes by dfs, color repeated nodes, with a dp[n] node blow
        for v in self._play_dfs_memoized(tree):
            vgroup.add(v)

        # Show O(n)
        label = manim.MathTex(r"n \implies \text{No. of nodes} = O(n)")
        label.next_to(vgroup, manim.UP * 2)
        self.play(manim.Write(label))
        self.wait(3)
        time_label = manim.MathTex(r"\text{Time complexity} = O(n)")
        time_label.next_to(vgroup, manim.UP * 2)
        self.play(manim.Transform(label, time_label))
        self.wait(3)
        self.play(manim.Unwrite(label))

        self.play(manim.FadeOut(vgroup))
        self.wait()

    def _play_dfs_memoized(self, tree: BTree) -> Generator[manim.VGroup, None, None]:
        """
        Play the tree by DFS, color repeated nodes, with a dp[n] node blow.

        Arguments:
            tree: The tree.
        """
        encountered = set()
        parent_arrow = {}
        for node in BTree.dfs(tree.root):
            if node != tree.root and node not in parent_arrow:
                continue

            # Add nodes and arrows
            vgroup = manim.VGroup()
            if node != tree.root:
                vgroup.add(parent_arrow[node])
            vgroup.add(node.get_circle())
            vgroup.add(node.get_mobject())

            # Color repeated nodes
            if node.label in encountered:
                node.get_mobject().set_color(manim.YELLOW) # type: ignore
                node.get_circle().set_color(manim.YELLOW) # type: ignore

            self.play(manim.Create(vgroup))
            yield vgroup

            # Add dp[n] node
            if node.label in encountered:
                dp_n = manim.VGroup()

                # Node
                label = tree.element_to_mobject(r"\text{dp}[", f"{node.label[2:-1]}", r"]", **tree.element_to_mobject_config)
                label.move_to(node.get_mobject().get_center() + manim.DOWN * tree.vbuff)

                # Rectangle
                rect = manim.SurroundingRectangle(label)
                rect.set_color(manim.WHITE)

                # Arrow
                arrow = manim.Line(
                    node.get_circle().get_bottom(),
                    rect.get_center() + manim.UP * rect.height / 2,
                    stroke_width=4,
                )
                arrow.add_tip(
                    tip_shape=manim.ArrowTriangleFilledTip,
                    tip_length=0.2,
                    tip_width=0.2,
                    at_start=False,
                )

                dp_n.add(arrow)
                dp_n.add(rect)
                dp_n.add(label)

                self.play(manim.Create(dp_n))
                yield dp_n

                continue

            # Else add to encountered
            encountered.add(node.label)
        
            if node.left is not None:
                parent_arrow[node.left] = node.get_left_arrow()
            if node.right is not None:
                parent_arrow[node.right] = node.get_right_arrow()

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
