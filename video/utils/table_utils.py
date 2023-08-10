from typing import Sequence
import manim


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
