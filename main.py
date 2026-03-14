from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routers import booth, users, songs, library, kiosk  # kiosk 추가
from fastapi.staticfiles import StaticFiles

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # <-- 반드시 먼저 선언

# --- Kiosk 관련 추가 ---
# 정적 파일 서비스 (HTML, JS 등)
app.mount("/kiosk_static", StaticFiles(directory="kiosk"), name="kiosk_static")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# 기존 라우터 연결
app.include_router(users.router)
app.include_router(booth.router)
app.include_router(songs.router)
app.include_router(library.router)
app.include_router(kiosk.router)

# 임시 노래 데이터 10곡 넣기
def init_dummy_songs(db: Session):
    if db.query(models.Song).count() == 0:
        dummy_songs = [
            models.Song(title="0+0", singer="한로로", tj_number=99991),
            models.Song(title="한숨", singer="이하이", tj_number=99992),
            models.Song(title="여름밤에 우리", singer="전진희(feat. wave to earth)", tj_number=99993),
            models.Song(title="좋은 날", singer="아이유", tj_number=1001),
            models.Song(title="너랑 나", singer="아이유", tj_number=1002),
            models.Song(title="밤편지", singer="아이유", tj_number=1003),
            models.Song(title="보고 싶다", singer="김범수", tj_number=2001),
            models.Song(title="응급실", singer="izi", tj_number=3001),
            models.Song(title="소주 한 잔", singer="임창정", tj_number=4001),
            models.Song(title="Hype Boy", singer="NewJeans", tj_number=5001),
        ]
        db.add_all(dummy_songs)
        db.commit()
        print("🎵 [System] 가짜 노래 10곡이 DB에 저장되었습니다!")

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    init_dummy_songs(db)

@app.get("/")
def read_root():
    return {"message": "SingPick Server is Running!"}