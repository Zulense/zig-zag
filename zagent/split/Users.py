from pathlib import Path
import os 
from google.genai import types
from .models import Split, MicroTopic, TopicStoryboard
from zagent.prompts.split import SPLIT_PROMPT
from zagent.prompts.story import STORYBOARD_PROMPT, format_topic_input


class SplitUser:

    """Split the Document and build story"""

    def __init__(self, gemni_api):
        
        self.gemni_api = gemni_api

    def split(self, 
              pdf_path: str | Path,
              model: str,
              ):

        if not os.path.exists(pdf_path):
            pdf_path = Path(pdf_path)

        # upload the pdf 
        self.uploaded_pdf = self.gemni_api.files.upload(file=pdf_path)

        # Generate Content
        gemni_response = self.gemni_api.models.generate_content(
            model = model,
            config = types.GenerateContentConfig(tools=[types.GoogleSearch()],
                                                 response_mime_type="application/json",
                                                 response_json_schema=Split.model_json_schema()),
            contents = [self.uploaded_pdf, SPLIT_PROMPT]
        )

        split = Split.model_validate_json(gemni_response.text)

        return split, gemni_response
    

    def storycontent(self, topic: MicroTopic, model: str, source_file: str | Path | None = None): 
        
        # Build the full prompt with topic input
        final_prompt = STORYBOARD_PROMPT + format_topic_input(topic)

        contents: list = []
        if source_file is not None:
            source_file = Path(source_file)
            uploaded_file = self.gemni_api.files.upload(file=source_file)
            contents.append(uploaded_file)
        contents.append(final_prompt)

        # ---------------------------------------------------------
        # STEP 1: The "Researcher" (Tools ON, JSON OFF)
        # ---------------------------------------------------------
        research_response = self.gemni_api.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                tools=[
                    types.GoogleSearch(),
                    types.Tool(code_execution=types.ToolCodeExecution),
                ],
                # Notice we do NOT ask for JSON here
            ),
            contents=contents,
        )
        
        # ---------------------------------------------------------
        # STEP 2: The "Formatter" (Tools OFF, JSON ON)
        # ---------------------------------------------------------
        formatting_prompt = (
            "Take the following drafted storyboard and format it STRICTLY into the requested JSON schema. "
            f"Draft:\n\n{research_response.text}"
        )

        final_response = self.gemni_api.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=TopicStoryboard.model_json_schema(),
            ),
            contents=[formatting_prompt],
        )

        # Validate perfectly structured output
        storyboard = TopicStoryboard.model_validate_json(final_response.text)

        return storyboard, final_response

    
    

            


