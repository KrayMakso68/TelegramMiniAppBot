from typing import Annotated
from fastapi import Depends

from app.core.security import oauth_scheme


def get_current_user(
        token: Annotated[str, Depends(oauth_scheme)]
):
    ...
