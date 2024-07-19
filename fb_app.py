import json
import time
import base64
import requests

import random
import string

import logging

from typing import Any

from  config_reader import config


url = 'https://api-key.fusionbrain.ai/'
api_key = config.api_key.get_secret_value()
secret_key = config.secret_key.get_secret_value()


class CreateImage:
    """
    The CreateImage class contains methods for generating an image.

    :param url:        Authorization link for keys
    :param api_key:    API key for connecting to the API
    :param secret_str: Secret key for connecting to the API
    """
    def __init__(self, url: str, api_key: str,
                 secret_key: str) -> None:
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    @staticmethod
    def get_number(length=6) -> str:
        all_symbols = string.ascii_uppercase + string.digits
        number = ''.join(random.choice(all_symbols) for _ in range(length))

        return number


    def get_model(self) -> int:
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()

        return data[0]['id']


    def generate(self, prompt: str, neagative_prompt: str, 
                 style: str, model: int, width: int, height: int
                ) -> Any:
        params = {
            "type": "GENERATE",
            "numImages": 1, 
            "style": style,
            "width": width,
            "height": height,
            "negativePromptUnclip": neagative_prompt,
            "generateParams": {
            "query": prompt
            }
        }

        data = {
            'model_id': (None, model),
            'params':   (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()

        return data['uuid']


    def check_generation(self, request_id: Any, 
                         attempts=10, delay=10
                        ) -> Any:
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()

            if data['status'] == 'DONE':
                return data['images']
            
            elif data['status'] == 'FAIL':
                return -1

            attempts -= 1
            time.sleep(delay)


def get_image(prompt: str, negative_prompt: str,
               style: str, ratio: tuple = None
             ) -> bytes:
    
    api = CreateImage(url, api_key=api_key, secret_key=secret_key)
    model_id = api.get_model()

    user_width, user_height = ratio

    uuid = api.generate(prompt=prompt, neagative_prompt=negative_prompt,
                        style=style, model=model_id, width=user_width, height=user_height)

    images = api.check_generation(uuid)

    if images != -1:

        image_base64 = images[0] 

        image_data = base64.b64decode(image_base64)
        number = api.get_number()
        with open(file=f"images/image{number}.jpg", mode="wb") as file:
            file.write(image_data)

        logging.info(f"Successful generation")

        return number
    
    else:
        logging.info(f"Error during generation")

        return -1 
