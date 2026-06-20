from pydantic import BaseModel, Field
from typing import Literal

class MicroTopic(BaseModel):
    """A self-contained topic extracted from a document."""

    name: str = Field(
        description="A concise, descriptive title for the extracted topic. Maximum of 6 words. Do not use punctuation at the end (e.g., 'Self-Attention Mechanism')."
    )
    summary: str = Field(
        description="A strict 2 to 3 sentence summary of the topic's core concept. Write in an engaging, accessible tone suitable for a video script hook. Avoid dense technical jargon in this field."
    )
    full_explanation: str = Field(
        description="A comprehensive, fully self-contained markdown explanation. The reader must be able to understand this without having read the rest of the document. Include all necessary context, definitions, and equations exactly as they appear in the source. If referencing figures or tables, describe what they show contextually, as the viewer cannot see the original images. Do not hallucinate external knowledge."
    )
    key_takeaways: list[str] = Field(
        description="Exactly 2 to 4 distinct points highlighting the most critical facts. Each item must be a single, concise sentence. Output raw text only; do not include markdown bullet characters (like '-' or '*') in the strings."
    )

    def to_text(self) -> str:
        """Convert the topic to a formatted markdown string."""
        takeaways = "\n".join(f"- {t}" for t in self.key_takeaways)
        return (
            f"**name**: {self.name}\n\n"
            f"**summary**: {self.summary}\n\n"
            f"**full_explanation**:\n{self.full_explanation}\n\n"
            f"**key_takeaways**:\n{takeaways}"
        )
    

class Split(BaseModel):

    """Split the document into micro part"""

    pdf_title: str = Field(description="The exact, formal title of the document as it appears on the first page. Do not include author names, publication dates, or file extensions (e.g., .pdf).")
    document_summary: str = Field(description="A concise, high-level summary of the document's core objective and key findings. Must be strictly 2 to 3 sentences long. Focus on the main purpose rather than specific data points.")

    topics: list[MicroTopic] = Field(description="List of atomic, self-contained topics extracted from the document.")


class Scene(BaseModel):
    """A single scene in the storyboard - a complete visual and audio sequence."""

    scene_type: Literal["hook", "mid", "closing"] = Field(
        default="mid",
        description="Type of scene: 'hook' for opening, 'mid' for main content, 'closing' for finale",
    )
    title: str = Field(
        description="A brief title for this scene (e.g., 'The Attention Spotlight', 'Matrix Multiplication Dance')"
    )
    visual_description: str = Field(
        description="""A filmmaker's script describing exactly what appears on screen. Written as a detailed visual 
        screenplay - every object, color, position, movement, transformation, and visual relationship must be 
        precisely specified. A reader should be able to perfectly visualize the animation without seeing it.
        Include: what appears, where it appears, how it moves, what colors/sizes, what transforms into what,
        spatial relationships, visual metaphors, and the emotional arc of the scene."""
    )
    narration: str = Field(
        description="The spoken narration for this scene, written for text-to-speech. "
        "Should complement (not duplicate) the visuals - explain what the viewer sees, "
        "provide context, and guide their understanding. Paced to match the visual flow."
    )

    def to_text(self) -> str:
        """Convert the scene to a formatted string."""
        return (
            f"## [{self.scene_type}] {self.title}\n\n"
            f"**Visual Description:**\n{self.visual_description}\n"
            f"**Narration:**\n{self.narration}\n"
        )

class TopicStoryboard(BaseModel):
    """A complete visual storyboard for one atomic topic - a filmmaker's screenplay."""

    topic_name: str = Field(description="Name of the atomic topic being visualized")
    visual_concept: str = Field(
        description="The overarching visual metaphor or analogy that ties the entire storyboard together. What is the 'big picture' visual idea?"
    )
    scenes: list[Scene] = Field(
        description="Ordered scenes (hook → mid scenes → closing) that tell the complete visual story. Each scene must have exhaustively detailed visual descriptions."
    )
