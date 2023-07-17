from ...utils.linked_list import LinkedList
from manim import *


class Visualization(Scene):
    def construct(self):
        # array
        array = IntegerTable(
            [[7, 3, 5, 5, 6, 0, 8]],
            include_outer_lines=True,
            v_buff=0.6,
            h_buff=1,
        )
        array.to_edge(UP, buff=2.4)

        array_label = Text('Array')
        array_label.scale(0.8)
        array_label.next_to(array, UP)

        # linked list
        linked_list = LinkedList(
            ['7', '3', '5', '5', '6', '0', '8'],
            element_to_mobject=MathTex,
            buff=5,
            circle_buffer_factor=2.4,
        )
        linked_list.to_edge(DOWN, buff=1.8)

        linked_list_label = Text('Linked List')
        linked_list_label.scale(0.8)
        linked_list_label.next_to(linked_list, UP * 1.6)

        # play
        self.play(FadeIn(array))
        self.play(Write(array_label))
        self.wait()
        self.play(FadeIn(linked_list))
        self.play(Write(linked_list_label))
        self.wait(duration=2)
        self.play(Unwrite(array_label), Unwrite(linked_list_label))

        # traverse
        array_indexer = Rectangle(
            width=array.get_cell((1, 1)).get_width(),
            height=array.get_cell((1, 1)).get_height(),
            stroke_color=GREEN,
        ).move_to(array.get_cell((1, 1)).get_center())

        array_arrow = Arrow(
            tip_length=0.2,
            color=GREEN,
        )
        array_arrow.put_start_and_end_on(
            array.get_cell((1, 1)).get_top() + UP,
            array.get_cell((1, 1)).get_top() + UP * 0.2,
        )

        linked_list_arrow = Arrow(
            tip_length=0.2,
            color=GREEN,
        )
        linked_list_arrow.put_start_and_end_on(
            linked_list.circles[0].get_top() + UP,
            linked_list.circles[0].get_top() + UP * 0.2,
        )

        self.play(
            # array
            FadeIn(array_indexer),
            FadeIn(array_arrow),

            # linked list
            linked_list.circles[0].animate.set_stroke_color(GREEN),
            FadeIn(linked_list_arrow),

            run_time=0.5,
        )

        self.wait()

        self.play(
            # array
            array[0][0].animate.set_color(YELLOW),
            # linked list
            linked_list.nodes[0].animate.set_color(YELLOW),

            run_time=0.5,
        )

        for i in range(1, len(linked_list.nodes)):
            # finish
            self.play(
                # array

                # linked list
                linked_list.circles[i - 1].animate.set_stroke_color(WHITE),
                FadeOut(linked_list_arrow),

                run_time=0.5,
            )

            # transition
            self.play(AnimationGroup(
                Succession(
                    FadeToColor(linked_list.arrows[i - 1], GREEN),
                    FadeToColor(linked_list.arrows[i - 1], WHITE),
                ),
                AnimationGroup(
                    array_indexer.animate.move_to(array.get_cell((1, i + 1)).get_center()),
                    array_arrow.animate.put_start_and_end_on(
                        array.get_cell((1, i + 1)).get_top() + UP,
                        array.get_cell((1, i + 1)).get_top() + UP * 0.2,
                    ),
                    run_time=1,
                ),
                run_time=1,
            ))

            # start            
            linked_list_arrow.put_start_and_end_on(
                linked_list.circles[i].get_top() + UP,
                linked_list.circles[i].get_top() + UP * 0.2,
            )

            self.play(
                # array
                array[0][i].animate.set_color(YELLOW),

                # linked list
                linked_list.nodes[i].animate.set_color(YELLOW),
                linked_list.circles[i].animate.set_stroke_color(GREEN),
                FadeIn(linked_list_arrow),

                run_time=0.5,
            )

            self.wait(duration=0.25)

        # finish
        self.play(
            # array
            FadeOut(array_indexer),
            FadeOut(array_arrow),

            # linked list
            linked_list.circles[-1].animate.set_stroke_color(WHITE),
            FadeOut(linked_list_arrow),

            run_time=0.5,
        )
        self.wait(duration=2)

        # iterator
        width = linked_list.get_width() + 0.5
        height = array.get_height() + 0.8

        # linked list
        ll_iter_label = Text('Iterator')
        ll_iter_label.scale(2)
        ll_iter_label.move_to(array)
        ll_iter_box = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=1,
        )
        ll_iter_box.move_to(ll_iter_label)

        # array
        array_iter_label = Text('Iterator')
        array_iter_label.scale(2)
        array_iter_label.move_to(linked_list)
        array_iter_box = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=1,
        )
        array_iter_box.move_to(array_iter_label)

        self.play(AnimationGroup(
            AnimationGroup(
                Write(ll_iter_box),
                Write(array_iter_box),
            ),
            AnimationGroup(
                Write(ll_iter_label),
                Write(array_iter_label),
            ),
            lag_ratio=0.5,
            run_time=1.5,
        ))
        self.remove(linked_list, array)
        self.remove(*linked_list.nodes, *linked_list.circles, *linked_list.arrows)
        self.wait()

        # iter
        iter_label = Text('Iterator')
        iter_label.scale(2)
        iter_box = Rectangle(
            width=width,
            height=height,
            stroke_color=WHITE,
        )
        iter_box.move_to(iter_label)
        iter = Group(iter_label, iter_box)

        self.play(
            ll_iter_box.animate.move_to(iter_box),
            ll_iter_label.animate.move_to(iter_label),
            array_iter_box.animate.move_to(iter_box),
            array_iter_label.animate.move_to(iter_label),
        )
        self.remove(ll_iter_box, ll_iter_label, array_iter_box, array_iter_label)
        self.add(iter)
        self.wait(duration=2)

        new_iter_label = Text('Iterator')
        new_iter_box = Rectangle(
            width=width * 0.3,
            height=height * 1.6,
            stroke_color=WHITE,
        )
        new_iter_box.move_to(new_iter_label)
        new_iter = Group(new_iter_label, new_iter_box)
        new_iter.to_edge(LEFT, buff=2)

        self.play(
            ReplacementTransform(iter, new_iter),
        )

        # operations
        next_label = Text('next()', font='JetBrains Mono', font_size=28)
        next_label.next_to(new_iter_box, RIGHT * 1.5)
        next_label.shift(DOWN * new_iter_box.get_height() * 0.25)
        next_imply = MathTex(r'\implies')
        next_imply.next_to(next_label, RIGHT * 1.5)

        has_next_label = Text('has_next()', font='JetBrains Mono', font_size=28)
        has_next_label.next_to(new_iter_box, RIGHT * 1.5)
        has_next_label.shift(UP * new_iter_box.get_height() * 0.25)
        has_next_imply = MathTex(r'\implies')
        has_next_imply.next_to(has_next_label, RIGHT * 1.5)

        self.play(AnimationGroup(
            AnimationGroup(
                Write(next_label),
                FadeIn(next_imply, shift=RIGHT),
                lag_ratio=0.2,
                run_time=1.2,
            ),
            AnimationGroup(
                Write(has_next_label),
                FadeIn(has_next_imply, shift=RIGHT),
                lag_ratio=0.2,
                run_time=1.2,
            ),
            lag_ratio=0.2,
            run_time=1.44,
        ))
        self.wait(duration=2)

        # traverse
        has_next_true = Tex('True')
        has_next_true.next_to(has_next_imply, RIGHT * 1.5)
        has_next_true.set_color(GREEN)
        has_next_false = Tex('False')
        has_next_false.next_to(has_next_imply, RIGHT * 1.5)
        has_next_false.set_color(RED)

        next_results = [MathTex(f'{i}') for i in [7, 3, 5, 5, 6, 0, 8]]
        next_results[0].next_to(next_imply, RIGHT * 1.2)
        for i in range(1, len(next_results)):
            next_results[i].next_to(next_results[i - 1], RIGHT * 1.5)

        self.play(FadeIn(has_next_true, shift=RIGHT))

        for i, mobj in enumerate(next_results):
            self.play(AnimationGroup(
                FadeIn(mobj, shift=RIGHT),
                Indicate(next_label),
                *([ReplacementTransform(has_next_true, has_next_false)] if i == len(next_results) - 1 else []),
                lag_ratio=0.2,
                run_time=1.2  if i != len(next_results) - 1 else 1.4,
            ))

            self.wait(0.2)
        self.wait(duration=4)
