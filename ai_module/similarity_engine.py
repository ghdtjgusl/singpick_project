import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

current_dir = os.path.dirname(os.path.abspath(__file__))
SINGER_DB_DIR = os.path.join(current_dir, "singer_db")

# ===============================
# 1. singer_db 로드
# ===============================
def load_singer_db(db_dir=SINGER_DB_DIR): 
    singers = []
    
    # 폴더가 존재하는지 한 번 더 체크 (방어적 코드)
    if not os.path.exists(db_dir):
        print(f"⚠️ [Warning] DB 폴더를 찾을 수 없습니다: {db_dir}")
        return singers

    for file in os.listdir(db_dir):
        if file.endswith(".json"):
            path = os.path.join(db_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                singers.append(json.load(f))

    return singers


# ===============================
# 2. 코사인 유사도 계산
# ===============================
def calculate_similarity(user_vector, singer_vector):
    user_vec = np.array(user_vector).reshape(1, -1)
    singer_vec = np.array(singer_vector).reshape(1, -1)

    similarity = cosine_similarity(user_vec, singer_vec)[0][0]
    return round(float(similarity), 4)


# ===============================
# 3. Top-N 추천
# ===============================
def recommend_singers(user_vector, top_n=3):
    singer_db = load_singer_db()
    results = []

    for singer in singer_db:
        sim_score = calculate_similarity(
            user_vector,
            singer["timbre_vector"]
        )

        results.append({
            "singer": singer["singer"],
            "similarity": sim_score
        })

    # 유사도 높은 순 정렬
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_n]


# ===============================
# 4. 단독 실행 테스트
# ===============================
if __name__ == "__main__":
    # 테스트용: 임시 벡터 (실제론 analyze_voice 결과 사용)
    dummy_vector = np.random.rand(15).tolist()

    recs = recommend_singers(dummy_vector, top_n=5)

    print(" 추천 가수 결과")
    for r in recs:
        print(r)
