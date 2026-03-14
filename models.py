from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from database import Base

# 1. 사용자 테이블
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))
    phone = Column(String(255), unique=True, index=True) 
    password = Column(String(255))       

    remaining_songs = Column(Integer, default=0)  # ⭐ 추가                

# 2. 노래방 부스(방) 테이블
class Booth(Base):
    __tablename__ = "booths"

    booth_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(50))                                
    status = Column(String(20), default="empty")             

# 3. 노래 데이터 (노래방 책)
class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True) 
    title = Column(String(100), index=True)                 
    singer = Column(String(50), index=True)                 
    tj_number = Column(Integer, unique=True)                

# 4. 예약 목록 (부스별 대기열)
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    booth_id = Column(Integer)  
    song_id = Column(Integer)   
    status = Column(String(20), default="waiting") 

# [새로 추가] 5. AI 분석 결과 테이블
class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=True)  # 어떤 사용자의 점수인지 (아이유, 김철수 등)
    filename = Column(String(100))               # 저장된 파일명
    
    # 점수 데이터
    pitch_score = Column(Float)
    tempo_score = Column(Float)
    volume_score = Column(Float)
    
    # 상세 분석 값
    pitch_hz_avg = Column(Float)
    tempo_bpm = Column(Float)
    volume_rms_avg = Column(Float)
    
    feedback = Column(String(500))               # AI 피드백 문구
    feature_path = Column(String(200))           # 특징 추출된 폴더 경로
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 분석 시간