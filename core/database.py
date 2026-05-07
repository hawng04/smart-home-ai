# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Thay root và password bằng user/pass MySQL của bạn. 
# 3306 là port mặc định, smart_home_db là tên database vừa tạo.
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/smart_home_db"

# Tạo Engine kết nối
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo Session để thực hiện các giao dịch (thêm, sửa, xóa)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class để các Model kế thừa
Base = declarative_base()

# Hàm tạo Session cho mỗi Request (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()