import os
import subprocess
import numpy as np
import librosa
import sys

os.environ["TORCHAUDIO_USE_BACKEND_DISPATCHER"] = "0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
FEATURE_DIR = os.path.join(BASE_DIR, "features")
SR = 22050

# 폴더 생성
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(FEATURE_DIR, exist_ok=True)


# =====================
# Demucs (절대 경로 및 mp3 출력 강제)
# =====================
def separate_vocals(wav_path):
    abs_wav_path = os.path.abspath(wav_path)
    abs_temp_dir = os.path.abspath(TEMP_DIR)
    
    # 1. 환경 변수 복사
    my_env = os.environ.copy()
    
    # [중요] FFmpeg bin 폴더의 절대 경로를 정확히 입력하세요.
    # 본인 컴퓨터의 실제 경로가 C:\ffmpeg\bin 인지 꼭 확인하세요!
    ffmpeg_bin_path = r"C:\ffmpeg\bin" 
    
    # 2. PATH의 맨 앞에 FFmpeg 경로를 추가하여 최우선순위로 만듭니다.
    my_env["PATH"] = ffmpeg_bin_path + os.pathsep + my_env.get("PATH", "")
    
    # 3. torchaudio 버그 방지 설정
    my_env["TORCHAUDIO_USE_BACKEND_DISPATCHER"] = "0"

    python_exe = sys.executable 

    print(f"[PROCESS] Demucs 실행 중: {abs_wav_path}")
    
    try:
        # 4. subprocess 실행 시 'env=my_env'를 통해 위 설정을 자식 프로세스에 강제 주입
        subprocess.run(
            [
                python_exe, "-m", "demucs",
                "--two-stems", "vocals",
                "--mp3",
                "-n", "htdemucs",
                abs_wav_path,
                "-o", abs_temp_dir
            ],
            check=True,
            env=my_env,      # 설정한 환경 변수 적용
            shell=False      # 윈도우 스토어 파이썬의 경우 False가 더 안정적입니다.
        )
    except subprocess.CalledProcessError as e:
        print(f"🔥 Demucs 실행 실패: {e}")
        raise e

    name = os.path.splitext(os.path.basename(abs_wav_path))[0]
    vocals_path = os.path.join(abs_temp_dir, "htdemucs", name, "vocals.mp3")
    return vocals_path

# =====================
# Feature 추출
# =====================
def extract_features(y, sr):
    features = {}

    # 음정(Pitch) 추출
    f0, _, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7")
    )
    features["f0"] = np.nan_to_num(f0)

    # 에너지(RMS) 추출
    features["rms"] = librosa.feature.rms(y=y)[0]

    # MFCC 추출
    features["mfcc"] = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # 기타 스펙트럴 특징
    features["spectral_centroid"] = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    features["spectral_bandwidth"] = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    features["spectral_rolloff"] = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    features["zcr"] = librosa.feature.zero_crossing_rate(y)[0]

    return features


# =====================
# 파일 처리 메인 로직
# =====================
def process_one_file(audio_dir, wav_name):
    # 경로 결합 시 절대 경로화
    wav_path = os.path.abspath(os.path.join(audio_dir, wav_name))
    name = os.path.splitext(wav_name)[0]

    print(f"\n--- [START] {wav_name} 분석 시작 ---")

    # 1) 보컬 분리
    try:
        vocals_path = separate_vocals(wav_path)
    except Exception as e:
        print(f"[ERROR] Demucs 분리 실패: {e}")
        return

    # 2) 파일 로드 및 전처리
    if not os.path.exists(vocals_path):
        print(f"[SKIP] vocals.mp3를 찾을 수 없음: {vocals_path}")
        return

    # librosa로 로드 (FFmpeg가 설치되어 있어야 함)
    y, sr = librosa.load(vocals_path, sr=SR, mono=True)
    
    # 무음 제거 (trim)
    y, _ = librosa.effects.trim(y, top_db=20)

    if len(y) < sr:
        print(f"[SKIP] 유효한 음성 구간이 너무 짧음 (1초 미만)")
        return

    # 3) 특징 추출
    features = extract_features(y, sr)

    # 4) 저장
    out_dir = os.path.abspath(os.path.join(FEATURE_DIR, name))
    os.makedirs(out_dir, exist_ok=True)

    for k, v in features.items():
        np.save(os.path.join(out_dir, f"{k}.npy"), v)

    print(f"[DONE] 분석 성공! 특징 저장 완료 → {out_dir}")


# =====================
# 외부 호출용 (analyze_voice_final.py 연동)
# =====================
def extract_single_wav(wav_path):
    """
    외부에서 절대경로 또는 상대경로를 주면 분석을 수행함
    """
    abs_path = os.path.abspath(wav_path)
    process_one_file(
        os.path.dirname(abs_path),
        os.path.basename(abs_path)
    )


# =====================
# 단독 실행 테스트
# =====================
if __name__ == "__main__":
    if not os.path.exists(AUDIO_DIR):
        print(f"[ERROR] {AUDIO_DIR} 폴더가 없습니다. 폴더를 생성해주세요.")
    else:
        for f in os.listdir(AUDIO_DIR):
            if f.lower().endswith(".wav"):
                process_one_file(AUDIO_DIR, f)

        print("\n 모든 음성 파일 feature 추출 프로세스 종료")