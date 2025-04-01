from typing import Optional
import requests
from requests.exceptions import (
    ConnectionError, Timeout, HTTPError
)
import io


class ImageClientError(Exception):
    """Custom error for cleint exceptions"""
    pass


class ImageClient:
    def __init__(self, host: str = 'http://89.169.157.72:8080'):
        self.host = host

    def request_image(self, image_id: int) -> Optional[bytes]:
        """get image by id from prodider"""
        try:
            response = requests.get(
                f'{self.host}/images/{image_id}',
                timeout=1
            )
            response.raise_for_status()
            img = io.BytesIO(response.content)
        except ConnectionError:
            raise ImageClientError("No connection to img")
        except Timeout:
            raise ImageClientError("The request timed out.")
        except HTTPError:
            raise HTTPError("Some other network error")
        except OSError:
            raise OSError("Server couldn handle")
        else:
            return img

    @staticmethod
    def check_if_img_acceptable(image_id: int) -> bool:
        """check if its possible to get image"""
        return image_id in {10022, 9965}
