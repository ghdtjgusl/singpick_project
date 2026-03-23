import os
import sys

os.environ["TORCHAUDIO_USE_BACKEND_DISPATCHER"] = "0"

import subprocess
import json

from .extract_basic_features import extract_single_wav
from .analyze_voice import analyze_voice
from .similarity_engine import recommend_singers


def analyzeVoice(wav_path, reference_song, user_bpm, top_n=3):
    # 1. 경로 설정 (OneDrive 한글 경로 완벽 대응을 위한 절대 경로화)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 서버 루트에 있는 uploaded_files 폴더 내의 파일을 가리킴
    abs_wav_path = os.path.abspath(wav_path)

    if not os.path.exists(abs_wav_path):
        return {"error": f"원본 파일을 찾을 수 없습니다: {abs_wav_path}"}

    # 2. 특징 추출 실행 (uploaded_files에 있는 파일을 읽어서 처리함)
    try:
        print(f"🚀 분석 시작: {abs_wav_path}")
        extract_single_wav(abs_wav_path)
    except Exception as e:
        return {"error": f"AI 분석(Demucs/Feature) 단계에서 오류 발생: {str(e)}"}

    # 3. 추출된 결과물이 저장된 features 폴더 확인
    voice_name = os.path.splitext(os.path.basename(abs_wav_path))[0]
    # extract_basic_features.py에서 생성하는 폴더 위치와 일치시켜야 함
    feature_dir = os.path.join(current_dir, "features", voice_name)

    if not os.path.exists(feature_dir):
        # 만약 ai_module 밖에 features 폴더가 있다면 아래 경로로 시도
        alt_feature_dir = os.path.abspath(os.path.join(current_dir, "..", "features", voice_name))
        if os.path.exists(alt_feature_dir):
            feature_dir = alt_feature_dir
        else:
            return {"error": f"분석 결과 폴더 생성 실패: {feature_dir}"}

    # 4. 분석 및 점수 계산
    analysis_result = analyze_voice(
        feature_dir=feature_dir,
        user_bpm=user_bpm,
        reference_song_name=reference_song
    )

    return {
        "scores": analysis_result["scores"],
        "analysis_values": analysis_result["analysis_values"],
        "recommendations": recommend_singers(analysis_result["timbre_vector"], top_n=top_n)
    }