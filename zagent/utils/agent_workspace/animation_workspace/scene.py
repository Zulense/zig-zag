# The videos are meant to be in vertical format (1080*1920, portrait orientation).
# Manually set the frame size, height, and width to ensure the scene is rendered correctly.
# Note: Now the scene measures 8 units in width and 14 units in height (9:16 ratio).

from manim import *
import random
import math
import numpy as np
import itertools

config.frame_size = [1080, 1920]
config.frame_height = 14
config.frame_width = 8

class SelfAttentionScene(Scene):
    def construct(self):
        # --- Concept Caption Bar ---
        caption_rect = Rectangle(
            width=config.frame_width,
            height=1.5,
            fill_opacity=0.7,
            fill_color=BLACK,
            stroke_width=0
        ).to_edge(DOWN, buff=0)
        caption_text = Text("Understanding Self-Attention", color=WHITE, font_size=32).move_to(caption_rect.get_center())
        concept_caption = VGroup(caption_rect, caption_text)

        def update_caption(new_text):
            nonlocal caption_text
            new_caption_text = Text(new_text, color=WHITE, font_size=32).move_to(caption_rect.get_center())
            self.play(Transform(caption_text, new_caption_text))
            caption_text = new_caption_text # Update the reference

        self.add(concept_caption)

        # Scene 0: Opening Frame
        series_header = Text("Part 4/5: Attention Is All You Need", font_size=24, color=GRAY).to_edge(UP)
        hook_text = Text(
            "Self-Attention: Unlocking Context in AI Models",
            font_size=48,
            weight=BOLD,
            line_spacing=1.5,
            text_align="center"
        ).move_to(ORIGIN)

        self.play(FadeIn(series_header), Write(hook_text))
        self.wait(2)
        self.play(FadeOut(hook_text))

        # Scene 1: Unraveling Context Clues
        sentence_str = "The animal didn't cross the street because it was too wide."
        sentence = Text(sentence_str, font_size=40).move_to(ORIGIN)
        it_word = VGroup(*[Text(w, font_size=40) for w in sentence_str.split()]).arrange(RIGHT, buff=0.1)
        it_word_index = 8 # Index of 'it'
        
        # Manually adjust positions to match the original sentence's layout
        # This is crucial for accurate highlighting without get_parts_by_text
        current_x = sentence.get_left()[0]
        for i, word_mobject in enumerate(it_word):
            if i > 0:
                current_x += it_word[i-1].width + 0.1 # Add buffer
            word_mobject.move_to([current_x + word_mobject.width / 2, sentence.get_center()[1], 0])
            
        it_mobject = it_word[it_word_index]
        it_mobject.set_color(RED)
        
        self.play(Write(sentence))
        self.wait(1)
        self.play(ReplacementTransform(sentence, it_word))
        self.wait(0.5)
        
        question_mark = Text("?", font_size=60, color=YELLOW).next_to(it_mobject, RIGHT, buff=0.2)
        self.play(FadeIn(question_mark))

        animal_mobject = it_word[1] # 'animal'
        street_mobject = it_word[6] # 'street'

        arrow_it_animal = Arrow(it_mobject.get_center(), animal_mobject.get_center(), buff=0.1, color=GRAY, max_stroke_width_to_length_ratio=0.05, stroke_width=3, tip_length=0.2)
        arrow_it_street = Arrow(it_mobject.get_center(), street_mobject.get_center(), buff=0.1, color=GRAY, max_stroke_width_to_length_ratio=0.05, stroke_width=3, tip_length=0.2)
        
        self.play(GrowArrow(arrow_it_animal), GrowArrow(arrow_it_street))
        self.wait(2)
        
        # Scene 2: Elements in Sequence
        self.play(FadeOut(question_mark), FadeOut(arrow_it_animal), FadeOut(arrow_it_street), FadeOut(series_header))
        
        update_caption("Representing words as individual elements")
        
        word_blocks = VGroup()
        for i, word in enumerate(sentence_str.split()):
            block_text = Text(word, font_size=32, color=BLACK)
            block_rect = Rectangle(width=block_text.width + 0.5, height=1.0, color=GRAY, fill_color=GRAY, fill_opacity=0.3)
            block = VGroup(block_rect, block_text)
            word_blocks.add(block)
            
        word_blocks.arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        # Adjust position for vertical screen
        word_blocks.move_to(UP * 2)

        self.play(
            FadeOut(it_word),
            LaggedStart(*[FadeIn(block) for block in word_blocks], lag_ratio=0.1)
        )
        self.wait(2)

        # Scene 3: Attention Within Itself
        update_caption("Each element attends to all others")

        # Find the 'it' block
        it_block_index = sentence_str.split().index("it")
        it_word_block = word_blocks[it_block_index]

        self.play(
            it_word_block[0].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            it_word_block.animate.scale(1.1)
        )
        self.wait(0.5)

        attention_lines_to_all = VGroup()
        for i, block in enumerate(word_blocks):
            if i != it_block_index:
                line = Line(it_word_block.get_center(), block.get_center(), color=PURPLE, stroke_width=2)
                attention_lines_to_all.add(line)

        self.play(Create(attention_lines_to_all))
        self.wait(2)

        # Scene 4: Asking for Relationships
        update_caption("Querying for relationships within the sequence")

        query_text = Text("Query", font_size=24, color=BLUE)
        query_dot = Dot(color=BLUE, radius=0.15)
        query_group = VGroup(query_dot, query_text).next_to(it_word_block, UP)

        self.play(FadeIn(query_group))

        for i, block in enumerate(word_blocks):
            if i != it_block_index:
                key_text = Text("Key", font_size=24, color=ORANGE)
                key_dot = Dot(color=ORANGE, radius=0.15)
                key_group = VGroup(key_dot, key_text).next_to(block, UP)

                # Animate query moving to target block
                self.play(
                    query_dot.animate.move_to(block.get_center()),
                    FadeIn(key_group), # Key appears at target
                    run_time=0.8
                )
                self.play(FadeOut(key_group), query_dot.animate.move_to(query_group.get_center()), run_time=0.4) # Key fades, query returns

        self.play(FadeOut(query_group))
        
        # Clean up existing lines before re-animating in Scene 5
        self.play(FadeOut(attention_lines_to_all))

        # Scene 5: Resolving Ambiguity
        update_caption("Self-attention resolves ambiguous references")

        animal_block_index = sentence_str.split().index("animal") # 1
        street_block_index = sentence_str.split().index("street") # 6

        it_to_street_line = Line(it_word_block.get_center(), word_blocks[street_block_index].get_center(), color=PURPLE, stroke_width=2)
        it_to_animal_line = Line(it_word_block.get_center(), word_blocks[animal_block_index].get_center(), color=PURPLE, stroke_width=2)

        self.play(Create(it_to_street_line), Create(it_to_animal_line))
        self.wait(0.5)

        self.play(
            it_to_street_line.animate.set_stroke(width=6, color=PURPLE_A),
            it_to_animal_line.animate.set_stroke(width=2, color=GRAY)
        )
        self.wait(2)

        # Scene 6: Weighted Context
        update_caption("Attention weights prioritize relevant context")

        # Intensify street line, highlight street block
        street_block = word_blocks[street_block_index]
        self.play(
            it_to_street_line.animate.set_stroke(width=8, color=PURPLE_E),
            street_block[0].animate.set_color(GREEN).set_fill(GREEN, opacity=0.8),
            street_block.animate.scale(1.1),
            run_time=1
        )

        weight_street = MathTex("0.8", font_size=30, color=WHITE).next_to(it_to_street_line, UP, buff=0.1)
        weight_animal = MathTex("0.2", font_size=30, color=WHITE).next_to(it_to_animal_line, DOWN, buff=0.1)

        self.play(Write(weight_street), Write(weight_animal))
        self.wait(2)

        # Clear everything for the next scene
        self.play(*[FadeOut(m) for m in self.mobjects if m != caption_rect and m != caption_text])

        # Scene 7: The Challenge of Distance
        update_caption("Older models struggled with long-range dependencies")

        long_sentence_str = "This is a very long sentence to illustrate the challenge of long-range dependencies."
        long_words = long_sentence_str.split()
        word_blocks_long = VGroup()
        for i, word in enumerate(long_words):
            block_text = Text(word, font_size=24, color=BLACK)
            block_rect = Rectangle(width=block_text.width + 0.4, height=0.8, color=GRAY, fill_color=GRAY, fill_opacity=0.3)
            block = VGroup(block_rect, block_text)
            word_blocks_long.add(block)

        word_blocks_long.arrange(RIGHT, buff=0.15).scale(0.8)
        word_blocks_long.move_to(UP * 3)
        
        self.play(FadeIn(word_blocks_long))

        # Highlight two distant blocks
        source_block = word_blocks_long[0] # 'This'
        target_block = word_blocks_long[-2] # 'dependencies'
        
        self.play(
            source_block[0].animate.set_color(BLUE).set_fill(BLUE, opacity=0.8),
            target_block[0].animate.set_color(ORANGE).set_fill(ORANGE, opacity=0.8),
        )
        self.wait(0.5)

        # ConvS2S line (Linear)
        conv_path_points = [source_block.get_center()] + [
            word_blocks_long[i].get_center() for i in range(1, len(long_words) - 2)
        ] + [target_block.get_center()]
        conv_line = VMobject()
        conv_line.set_points_as_corners(conv_path_points)
        conv_line.set_stroke(color=GRAY, width=3, opacity=0.7)
        conv_line.make_smooth()
        conv_line.insert_n_curves(100) # For smooth animation over a curve
        conv_line_dashed = DashedLine(conv_line.get_start(), conv_line.get_end(), color=GRAY, dash_length=0.1).add_tip(tip_length=0.2)
        conv_line_dashed.set_points_as_corners(conv_path_points) # Apply same points as curve
        conv_line_dashed.make_smooth()

        conv_text = Text("Linear (ConvS2S)", font_size=28, color=GRAY).next_to(word_blocks_long, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Create(conv_line_dashed), Write(conv_text))
        self.wait(1.5)
        
        # ByteNet line (Logarithmic)
        # Simplified path for ByteNet to show fewer intermediate steps
        bytenet_path_points = [
            source_block.get_center(),
            word_blocks_long[len(long_words)//3].get_center(),
            word_blocks_long[2*len(long_words)//3].get_center(),
            target_block.get_center()
        ]
        bytenet_line = VMobject()
        bytenet_line.set_points_as_corners(bytenet_path_points)
        bytenet_line.set_stroke(color=GRAY, width=3, opacity=0.7)
        bytenet_line.make_smooth()
        bytenet_line.insert_n_curves(100)
        bytenet_line_dashed = DashedLine(bytenet_line.get_start(), bytenet_line.get_end(), color=GRAY, dash_length=0.1).add_tip(tip_length=0.2)
        bytenet_line_dashed.set_points_as_corners(bytenet_path_points)
        bytenet_line_dashed.make_smooth()

        bytenet_text = Text("Logarithmic (ByteNet)", font_size=28, color=GRAY).next_to(conv_text, DOWN, buff=0.3)
        self.play(Create(bytenet_line_dashed), Write(bytenet_text))
        self.wait(2)

        # Scene 8: Constant Operations
        update_caption("Self-attention resolves distant relationships directly")

        self.play(FadeOut(conv_line_dashed), FadeOut(conv_text), FadeOut(bytenet_line_dashed), FadeOut(bytenet_text))

        # Straight line for Self-Attention
        self_attention_line = Line(source_block.get_center(), target_block.get_center(), color=PURPLE_A, stroke_width=6)
        self_attention_text = Text("Constant (Self-Attention)", font_size=28, color=PURPLE_A).next_to(word_blocks_long, DOWN, buff=0.5).to_edge(LEFT)

        self.play(Create(self_attention_line), Write(self_attention_text))
        self.wait(2)

        # Scene 9: Parallel Efficiency
        update_caption("Self-attention enables parallel computation")
        
        # Clear previous lines/text, reset block colors
        self.play(
            FadeOut(self_attention_line), FadeOut(self_attention_text),
            *[block[0].animate.set_color(GRAY).set_fill(GRAY, opacity=0.3) for block in word_blocks_long]
        )

        all_attention_lines = VGroup()
        for i, source_block in enumerate(word_blocks_long):
            for j, target_block in enumerate(word_blocks_long):
                if i != j:
                    line = Line(source_block.get_center(), target_block.get_center(), color=PURPLE, stroke_width=1.5, opacity=0.6)
                    all_attention_lines.add(line)
        
        self.play(Create(all_attention_lines))
        self.wait(2)

        # Scene 10: The Transformer's Core
        update_caption("The Transformer relies entirely on self-attention")
        
        self.play(
            word_blocks_long.animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(UP*1.5),
            all_attention_lines.animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(UP*1.5),
            *[block[0].animate.set_fill(WHITE, opacity=0) for block in word_blocks_long] # Make blocks subtle for context
        )
        
        transformer_label = Text("Transformer", font_size=48, weight=BOLD, color=BLUE_C)
        transformer_block = Rectangle(width=4, height=3, color=BLUE_C, fill_color=BLUE_D, fill_opacity=0.6)
        transformer_group = VGroup(transformer_block, transformer_label).next_to(word_blocks_long, RIGHT, buff=1.0).shift(DOWN*0.5)
        
        self.play(FadeIn(transformer_group))
        
        input_arrow = Arrow(
            all_attention_lines.get_right(),
            transformer_block.get_left(),
            color=GREEN_C,
            stroke_width=6,
            buff=0.1
        )
        self.play(GrowArrow(input_arrow))
        self.play(Indicate(transformer_block, scale_factor=1.1, color=GREEN_C))
        self.wait(2)

        # Scene 11: Fueling Large Language Models
        update_caption("Self-attention is key to modern Large Language Models")

        llm_text = Text("LLM", font_size=48, weight=BOLD, color=GOLD_C)
        llm_bubble = Circle(radius=1.8, color=GOLD_C, fill_color=GOLD_D, fill_opacity=0.6)
        llm_group = VGroup(llm_bubble, llm_text).next_to(transformer_group, RIGHT, buff=1.0)

        self.play(
            transformer_group.animate.shift(LEFT*1.0),
            input_arrow.animate.shift(LEFT*1.0),
            FadeIn(llm_group)
        )

        llm_arrow = Arrow(
            transformer_block.get_right(),
            llm_bubble.get_left(),
            color=GREEN_C,
            stroke_width=6,
            buff=0.1
        )

        self.play(GrowArrow(llm_arrow))

        gpt_text = Text("GPT", font_size=24, color=GRAY).next_to(llm_bubble, UP+LEFT, buff=0.2)
        bard_text = Text("Bard", font_size=24, color=GRAY).next_to(llm_bubble, UP+RIGHT, buff=0.2)
        llama_text = Text("Llama", font_size=24, color=GRAY).next_to(llm_bubble, DOWN, buff=0.2)

        self.play(FadeIn(gpt_text), FadeIn(bard_text), FadeIn(llama_text))
        self.wait(2)

        # Scene 12: Self-Attention's Legacy
        update_caption("Self-attention's profound impact on AI")

        self.play(*[FadeOut(m) for m in self.mobjects if m != caption_rect and m != caption_text])

        # Recreate the original sentence blocks for this summary scene
        sentence_str = "The animal didn't cross the street because it was too wide."
        word_blocks_summary = VGroup()
        for i, word in enumerate(sentence_str.split()):
            block_text = Text(word, font_size=32, color=BLACK)
            block_rect = Rectangle(width=block_text.width + 0.5, height=1.0, color=GRAY, fill_color=GRAY, fill_opacity=0.3)
            block = VGroup(block_rect, block_text)
            word_blocks_summary.add(block)
            
        word_blocks_summary.arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        word_blocks_summary.move_to(UP * 2)
        self.play(FadeIn(word_blocks_summary))

        # Draw all connections
        all_connections_summary = VGroup()
        for i, source_block in enumerate(word_blocks_summary):
            for j, target_block in enumerate(word_blocks_summary):
                if i != j:
                    line = Line(source_block.get_center(), target_block.get_center(), color=PURPLE, stroke_width=1.0, opacity=0.5)
                    all_connections_summary.add(line)
        self.play(Create(all_connections_summary))

        # Highlight 'it' to 'street' again
        it_block_summary_index = sentence_str.split().index("it")
        street_block_summary_index = sentence_str.split().index("street")
        it_block_summary = word_blocks_summary[it_block_summary_index]
        street_block_summary = word_blocks_summary[street_block_summary_index]

        # Find the specific line to animate its color and width
        # Iterate through all_connections_summary to find the correct line
        # For clarity, let's just create a new one to highlight.
        temp_highlight_line = Line(it_block_summary.get_center(), street_block_summary.get_center(), color=PURPLE_A, stroke_width=4, opacity=1)
        self.play(Create(temp_highlight_line), run_time=0.5)
        self.play(FadeOut(temp_highlight_line), run_time=0.5)
        
        # Key Takeaways
        takeaway1 = Text("• Relates within sequence", font_size=30, color=WHITE).next_to(word_blocks_summary, DOWN, buff=1.0).to_edge(LEFT, buff=0.5)
        takeaway2 = Text("• Efficient long-range dependencies", font_size=30, color=WHITE).next_to(takeaway1, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        takeaway3 = Text("• Constant operations", font_size=30, color=WHITE).next_to(takeaway2, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)

        self.play(FadeIn(takeaway1), FadeIn(takeaway2), FadeIn(takeaway3))
        self.wait(3)

        # Final Scene: Closing & Preview
        self.play(*[FadeOut(m) for m in self.mobjects if m != caption_rect and m != caption_text])

        update_caption("Summary & Next Topic")

        summary_title = Text("Key Takeaways:", font_size=40, weight=BOLD).to_edge(UP, buff=1.0)
        summary_items = VGroup(
            Text("1. Self-attention relates elements within a single sequence.", font_size=32, line_spacing=1.2),
            Text("2. It efficiently handles long-range dependencies.", font_size=32, line_spacing=1.2),
            Text("3. Operations for distant elements become constant.", font_size=32, line_spacing=1.2),
            Text("4. Core of the Transformer architecture and LLMs.", font_size=32, line_spacing=1.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(summary_title, DOWN, buff=1.0).to_edge(LEFT, buff=0.5)

        self.play(FadeIn(summary_title), LaggedStart(*[Write(item) for item in summary_items], lag_ratio=0.3))
        self.wait(3)

        coming_next_title = Text("Coming Next:", font_size=36, weight=BOLD, color=YELLOW).to_edge(DOWN, buff=3.0)
        next_topic_text = Text("Next: Encoder-Decoder Model Structure", font_size=32, color=WHITE).next_to(coming_next_title, DOWN, buff=0.3)
        next_topic_teaser = Text("How AI models process input and generate output.", font_size=28, color=GRAY).next_to(next_topic_text, DOWN, buff=0.2)

        self.play(FadeIn(coming_next_title), Write(next_topic_text), Write(next_topic_teaser))
        self.wait(4)

        self.play(FadeOut(coming_next_title), FadeOut(next_topic_text), FadeOut(next_topic_teaser), FadeOut(caption_rect), FadeOut(caption_text))
        self.wait(1)

