from google import genai
from dotenv import load_dotenv
load_dotenv()
import os 
api_key = os.getenv("API_KEY")

from zagent.split.Users import SplitUser


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


    ## Generate story of each topics.

    storyboards = {}
    for topic in split.topics:
        storyboard, _ = split_client.storycontent(
            topic=topic,
            model="gemini-2.5-flash",
            
        )
        storyboards[topic.name] = storyboard
    print("==============> [storyboards]", storyboards)


if __name__ == "__main__":
    main()
