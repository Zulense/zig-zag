from google import genai
from dotenv import load_dotenv
load_dotenv()
import os 
api_key = os.getenv("API_KEY")


def main():
    print("Welome to z-agent")

    # initialize gemni client.
    gemni_api = genai.Client(api_key=api_key)

    ## split the pdf into sentences.
    split_client = 


if __name__ == "__main__":
    main()
