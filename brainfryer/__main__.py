import argparse
import os
from dotenv import load_dotenv

from brainfryer.creator import *

LOGO = """
  ____               _         _____                         
 | __ )  _ __  __ _ (_) _ __  |  ___|_ __  _   _   ___  _ __ 
 |  _ \ | '__|/ _` || || '_ \ | |_  | '__|| | | | / _ \| '__|
 | |_) || |  | (_| || || | | ||  _| | |   | |_| ||  __/| |   
 |____/ |_|   \__,_||_||_| |_||_|   |_|    \__, | \___||_|   
                                           |___/             
"""

DEFAULT_SONG = "https://www.youtube.com/watch?v=bESTXIqCnac"
DEFAULT_BACKGROUND = "https://www.youtube.com/watch?v=R0b-VFV8SJ8"

load_dotenv()

GPT_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL_TEXT = os.getenv('OPENAI_MODEL_TEXT')
GPT_MODEL_IMAGE = os.getenv('OPENAI_MODEL_IMAGE')
GPT_MODEL_TTS = os.getenv('OPENAI_MODEL_TTS')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate attention-grabbing videos!', prog='python -m brainfryer')
    parser.add_argument('url', help='Reddit URL')
    parser.add_argument('--background', help='Youtube background URL (optional)')
    parser.add_argument('--song', help='Youtube song URL (optional)')
    parser.add_argument('--gen-images', action='store_true', help='Generate images (default: False)')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    # If CLI arguments are provided, use them; otherwise, prompt the user
    if args.url:
        url = args.url
        background = args.background or DEFAULT_BACKGROUND
        song = args.song or DEFAULT_SONG
        gen_images = args.gen_images
    else:
        print(LOGO)

        # Query user
        url = input("Reddit url: ")
        background = input("Youtube background url (empty = default): ") or DEFAULT_BACKGROUND
        song = input("Youtube song url (empty = default): ") or DEFAULT_SONG
        gen_images = True if input("Generate images (Y/N)? ").strip().lower() == 'y' else False

    creator = VideoCreator(GPT_KEY, GPT_MODEL_IMAGE, GPT_MODEL_TEXT, GPT_MODEL_TTS)

    # Generate
    creator.generate_from_reddit_comments(url, background, song, gen_images)

if __name__ == "__main__":
    main()