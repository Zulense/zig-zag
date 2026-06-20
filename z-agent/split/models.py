from pydantic import BaseModel, Field


class Split(BaseModel):

    """Split the document into micro part"""

    pdf_title: str = Field(description="Title of the paper/document")
    document_summary: str = Field(description="Berief 2-3 sentence overview of the entire document.")
