# routers/library.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/library",
    tags=["📖 Library (노래 검색/예약)"]
)

# 1. 노래 검색 API
@router.get("/search", summary="노래 검색", description="가수나 제목으로 노래를 찾습니다.")
def search_song(keyword: str, db: Session = Depends(get_db)):
    # 제목이나 가수에 키워드가 포함된 노래 찾기 (LIKE 검색)
    results = db.query(models.Song).filter(
        (models.Song.title.like(f"%{keyword}%")) | 
        (models.Song.singer.like(f"%{keyword}%"))
    ).all()
    return {"count": len(results), "results": results}

# 2. 노래 예약 API
@router.post("/reserve", summary="노래 예약", description="부스 번호와 노래방 번호(TJ 번호)를 받아 예약합니다.")
def reserve_song(booth_id: int, tj_number: int, db: Session = Depends(get_db)): 
    
    # 1. 노래 찾기 (tj_number로 검색!)
    song = db.query(models.Song).filter(models.Song.tj_number == tj_number).first()
    
    if not song:
        raise HTTPException(status_code=404, detail="존재하지 않는 노래 번호입니다.")

    # 2. 예약 내역 저장 (저장할 때는 song_id(고유키)로 연결해두는 게 DB 정석)
    new_reservation = models.Reservation(
        booth_id=booth_id,
        song_id=song.song_id, # 찾은 노래의 고유 ID를 저장
        status="waiting"
    )
    db.add(new_reservation)
    db.commit()

    return {"status": "success", "message": f"[{song.title}] 예약되었습니다. (방: {booth_id}번)"}


# 3. 예약 목록 조회 (현재 대기 중인 곡)
@router.get("/reservations/{booth_id}", summary="예약 목록 확인")
def get_reservations(booth_id: int, db: Session = Depends(get_db)):
    return db.query(models.Reservation).filter(
        models.Reservation.booth_id == booth_id,
        models.Reservation.status == "waiting"
    ).all()