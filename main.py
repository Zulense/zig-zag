from google import genai
from dotenv import load_dotenv
load_dotenv()
import os 
api_key = os.getenv("API_KEY")

from zagent.split.Users import SplitUser, AnimationClient


def my_progress_tracker(topic_index, iteration, message):
    print(f"⏳ [Topic {topic_index} | Attempt {iteration}] {message}")

def main():
    print("Welome to z-agent")

    # initialize gemni client.
    gemni_api = genai.Client(api_key=api_key)

    ## split the pdf into sentences.
    split_client = SplitUser(gemni_api=gemni_api)

    split, gemni_response = split_client.split(pdf_path="./attention_is_all_you_need_removed.pdf",
                                               model="gemini-2.5-flash")
    

    print(f"Document: {split.pdf_title}")
    for i, topic in enumerate(split.topics):
        print(f"  Topic {i}: {topic.name}")

    # -------------------------------------------------------------------------------------
    # 1. Write the topic name you want to animate
    desired_topic_name = "Self-Attention"

    # 2. Dynamically calculate the target_index based on the name
    target_index = 0
    best_match_score = 0

    # Helper function to clean text: replaces punctuation with spaces, then makes a set
    def extract_words(text):
        clean_text = ''.join(c if c.isalnum() else ' ' for c in text.lower())
        return set(clean_text.split())

    search_words = extract_words(desired_topic_name)

    for i, topic in enumerate(split.topics):
        topic_words = extract_words(topic.name)
        
        # Count how many words match between your target and the AI's output
        match_score = len(search_words.intersection(topic_words))
        
        # Keep track of the highest scoring index
        if match_score > best_match_score:
            best_match_score = match_score
            target_index = i

    # 3. Safely set the target topic name using the dynamically found index
    target_topic_name = split.topics[target_index].name
    print(f"🎯 Dynamically matched to Index {target_index}: '{target_topic_name}'")
   

    # -------------------------------------------------------------------------------------------------------


    ## Generate story of each topics.

    storyboards = {}
    for topic in split.topics:
        storyboard, _ = split_client.storycontent(
            topic=topic,
            model="gemini-2.5-flash",
            
        )
        storyboards[topic.name] = storyboard
    print("==============> [storyboards]", storyboards)

    ## step 3. Animate story board with the Manim Agent.
    from langchain_google_genai import ChatGoogleGenerativeAI

    langchain_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        tempurate=1.0,
        api_key=api_key
    )

    animation = AnimationClient(langchain_model=langchain_model,
                                agent_workspace_path="./zagent/utils/agent_workspace")
    
    # target_index = 1
    # target_topic_name = split.topics[target_index].name

    # Animate a single topic
    result = animation.animate_single(
        split=split,
        story=storyboards[target_topic_name],
        topic_index=target_index,
        max_iteration=3,
        on_progress=my_progress_tracker
    )


if __name__ == "__main__":
    main()
