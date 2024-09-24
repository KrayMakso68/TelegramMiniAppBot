from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sing-in")
def sing_in():
    pass
