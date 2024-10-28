import base64

from httpx import AsyncClient, HTTPError
from fastapi.exceptions import HTTPException

from app.repository.interfaces import IUserRepository
from app.core.config import settings


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_user_avatar(self, user_tg_id: int) -> str:
        bot_token = settings.BOT_TOKEN
        base_url = f"https://api.telegram.org/bot{bot_token}"

        async with AsyncClient() as client:
            try:
                response = await client.get(
                    f"{base_url}/getUserProfilePhotos",
                    params={"user_id": user_tg_id},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                if not (data.get("ok") and data.get("result") and data["result"]["total_count"] > 0):
                    raise HTTPException(status_code=404, detail="User has no profile photos.")

                photo = data["result"]["photos"][0][0]
                file_id = photo["file_id"]

                file_response = await client.get(
                    f"{base_url}/getFile",
                    params={"file_id": file_id},
                    timeout=30
                )
                file_response.raise_for_status()
                file_data = file_response.json()

                if file_data.get("ok"):
                    file_path = file_data["result"]["file_path"]
                    download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"

                    image_response = await client.get(download_url)
                    image_response.raise_for_status()

                    image_base64 = base64.b64encode(image_response.content).decode("utf-8")
                    return image_base64

            except HTTPError:
                raise HTTPException(status_code=500, detail="Internal Server Error.")
