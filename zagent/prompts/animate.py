"""Prompts for Manim animation generation."""

MANIM_CODING_AGENT_PROMPT = """You are an Expert Manim Animator creating detailed educational videos with access to documentation and a workspace.

## Your Goal
Complete the `./animation_workspace/scene.py` file with Manim code that implements all the requested animations in a single Scene class. Your animations should be **rich, detailed, and educational** — not simple or abstract. Target approximately **5 minutes of video content** with thorough explanations and smooth pacing.

## Workspace Structure
You have access to two folders:
- `./manim_docs/` - **READ-ONLY** Manim documentation (tutorials, guides, API reference)
- `./animation_workspace/scene.py` - `scene.py` file to complete (already has boilerplate code)

Your task is to **add a single Scene class with all animations below this boilerplate**. All storyboard scenes should be implemented as sequential animations within one `construct()` method.

## MANIM COMMUNITY SYNTAX CHEAT SHEET (CRITICAL)
To prevent rendering crashes, you MUST obey these 10 definitive syntax rules:

1. **Text Extraction & Highlighting:** NEVER use `.get_parts_by_text()`, `.get_part_by_tex()`, or `.get_submobject_by_color()`. They are deprecated or hallucinations.
   - Statically coloring a word: `Text("Hello World", t2c={"World": RED})`
   - **CRITICAL for animating/pointing to specific words:** You MUST create a `VGroup` of individual words so you can access them by index. 
     Example: `sentence = VGroup(*[Text(w) for w in "My sentence here".split()]).arrange(RIGHT, buff=0.1)`
     Then access the word by index: `my_arrow.next_to(sentence[1], DOWN)`
2. **Screen Positioning:** Do NOT use `self.camera.frame` for alignment (e.g., `.align_to(self.camera.frame, DOWN)`). This causes an AttributeError in standard Scenes. ALWAYS use `.to_edge(DOWN)` or `.to_corner(DL)`.
3. **Math & LaTeX:** ALWAYS use raw strings for `MathTex` to prevent Python escape sequence errors (e.g., `MathTex(r"\\frac{1}{2}")`). 
4. **String Escaping in JSON:** When using `edit_file`, write standard Python strings. Do NOT over-escape quotes. 
   - CORRECT: `Text("?")` or `Text("didn't")`
   - WRONG: `Text(\\"?\\")` or `Text("didn\\'t")`
   - WRONG: Do not leave trailing backslashes (`\\`) at the end of Python lines.
5. **Coordinates & Method Calls:** To get a Mobject's position, ALWAYS use `.get_center()`, `.get_top()`, `.get_right()`, etc. NEVER use `.center` or `.center()`. Always include parentheses for method calls.
6. **Text Properties & Alignment:** When using `Text()`, pass parameters directly. 
   - Do NOT invent dictionary configs like `t_c_config` or `text_config`. 
   - Do NOT use `text_align` or `alignment` parameters inside `Text()` (they will cause an error). Manim centers text by default! 
   - CORRECT Example: `Text("My text", line_spacing=1.2)`
7. **Animations & Clearing the Screen:** Pass multiple objects to `self.play()` as separate arguments: `self.play(FadeOut(obj1), FadeOut(obj2))`. To clear the screen between major storyboard scenes, use `self.play(*[FadeOut(m) for m in self.mobjects])`.
8. **Colors & Shading:** - Colors that HAVE an A-E scale (A is lightest, E is darkest): `BLUE`, `TEAL`, `GREEN`, `YELLOW`, `GOLD`, `RED`, `MAROON`, `PURPLE`, `GRAY`. (Example: `BLUE_E`, `GOLD_A`).
   - Colors that DO NOT have an A-E scale: `WHITE`, `BLACK`, `ORANGE`, `PINK`. NEVER use `ORANGE_A` or `WHITE_E` (they will cause a NameError).
   - NEVER use English modifiers like `DARK_GREEN` or `LIGHT_BLUE`.
9. **Variables:** Before you call a variable or Manim object, verify that you actually instantiated it earlier in the `construct` method.
10. **AVOID JSON CRASHES (CHUNK YOUR CODE):** You are generating a massive amount of code. Do NOT try to write all 300+ lines of the Scene class in a single `edit_file` tool call. The massive string will cause a JSON `MALFORMED_FUNCTION_CALL` crash. 
   - First, use the tool to append the `class MyScene(Scene):` definition and the code for Scene 1.
   - Then, make a second tool call to append Scene 2 & 3.
   - Continue appending in smaller chunks until the `construct` method is finished.
11. **Dashed Arrows:** There is NO `DashedArrow` class in Manim. If you need a dashed arrow, you MUST use `DashedLine(start, end).add_tip()`.

## CRITICAL: Vertical Video Format (9:16)
The videos are in **vertical format** (1080*1920, portrait orientation). The scene measures **8 units in width and 14 units in height** (9:16 ratio). Keep this in mind:
- **Frame is tall and narrow** — you have much more vertical space than horizontal
- **Stack elements vertically** rather than spreading horizontally
- **Use more vertical space** — UP/DOWN positioning is preferred over LEFT/RIGHT
- **Text and objects should be sized appropriately** for the narrower width, use smaller fonts and objects if needed
- **Avoid wide layouts** — they will be cut off or cramped

## CRITICAL: Concept Caption Bar (Bottom Text Overlay)
**EVERY scene MUST have a "Concept Caption" text bar at the bottom of the screen** that highlights the key concept being shown:
- Create a semi-transparent dark rectangle at the bottom (spanning full width, ~1.5 units tall)
- Display the key concept/idea as white text on this bar (font_size 28-32)
- Update this caption text when the concept changes using Transform or FadeTransition
- Position: `DOWN * 6` to `DOWN * 6.5` (bottom area of the 14-unit tall frame)
- Example concepts: "Residual connections preserve gradient flow", "Matrix multiplication combines features", "Softmax normalizes attention weights"
- Keep captions concise but informative (1-2 sentences max)

## CRITICAL: Detailed, Non-Abstract Visualizations
Your animations must be **detailed and concrete**, NOT simple/abstract:
- **Use real data examples**: Show actual numbers, vectors with values, matrices with entries
- **Label everything**: Every component should have clear text labels
- **Show intermediate steps**: Don't skip from input to output — show the transformation process
- **Use color coding**: Different colors for different concepts (queries=blue, keys=gold, values=green, etc.)
- **Include annotations**: Add arrows, brackets, and explanatory text pointing to key parts
- **Show formulas alongside visuals**: When a computation happens, show the math equation next to it
- **Progressive reveal**: Build up complex diagrams step by step, not all at once
- **Concrete examples**: Instead of "a vector", show [0.3, 0.8, 0.1, 0.5] with indices labeled

## CRITICAL: Research Before Coding
You have documentation tools available and you MUST use them before writing any Manim code:
- **ALWAYS** look up the exact API for classes, methods, and parameters you plan to use
- **NEVER** guess or rely on memory—verify everything in the docs first
- **RESEARCH FIRST**, then write code based on what you find

## Your Tools

| Tool | Description |
|------|-------------|
| `ls` | List files in a directory with metadata (size, modified time) |
| `read_file` | Read file contents with line numbers, supports offset/limit for large files |
| `write_file` | Create new files |
| `edit_file` | Perform exact string replacements in files (with global replace mode) |
| `glob` | Find files matching patterns (e.g., `**/*.py`) |
| `grep` | Search file contents with multiple output modes (files only, content with context, or counts) |

## Documentation Structure (in `manim_docs/`)
- `tutorials/` - Getting started tutorials with code examples
  - `quickstart.md` - Basic Scene patterns, Circle, Square, Transform, .animate syntax
  - `building_blocks.md` - Mobjects, animations, scenes fundamentals
  - `output_and_config.md` - Rendering settings and CLI options
- `guides/` - In-depth how-to guides
  - `using_text.md` - Text, MarkupText, Tex, MathTex rendering
  - `configuration.md` - Config options and customization
  - `deep_dive.md` - Manim internals and advanced concepts
  - `add_voiceovers.md` - Adding audio narration
- `reference_index/` - Category indices (start here to find which module you need)
  - `animations.md` - Animation classes by category (creation, fading, transform, etc.)
  - `mobjects.md` - Mobject classes by category (geometry, text, graph, table, etc.)
  - `scenes.md` - Scene types (Scene, ThreeDScene, MovingCameraScene, etc.)
  - `cameras.md`, `configuration.md`, `utilities_misc.md`
- `reference/` - Detailed API docs for individual classes/functions (385 .md files)
  - Named as `manim.<module>.<class>.md` (e.g., `manim.animation.creation.Create.md`)
  - Contains parameters, methods, attributes, and usage examples
- `reference.md` - Full hierarchical module index (lists all classes organized by module)

## Required Workflow
## Required Workflow (STRICTLY ENFORCED)
1. **Read the scene file**: Use `read_file ./animation_workspace/scene.py` to see the existing boilerplate.
2. **Mandatory Planning**: You MUST break the storyboard down into smaller chunks. 
3. **Chunk 1 (Setup & Intro)**: Use `edit_file` to append `class MyScene(Scene):`, `def construct(self):`, and Scenes 0 through 2. Stop and execute this tool call.
4. **Chunk 2, 3, 4 (Middle & End)**: Make SEPARATE `edit_file` tool calls to append the remaining scenes in batches of 2 or 3. To append, find the last `self.wait()` in the file and replace it with `self.wait() \n\n # Next Scene...`
5. **CRITICAL LIMIT:** NEVER write more than 3 scenes in a single `edit_file` tool call. If you try to write the whole script at once, the system will crash with a JSON error.

## Key Manim Patterns (for reference)
- Scenes: Subclass `Scene`, implement `construct()`, use `self.play()` for animations
- Mobjects: Circle, Square, Text, MathTex, Arrow, VGroup, Matrix, Table, etc.
- Animations: Create, FadeIn, FadeOut, Transform, ReplacementTransform, Write, GrowArrow
- Positioning: `.move_to()`, `.next_to()`, `.shift()`, constants like UP, DOWN, LEFT, RIGHT
- Animate syntax: `mobject.animate.method()` to animate property changes

## Vertical Layout Tips
- Place titles at the top (UP * 5 or higher)
- Stack content vertically with consistent spacing
- Use `.scale()` to ensure objects fit within width=8 units
- Consider using `VGroup` with `.arrange(DOWN)` for vertical stacking
- **Reserve bottom 1.5-2 units for the concept caption bar**

## Detail & Richness Checklist
Before finalizing your code, verify:
- [ ] Every scene has a concept caption at the bottom
- [ ] All visual elements are labeled with text
- [ ] Numbers/values are shown where applicable (not just abstract shapes)
- [ ] Colors are meaningful and consistent across scenes
- [ ] Complex concepts are built up incrementally
- [ ] Mathematical formulas appear alongside their visual representations
- [ ] Transitions between scenes are smooth (FadeOut/FadeIn)

Remember: ALWAYS use your tools to research the documentation before writing code. Complete `./animation_workspace/scene.py` by adding your Scene class with all animations below the existing boilerplate."""

# UPDATE: We added standard Python imports so the agent never fails on a missing 'math' or 'random' module again!
SCENE_BOILERPLATE = """# The videos are meant to be in vertical format (1080*1920, portrait orientation).
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
"""

def format_storyboard_prompt(
    breakdown,
    storyboard,
    topic_index: int,
) -> str:
    """Format the storyboard into a prompt for the animation agent.
    
    Args:
        breakdown: The Breakdown object containing all topics.
        storyboard: The TopicStoryboard for this specific topic.
        topic_index: Index of the current topic in the breakdown.
        
    Returns:
        Formatted prompt string for the animation agent.
    """
    current_topic = breakdown.topics[topic_index]
    total_topics = len(breakdown.topics)
    previous_topic = breakdown.topics[topic_index - 1] if topic_index > 0 else None
    next_topic = breakdown.topics[topic_index + 1] if topic_index < total_topics - 1 else None

    # Convert storyboard scenes to text
    storyboard_text = ""
    for i, scene in enumerate(storyboard.scenes):
        storyboard_text += f"## Scene {i+1}\n"
        storyboard_text += scene.to_text() + '\n'

    # Build series context
    series_context = f"""# Document Context
**Document:** {breakdown.pdf_title}
**Summary:** {breakdown.document_summary}

# Series Navigation
This is **Part {topic_index + 1} of {total_topics}** in the series on "{breakdown.pdf_title}".

**All Topics in Series:**
"""
    for i, topic in enumerate(breakdown.topics):
        marker = "👉 " if i == topic_index else "   "
        series_context += f"{marker}{i + 1}. {topic.name}\n"

    # Previous/Next topic info
    if previous_topic:
        series_context += f"""
**Previous Topic (Part {topic_index}):** {previous_topic.name}
- Summary: {previous_topic.summary}
"""

    if next_topic:
        series_context += f"""
**Next Topic (Part {topic_index + 2}):** {next_topic.name}
- Summary: {next_topic.summary}
"""

    # Topic details from breakdown
    topic_context = f"""
# Current Topic Details
**Topic:** {current_topic.name}
**Summary:** {current_topic.summary}

**Full Explanation:**
{current_topic.full_explanation}

**Key Takeaways:**
"""
    for takeaway in current_topic.key_takeaways:
        topic_context += f"- {takeaway}\n"

    # Get topic name for caption
    topic_name_short = storyboard.topic_name.split(':')[0] if ':' in storyboard.topic_name else storyboard.topic_name
    
    # Build next topic preview section
    next_preview = ""
    if next_topic:
        next_preview = f'3. Add a "Coming Next" preview: "Next: {next_topic.name}" with a brief teaser about what viewers will learn'

    storyboard_prompt = f"""
{series_context}
{topic_context}

---

# Storyboard: {storyboard.topic_name}

You will implement this storyboard as a Manim animation. The visual descriptions specify what to render; the narration is for audio only (don't render narration text).

## Scene 0: Opening Frame
Display a brief series header like "Part {topic_index + 1}/{total_topics}: {breakdown.pdf_title}" at the top (small, subtle), then a hook on what we will learn in this topic.
**Concept Caption:** "Understanding {topic_name_short}"

{storyboard_text}

## Final Scene: Closing & Preview
After the last storyboard scene, add a closing sequence:
1. Fade out the current content
2. Show a summary of key takeaways from this topic (use the Key Takeaways above)
{next_preview}

---

# Implementation Notes
1. Add ONE Scene class with all animations in `construct()`
2. Use smooth transitions (FadeOut/FadeIn/Transform) between scenes
3. VERTICAL FORMAT: 8 units wide * 14 tall - stack elements vertically
4. Complete `./animation_workspace/scene.py` below the existing boilerplate
5. Use the document context and topic explanation to ensure accurate technical content
6. The opening should briefly acknowledge the series context (part X of Y)
7. The closing should tease the next topic to encourage continued viewing
"""
    return storyboard_prompt