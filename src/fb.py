import json
import time
import base64
import random
import string
import requests
from typing import Any

from configs.config_reader import cfg


class CreateImage:
    """
    Создание изображений 
    """    
    def __init__(
        self, 
        url: str, 
        api_key: str,
        secret_key: str
        ) -> None:

        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }


    @staticmethod
    def get_random_number(length: int = 6) -> str:
        """
        Создание случайного номера для сгенерированной картинки 
        """
        all_symbols = string.ascii_uppercase + string.digits
        number = ''.join(random.choice(all_symbols) for _ in range(length))

        return number


    def get_model(self) -> int:
        """
        Обращение к модели Kandinsky 3.1 
        """
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()

        return data[0]['id']


    def generate_image(
        self, 
        prompt: str, 
        neagative_prompt: str, 
        style: str, 
        model: int, 
        ) -> Any:
        """
        Отправка запроса генерации модели
        """
        params = {
            "type": "GENERATE",
            "numImages": 1, 
            "style": style,
            "width": 1024,
            "height": 1024,
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


    def check_generation(
        self, 
        request_id: Any, 
        attempts=10, 
        delay=10
        ) -> Any:
        """
        Проверка статуса генерации изображения 
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()

            if data['status'] == 'DONE':
                    return data['images']
            
            attempts -= 1
            time.sleep(delay)


def get_image(
    prompt: str, 
    negative_prompt: str,
    style: str, 
    ) -> bytes:
    """
    Сохранение изображения 
    """
    api = CreateImage(url=cfg.url,
                        api_key=cfg.api_key.get_secret_value(),
                        secret_key=cfg.secret_key.get_secret_value())
        
    uuid = api.generate_image(style=style,
                              prompt=prompt,
                              model=api.get_model(), 
                              neagative_prompt=negative_prompt)

    image = api.check_generation(uuid)
    image_data = base64.b64decode(image[0])

    number = api.get_random_number()

    with open(file=f"images/image_{number}.jpg", mode="wb") as file:
        file.write(image_data)

    return number


