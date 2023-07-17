from __future__ import annotations
from typing import Optional, Callable, Dict, Any, Generator, List
import numpy as np
import manim


class BNode(manim.VMobject):
    def __init__(
        self,
        label: str,
        left: Optional[BNode] = None,
        right: Optional[BNode] = None,
    ):
        self.label = label
        self.left = left
        self.right = right
        self.mobject: Optional[manim.VMobject] = None
        self.circle: Optional[manim.Circle] = None
        self.left_arrow: Optional[manim.Line] = None
        self.right_arrow: Optional[manim.Line] = None

    def get_mobject(self) -> manim.VMobject:
        if self.mobject is None:
            raise ValueError("mobject is None")
        return self.mobject

    def get_circle(self) -> manim.Circle:
        if self.circle is None:
            raise ValueError("circle is None")
        return self.circle

    def get_left_arrow(self) -> manim.Line:
        if self.left_arrow is None:
            raise ValueError("left_arrow is None")
        return self.left_arrow

    def get_right_arrow(self) -> manim.Line:
        if self.right_arrow is None:
            raise ValueError("right_arrow is None")
        return self.right_arrow


class BTree(manim.VGroup):
    """
    Binary tree mobject.
    Its use is to initialize all the nodes and arrows.

    It initializes the depth and breadth of the tree,
    and assign the mobjects to each BNodes associated with this tree.

    You can either play this object directly, or play each node separately.
    """

    def __init__(
        self,
        root: BNode,
        vbuff: float = 1,
        hbuff: float = 1,
        element_to_mobject: Callable[..., manim.VMobject] = manim.Paragraph,  # first arg is str, remaining is config
        element_to_mobject_config: Dict[str, Any] = {},
        circle_config: Dict[str, Any] = {},
        circle_buffer_factor: float = 2,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.root = root
        self.vbuff = vbuff
        self.hbuff = hbuff
        self.element_to_mobject = element_to_mobject
        self.element_to_mobject_config = element_to_mobject_config

        self.circle_config = circle_config
        if "color" not in self.circle_config:
            self.circle_config["color"] = manim.WHITE # type: ignore
        
        self.circle_buffer_factor = circle_buffer_factor
        
        self.nodes = manim.VGroup()
        self.circles = manim.VGroup()
        self.arrows = manim.VGroup()
        self.tree_depth: int = BTree._compute_depth(self.root)
        self.tree_breadth: int = 2 ** (self.tree_depth - 1)
        self.grid = manim.VGroup()

        self.setup()

    def setup(self):
        """
        Setup the tree.
        """
        # Add nodes
        self._add_node_mobject(self.root, None, self.tree_breadth)
        self._add_arrow_mobject(self.root)
        self.add(self.circles, self.nodes, self.arrows)

        self.center()
    
    def set_hbuff(self, hbuff: float):
        """
        Set the horizontal buffer of the tree.

        Arguments:
            hbuff: The horizontal buffer.
        """
        self.hbuff = hbuff
        self.setup()
    
    def set_vbuff(self, vbuff: float):
        """
        Set the vertical buffer of the tree.

        Arguments:
            vbuff: The vertical buffer.
        """
        self.vbuff = vbuff
        self.setup()

    @staticmethod
    def bfs_layer_by_layer(root: BNode) -> Generator[List[BNode], None, None]:
        """
        Breadth-first search the tree, yielding one layer at a time.

        Arguments:
            root: The root node of the tree.
        
        Returns:
            A generator of layers.
        """
        queue = [root]
        while queue:
            layer = []
            for _ in range(len(queue)):
                node = queue.pop(0)
                layer.append(node)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            yield layer

    @staticmethod
    def bfs(root: BNode) -> Generator[BNode, None, None]:
        """
        Breadth-first search the tree, yielding one node at a time,
        left to right.

        Arguments:
            root: The root node of the tree.

        Returns:
            A generator of nodes.
        """
        for layer in BTree.bfs_layer_by_layer(root):
            for node in layer:
                yield node

    @staticmethod
    def dfs(root: BNode) -> Generator[BNode, None, None]:
        """
        Depth-first search the tree, yielding one node at a time,
        left to right.

        Arguments:
            root: The root node of the tree.

        Returns:
            A generator of nodes.
        """
        stack = [root]
        while stack:
            node = stack.pop()
            yield node
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
    
    @staticmethod
    def dfs_right_to_left(root: BNode) -> Generator[BNode, None, None]:
        """
        Depth-first search the tree, yielding one node at a time,
        right to left.

        Arguments:
            root: The root node of the tree.

        Returns:
            A generator of nodes.
        """
        stack = [root]
        while stack:
            node = stack.pop()
            yield node
            if node.left is not None:
                stack.append(node.left)
            if node.right is not None:
                stack.append(node.right)

    def _add_node_mobject(
        self,
        node: Optional[BNode],
        parent: Optional[BNode],
        width: float,
        direction: np.ndarray = manim.RIGHT,
    ):
        """
        Process position of node and add to self.nodes recursively.
        This node will be positioned at the middle of the width,
        and to the specified direction of the parent.

        Arguments:
            node: The node to add.
            parent: The parent node of the node to add.
            width: The width of the subtree to add.
            direction: The direction of the node to add.
        """
        if node is None:
            return

        # Add node
        is_new = node.mobject is None

        if is_new:
            node.mobject = self.element_to_mobject(
                node.label, **self.element_to_mobject_config
            )
        if parent is not None:
            node.get_mobject().move_to(
                parent.get_mobject().get_center()
                + manim.DOWN * self.vbuff
                + direction * (width / 2 * self.hbuff)
            )
        if is_new:
            self.nodes.add(node.get_mobject())

        # Add circle
        if is_new:
            circle = self._get_circle(node.get_mobject())
            node.circle = circle
            self.circles.add(circle)
        else:
            node.get_circle().surround(node.get_mobject(), buffer_factor=self.circle_buffer_factor)

        self._add_node_mobject(node.left, node, width / 2, manim.LEFT)
        self._add_node_mobject(node.right, node, width / 2, manim.RIGHT)

    def _add_arrow_mobject(self, node: Optional[BNode]):
        """
        Add arrow mobjects recursively.

        Arguments:
            node: The node to add arrow mobjects to.
        """
        if node is None:
            return

        # Function to construct arrow
        def get_arrow(start: np.ndarray, end: np.ndarray) -> manim.Line:
            buff = np.sqrt(node.get_mobject().width ** 2 + node.get_mobject().height ** 2) / 2 * self.circle_buffer_factor
            arrow = manim.Line(
                start,
                end,
                stroke_width=4,
                buff=buff,
            )
            add_tip(arrow)
            return arrow

        def add_tip(arrow: manim.Line):
            arrow.add_tip(
                tip_shape=manim.ArrowTriangleFilledTip,
                tip_length=0.2,
                tip_width=0.2,
                at_start=False,
            )

        # Add left arrow
        if node.left is not None:
            start = node.get_circle().get_center()
            end = node.left.get_circle().get_center()
            if node.left_arrow is None:
                arrow = get_arrow(start, end)
                node.left_arrow = arrow
                self.arrows.add(arrow)
            else:
                node.left_arrow.put_start_and_end_on(start, end) # type: ignore
                node.left_arrow.pop_tips()
                add_tip(node.left_arrow)

        # Add right arrow
        if node.right is not None:
            start = node.get_circle().get_center()
            end = node.right.get_circle().get_center()
            if node.right_arrow is None:
                arrow = get_arrow(start, end)
                node.right_arrow = arrow
                self.arrows.add(arrow)
            else:
                node.right_arrow.put_start_and_end_on(start, end) # type: ignore
                node.right_arrow.pop_tips()
                add_tip(node.right_arrow)

        self._add_arrow_mobject(node.left)
        self._add_arrow_mobject(node.right)

    def _get_circle(self, node: manim.VMobject) -> manim.Circle:
        """
        Get the circle surrounding the node.

        Arguments:
            node: The node mobject.

        Returns:
            The circle mobject.
        """
        circle = manim.Circle(**self.circle_config)
        circle.surround(node, buffer_factor=self.circle_buffer_factor)
        return circle

    @staticmethod
    def _compute_depth(root: BNode) -> int:
        """
        Compute the depth of the tree using BFS.

        Arguments:
            root: The root of the tree.

        Returns:
            The depth of the tree.
        """
        depth = 0
        for _ in BTree.bfs_layer_by_layer(root):
            depth += 1
        return depth
