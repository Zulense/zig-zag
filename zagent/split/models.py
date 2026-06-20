from pydantic import BaseModel, Field


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


