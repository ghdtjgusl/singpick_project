import os
import json
import numpy as np

# ===============================
# 1. Feature 로드
# ===============================

def load_basic_features(feature_dir):
    """
    features/voice_name/ 안의 npy 파일을 불러와
    평균 음정, 평균 음량, MFCC 평균 벡터를 계산
    """

    f0 = np.load(os.path.join(feature_dir, "f0.npy"))
    rms = np.load(os.path.join(feature_dir, "rms.npy"))
    mfcc = np.load(os.path.join(feature_dir, "mfcc.npy"))

    pitch_avg = float(np.mean(f0)) if len(f0) > 0 else 0.0
    volume_avg = float(np.mean(rms))
    mfcc_mean = np.mean(mfcc, axis=1)

    return pitch_avg, volume_avg, mfcc_mean


# ===============================
# 2. 점수 계산 함수
# ===============================

def calculate_pitch_score(user_pitch, ref_pitch):
    if user_pitch > 0:
        while abs(user_pitch * 2 - ref_pitch) < abs(user_pitch - ref_pitch):
            user_pitch *= 2
        while abs(user_pitch / 2 - ref_pitch) < abs(user_pitch - ref_pitch):
            user_pitch /= 2

    error = abs(user_pitch - ref_pitch)
    score = max(0, 100 - error * 0.5) 
    return round(score, 1)


def calculate_tempo_score(user_bpm, ref_bpm):
    diff = abs(user_bpm - ref_bpm)
    score = max(0, 100 - diff * 1.5)
    return round(score, 1)


def calculate_volume_score(user_volume, ref_volume):
    diff = abs(user_volume - ref_volume)
    score = max(0, 100 - diff * 500)
    return round(score, 1)


# ===============================
# 3. 음색 특징 벡터 생성
# ===============================

def build_timbre_vector(feature_dir):
    """
    MFCC + Spectral Centroid + ZCR
    → 가수 유사도 비교용 벡터
    """

    mfcc = np.load(os.path.join(feature_dir, "mfcc.npy"))
    centroid = np.load(os.path.join(feature_dir, "spectral_centroid.npy"))
    zcr = np.load(os.path.join(feature_dir, "zcr.npy"))

    vector = np.concatenate([
        np.mean(mfcc, axis=1),
        [np.mean(centroid)],
        [np.mean(zcr)]
    ])

    return vector.tolist()


# ===============================
# 4. 전체 분석 함수
# ===============================

def analyze_voice(feature_dir, user_bpm, reference_song_name):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "reference_songs.json")

    with open(json_path, "r", encoding="utf-8") as f:
        reference_db = json.load(f)

    if reference_song_name not in reference_db:
        raise ValueError("기준곡 이름이 reference_songs.json에 없습니다.")

    ref = reference_db[reference_song_name]

    pitch_avg, volume_avg, _ = load_basic_features(feature_dir)

    result = {
        "scores": {
            "pitch": calculate_pitch_score(pitch_avg, ref["pitch_hz_avg"]),
            "tempo": calculate_tempo_score(user_bpm, ref["tempo_bpm"]),
            "volume": calculate_volume_score(volume_avg, ref["volume_rms_avg"])
        },
        "analysis_values": {
            "pitch_hz_avg": round(pitch_avg, 2),
            "tempo_bpm": round(user_bpm, 2),
            "volume_rms_avg": round(volume_avg, 4)
        },
        "timbre_vector": build_timbre_vector(feature_dir)
    }

    return result


# ===============================
# 5. 실행부
# ===============================

if __name__ == "__main__":
    FEATURE_DIR = "features/voice6_big"
    USER_BPM = 129.19921875
    REFERENCE_SONG = "No_Doubt"

    result = analyze_voice(
        feature_dir=FEATURE_DIR,
        user_bpm=USER_BPM,
        reference_song_name=REFERENCE_SONG
    )

    os.makedirs("results", exist_ok=True)

    with open("results/analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("분석 완료 → results/analysis_result.json 생성")
