from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 형식: mysql+pymysql://아이디:비밀번호@주소:포트/데이터베이스이름
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/singpick_db"

# 2. 엔진 생성 (파이썬과 DB를 연결하는 자동차 엔진)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. 세션 생성 (DB와 대화하는 통로)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델 베이스 (테이블 만드는 틀)
Base = declarative_base()

# 5. DB 세션 가져오기 함수 (나중에 API에서 씁니다)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()