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

    
    
from langchain_core.language_models import BaseChatModel
from typing import Callable
from .models import AnimationResult
from zagent.prompts.animate import SCENE_BOILERPLATE, MANIM_CODING_AGENT_PROMPT, format_storyboard_prompt
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend



class AnimationClient:

    def __init__(self,
                 langchain_model: BaseChatModel,
                 agent_workspace_path: str | Path):
        
        
        self.langchain_model = langchain_model
        self.agent_workspace_path = Path(agent_workspace_path).resolve()

        # path within agent workspace agent
        self.manim_docs_path = self.agent_workspace_path / "manim_docs"
        self.animation_workspace_path = self.agent_workspace_path / "animation_workspace"
        self.rendered_video_path = self.agent_workspace_path / "rendered_videos"

        # Validate paths
        if not self.agent_workspace_path.exists():
            raise ValueError(f"agent_workspace_path does not exist: {self.agent_workspace_path}")
        if not self.manim_docs_path.exists():
            raise ValueError(f"manim_docs folder not found: {self.manim_docs_path}")
        if not self.animation_workspace_path.exists():
            self.animation_workspace_path.mkdir(parents=True, exist_ok=True)
        if not self.rendered_video_path.exists():
            self.rendered_video_path.mkdir(parents=True, exist_ok=True)

    def _prepare_workspace(self):
        """Clear the workspace and write the boilerplate scene file."""
        # Clear existing files in workspace (except keep the directory)
        for item in self.animation_workspace_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                import shutil
                shutil.rmtree(item)

        # Write boilerplate scene file
        scene_file = self.animation_workspace_path / "scene.py"
        scene_file.write_text(SCENE_BOILERPLATE)

    def _create_agent(self):
        """Create a new coding agent instance."""

        return create_deep_agent(
            model=self.langchain_model,
            system_prompt=MANIM_CODING_AGENT_PROMPT,
            backend=FilesystemBackend(root_dir=str(self.agent_workspace_path), virtual_mode=True),
        )


    def animate_single(self,
                       split: Split,
                       story: TopicStoryboard,
                       topic_index: int,
                       max_iteration: int,
                       on_progress: Callable[[int, int, str], None] | None = None,
                       ratelimit: int = 0) -> AnimationResult:
        

        import shutil

        topic_name = split.topics[topic_index].name if topic_index < len(split.topics) else "Unknown"
        print(f"[step-3] Topic Name =======================> {topic_name}")

        if on_progress:
            on_progress(topic_index, 0, f"Starting animation for Topic: {topic_name}")

        # prepare workspace 
        self._prepare_workspace()

        # create agent 
        agent = self._create_agent()
        print(f"[step-3] Agent =======================> {agent}")


        # Format the prompt for this topic
        prompt = format_storyboard_prompt(split, story, topic_index)
        print(f"[step-3] Prompt =======================> {prompt}")


        # Run agent
        if on_progress:
            on_progress(topic_index, 0, "Running coding agent...")
        



            


