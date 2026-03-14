from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

# 라우터 이름표 붙이기 (URL 앞에 /booth가 자동으로 붙음)
router = APIRouter(prefix="/booth", tags=["Booth (노래방 부스 관리)"])

# 1. 모든 방 목록 조회 (GET /booth/)
@router.get("/")
def get_all_booths(db: Session = Depends(get_db)):
    # DB 명령: SELECT * FROM booths;
    booths = db.query(models.Booth).all()
    return {"status": "success", "data": booths}

# 2. 특정 방 상태 조회 (GET /booth/1) - 나중에 쓸 수 있음
@router.get("/{booth_id}")
def get_booth_status(booth_id: int, db: Session = Depends(get_db)):
    # DB 명령: SELECT * FROM booths WHERE booth_id = ...
    booth = db.query(models.Booth).filter(models.Booth.booth_id == booth_id).first()
    
    if not booth:
        return {"status": "error", "message": "존재하지 않는 방입니다."}
    
    return {"status": "success", "data": booth}

# 3. 방 사용 시작 (POST /booth/1/start)
@router.post("/{booth_id}/start")
def start_use_booth(booth_id: int, db: Session = Depends(get_db)):
    booth = db.query(models.Booth).filter(models.Booth.booth_id == booth_id).first()
    
    if not booth:
        return {"status": "error", "message": "존재하지 않는 방입니다."}

    if booth.status == "busy":
        return {"status": "error", "message": "이미 사용 중인 방입니다."}

    booth.status = "busy"
    db.commit() 

    return {"status": "success", "message": f"{booth_id}번 방 사용을 시작합니다.", "current_status": "busy"}

# 4. 방 사용 종료 (POST /booth/1/end)
@router.post("/{booth_id}/end")
def finish_use_booth(booth_id: int, db: Session = Depends(get_db)):
    booth = db.query(models.Booth).filter(models.Booth.booth_id == booth_id).first()
    
    if not booth:
        return {"status": "error", "message": "존재하지 않는 방입니다."}
    
    if booth.status == "empty":
        return {"status": "error", "message": "이미 빈 방입니다."}

    booth.status = "empty"
    db.commit()

    return {"status": "success", "message": f"{booth_id}번 방 사용을 종료합니다.", "current_status": "empty"}