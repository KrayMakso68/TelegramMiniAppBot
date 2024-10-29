import base64
from enum import Enum

from fastapi import HTTPException
from httpx import AsyncClient, HTTPError


class TelegramApi:
    request_timeout = 30

    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def get_user_avatar(self, user_id: int, high_quality: bool = False) -> str:
        base_url = f"https://api.telegram.org/bot{self.bot_token}"
        quality = 0

        if high_quality:
            quality = -1

        async with AsyncClient() as client:
            try:
                response = await client.get(
                    f"{base_url}/getUserProfilePhotos",
                    params={"user_id": user_id},
                    timeout=self.request_timeout
                )
                response.raise_for_status()
                data = response.json()

                if not (data.get("ok") and data.get("result") and data["result"]["total_count"] > 0):
                    raise HTTPException(status_code=404, detail="User has no profile photos.")

                photo = data["result"]["photos"][0][quality]
                file_id = photo["file_id"]

                file_response = await client.get(
                    f"{base_url}/getFile",
                    params={"file_id": file_id},
                    timeout=self.request_timeout
                )
                file_response.raise_for_status()
                file_data = file_response.json()

                if file_data.get("ok"):
                    file_path = file_data["result"]["file_path"]
                    download_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

                    image_response = await client.get(download_url)
                    image_response.raise_for_status()

                    image_base64 = base64.b64encode(image_response.content).decode("utf-8")
                    return image_base64

            except HTTPError:
                raise HTTPException(status_code=500, detail="Internal Server Error.")
