from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils import aes_encrypt
import models

# DB 연결
from database import get_db
from models import User

# 이 파일은 '키오스크' 관련 기능만 모아두는 곳입니다.
router = APIRouter(prefix="/kiosk", tags=["External Kiosk (외부 키오스크)"])

# 요청 데이터 양식 (곡 수 선택)
class SongSelect(BaseModel):
    phone: str | None = None  # 비회원이면 None(비어있음)
    song_count: int  # 1 ~ 3곡


# 1. 잔여 곡 수 / 회원 상태 확인 API
from database import SessionLocal

@router.get("/user/{phone}")
def check_user_credits(phone: str, db: Session = Depends(get_db)):

    crypto_phone = aes_encrypt(phone)

    user = db.query(models.User).filter(models.User.phone == crypto_phone).first()

    if user:
        return {
            "phone": phone,
            "is_member": True,
            "remaining_songs": user.remaining_songs
        }

    return {
        "phone": phone,
        "is_member": False,
        "remaining_songs": 0
    }


# 2. 곡 수 결제 및 입장 처리 API
@router.post("/entry")
def enter_booth(selection: SongSelect, db: Session = Depends(get_db)):

    user_type = "회원" if selection.phone else "비회원"

    if selection.phone:
        crypto_phone = aes_encrypt(selection.phone)

        user = db.query(models.User).filter(
            models.User.phone == crypto_phone
        ).first()

        if user:
            user.remaining_songs = selection.song_count
            db.commit()

    return {
        "status": "success",
        "message": f"{user_type} 입장 처리 완료",
        "data": {
            "assigned_songs": selection.song_count,
            "room_status": "active"
        }
    }