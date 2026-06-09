from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_ports():
    return {"message": "Liste des ports"}