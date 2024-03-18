import logging
import time
import re
from openai import OpenAI, BadRequestError

MAX_ATTEMPT = 3
logger = logging.getLogger(__name__)

class ImageAgent:
    def __init__(self, key, model, text_agent):
        self.client = OpenAI(api_key=key)
        self.model = model
        self.text_agent = text_agent
    
    def generate(self, message, attempt=1):
        pattern = re.compile(r'nacked|nude|naked', re.IGNORECASE)
        message = pattern.sub('skin-colored', message).replace("\"", "")
        logger.debug(f"Generating \"{message}\"...")

        try:
            completion = self.client.images.generate(prompt=message, n=1, size="1024x1024", model=self.model) # 1024*1792
        except BadRequestError as e:
            logger.debug(e)
            if (e.code == "content_policy_violation"):
                logger.debug(f"Message denied: \"{message}\"")
                if attempt > MAX_ATTEMPT:
                    logger.debug("Max tentative reached! Image won't be generated.")
                    return
                logger.debug(f"Retrying, {MAX_ATTEMPT - attempt} retry left...")
                new_message = self.text_agent.send_message(
                    f"This text does not pass DALL-E content policy. Rewrite it: {message}"
                )
                logger.debug(f"New message: \"{new_message}\"")
                return self.generate(new_message, attempt + 1)
            else:
                time.sleep(10)
                return self.generate(new_message, attempt)

        return completion.data[0].url
