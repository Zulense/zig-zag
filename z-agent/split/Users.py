from pathlib import Path
import os 
from google.genai import types

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
                                                 response_json_schema=)
        )

            


