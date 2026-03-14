import requests
import threading
import time

# 목표: 100명이 동시에 "아이유"를 검색하는 상황 시뮬레이션
URL = "http://127.0.0.1:8000/library/search"
PARAMS = {"keyword": "아이유"}

# 성공/실패 횟수 카운트
success_count = 0
fail_count = 0

def attack_server(user_id):
    global success_count, fail_count
    try:
        start_time = time.time()
        response = requests.get(URL, params=PARAMS)
        end_time = time.time()
        
        if response.status_code == 200:
            success_count += 1
            print(f"✅ [User {user_id}] 검색 성공! (소요시간: {end_time - start_time:.4f}초)")
        else:
            fail_count += 1
            print(f"🔥 [User {user_id}] 에러 발생: {response.status_code}")
    except Exception as e:
        fail_count += 1
        print(f"💀 [User {user_id}] 접속 실패 (서버 다운됨?): {e}")

# 100명의 유저(스레드) 준비
threads = []
print("부하 테스트 시작! (가상 사용자 100명 투입)")
start_total = time.time()

for i in range(100):
    t = threading.Thread(target=attack_server, args=(i,))
    threads.append(t)
    t.start() # 공격 시작

# 모든 유저의 작업이 끝날 때까지 대기
for t in threads:
    t.join()

end_total = time.time()

print("\n" + "="*30)
print(f"📊 테스트 결과 리포트")
print(f"총 소요 시간: {end_total - start_total:.4f}초")
print(f"성공: {success_count}회")
print(f"실패: {fail_count}회")
print("="*30)

if fail_count == 0:
    print("🏆 서버 Good! (모두 정상 처리)")
else:
    print("⚠️ 서버가 힘들어하고 있습니다.")