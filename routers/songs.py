from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import shutil
import os
from ai_module.analyze_voice_final import analyzeVoice

router = APIRouter(prefix="/songs", tags=["🎵 Songs (노래/AI 연동)"])

# 경로 설정 (OneDrive 및 한글 경로 대응)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_files")

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload", summary="녹음 파일 업로드, AI 분석 및 예약 완료 처리")
async def upload_song(
    file: UploadFile = File(...),
    reservation_id: int = Form(...),  # 예약 번호 (상태 업데이트용)
    user_id: str = Form(...),         # 사용자 아이디 (기록 매칭용)
    reference_song: str = Form("No_Doubt"),
    user_bpm: float = Form(120.0),
    db: Session = Depends(get_db)
):
    # 1. 파일 저장
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. AI 분석 실행
    try:
        # analyze_voice_final.py의 analyzeVoice 함수 호출
        result = analyzeVoice(wav_path=file_path, reference_song=reference_song, user_bpm=user_bpm)
        
        if "error" in result:
            return {"status": "fail", "message": result["error"]}

        # 3. AI 피드백 및 추천 가수 문자열 정리
        # AI 담당자가 만든 피드백 문구를 가져오고, 없으면 기본값 설정
        ai_feedback = result.get("feedback", "분석이 성공적으로 완료되었습니다.")
        
        # 추천 가수 리스트를 "가수명(유사도%)" 형태의 한 문장으로 합침
        recommendations = result.get("recommendations", [])
        recommend_str = ", ".join([f"{r['singer']}({r['similarity']*100:.1f}%)" for r in recommendations])
        
        # 최종적으로 DB에 저장될 피드백 내용
        final_feedback_text = f"{ai_feedback} [추천: {recommend_str}]"

        # 4. 분석 결과 DB 저장 (1단계 완료)
        new_analysis = models.AnalysisResult(
            user_id=user_id,
            filename=filename,
            pitch_score=result["scores"]["pitch"],
            tempo_score=result["scores"]["tempo"],
            volume_score=result["scores"]["volume"],
            pitch_hz_avg=result["analysis_values"]["pitch_hz_avg"],
            tempo_bpm=result["analysis_values"]["tempo_bpm"],
            volume_rms_avg=result["analysis_values"]["volume_rms_avg"],
            feedback=final_feedback_text,  # AI의 실제 피드백 저장
            feature_path=file_path
        )
        db.add(new_analysis)

        # 5. 예약 상태 업데이트 (2단계 완료)
        # 해당 예약 번호를 찾아서 상태를 'completed'로 변경
        reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
        if reservation:
            reservation.status = "completed"
            print(f"✅ 예약 {reservation_id}번 상태가 'completed'로 변경되었습니다.")

        # 모든 변경사항(분석결과 추가 + 예약상태 변경)을 한 번에 저장
        db.commit() 

        return {
            "status": "success", 
            "message": f"{user_id}님의 분석 및 예약 완료 처리가 성공했습니다.",
            "data": {
                "scores": result["scores"],
                "feedback": ai_feedback,
                "recommendations": recommendations
            }
        }

    except Exception as e:
        db.rollback()
        print(f"❌ 서버 에러 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")