from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
from database import get_db
import models
from utils import aes_encrypt
from passlib.context import CryptContext

# 비밀번호 암호화 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["👤 Users (회원관리)"]
)

# ===============================
# Pydantic 모델
# ===============================

class UserCreate(BaseModel):
    user_id: str = Field(..., pattern=r"^[a-zA-Z]{4,20}$")
    phone: str = Field(..., pattern=r"^010\d{8}$")
    password: str = Field(..., pattern=r"^\d{1,6}$")

    @field_validator("user_id")
    def validate_user_id(cls, v):
        if not v.isalpha():
            raise ValueError("아이디는 영문만 가능합니다.")
        return v


class UserLogin(BaseModel):
    phone: str = Field(..., pattern=r"^010\d{8}$")
    password: str


# ===============================
# 1️⃣ 회원가입 API
# ===============================

@router.post("/signup", summary="회원가입")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):

    try:
        # 전화번호 암호화
        crypto_phone = aes_encrypt(user_data.phone)

        # 이미 가입된 전화번호 확인
        existing_user = db.query(models.User).filter(models.User.phone == crypto_phone).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="이미 가입된 전화번호입니다."
            )

        # 비밀번호 해시
        hashed_password = pwd_context.hash(user_data.password)

        # 유저 생성
        new_user = models.User(
            user_id=user_data.user_id,
            phone=crypto_phone,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "회원가입 완료",
            "user_id": new_user.user_id
        }

    except Exception as e:
        print("회원가입 오류:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 2️⃣ 로그인 API
# ===============================

@router.post("/login", summary="로그인")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    try:
        # 전화번호 암호화
        crypto_phone = aes_encrypt(user_data.phone)

        # DB 조회
        db_user = db.query(models.User).filter(models.User.phone == crypto_phone).first()

        # 유저 없거나 비밀번호 틀림
        if not db_user or not pwd_context.verify(user_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="전화번호 또는 비밀번호가 일치하지 않습니다."
            )

        return {
            "status": "success",
            "message": f"안녕하세요, {db_user.user_id}님!",
            "user_id": db_user.user_id
        }

    except Exception as e:
        print("로그인 오류:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 3️⃣ 내 점수 기록 조회
# ===============================

@router.get("/{user_id}/history", summary="내 점수 기록 조회")
def get_user_history(user_id: str, db: Session = Depends(get_db)):

    history = (
        db.query(models.AnalysisResult)
        .filter(models.AnalysisResult.user_id == user_id)
        .order_by(models.AnalysisResult.id.desc())
        .all()
    )

    return {
        "status": "success",
        "data": history
    }