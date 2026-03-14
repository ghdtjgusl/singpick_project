import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QGridLayout, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
import requests

# ================= 키보드 =================
class NumberKeyboard(QWidget):
    def __init__(self, target: QLineEdit):
        super().__init__()
        self.target = target
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(15)

        keys = [
            "1","2","3","4","5",
            "6","7","8","9","0","←"
        ]

        positions = [(i, j) for i in range(2) for j in range(6)]

        for pos, key in zip(positions, keys):
            btn = QPushButton(key)
            btn.setFixedSize(56, 48)

            if key == "←":   # 백스페이스
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 20px;
                        font-weight: bold;
                        color: white;
                        background-color: #EB5757;
                        border-radius: 12px;
                        border: none;
                    }
                    QPushButton:pressed {
                        background-color: #C44545;
                    }
                """)
                btn.clicked.connect(lambda _, k=key: self.press(k))

            elif key == "":  # 빈 칸
                btn.setEnabled(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                    }
                """)

            else:  # 숫자 키
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        font-weight: bold;
                        color: #212121;
                        background-color: #E0E0E0;
                        border-radius: 12px;
                        border: 1px solid #BDBDBD;
                    }
                    QPushButton:pressed {
                        background-color: #BDBDBD;
                    }
                """)
                btn.clicked.connect(lambda _, k=key: self.press(k))

            grid.addWidget(btn, *pos)

        self.setLayout(grid)

    def press(self, key):
        if not self.target:
            return

        if key == "←":
            self.target.backspace()
        else:
            self.target.insert(key)


# ---------- 영어 키보드 ----------
class EnglishKeyboard(QWidget):
    def __init__(self, target: QLineEdit = None):
        super().__init__()
        self.target = target
        self.init_ui()

    def set_target(self, target):
        self.target = target

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        keys = [
            "Q","W","E","R","T","Y","U","I","O","P",
            "A","S","D","F","G","H","J","K","L","",
            "Z","X","C","V","B","N","M","","","←"
        ]

        positions = [(i, j) for i in range(3) for j in range(10)]

        for pos, key in zip(positions, keys):
            btn = QPushButton(key)
            btn.setFixedSize(56, 48)

            if key == "←":   # 백스페이스
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 20px;
                        font-weight: bold;
                        color: white;
                        background-color: #EB5757;
                        border-radius: 12px;
                        border: none;
                    }
                    QPushButton:pressed {
                        background-color: #C44545;
                    }
                """)
                btn.clicked.connect(lambda _, k=key: self.press(k))

            elif key == "":  # 빈 칸
                btn.setEnabled(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                    }
                """)

            else:  # 일반 키
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 18px;
                        font-weight: bold;
                        color: #212121;
                        background-color: #E0E0E0;
                        border-radius: 12px;
                        border: 1px solid #BDBDBD;
                    }
                    QPushButton:pressed {
                        background-color: #BDBDBD;
                    }
                """)
                btn.clicked.connect(lambda _, k=key: self.press(k))

            grid.addWidget(btn, *pos)

        self.setLayout(grid)

    def press(self, key):
        if not self.target:
            return

        if key == "←":
            self.target.backspace()
        else:
            self.target.insert(key)



# ================= 홈 =================
class HomePage(QWidget):
    def __init__(self, go_signup, go_login, go_guest):
        super().__init__()
        self.go_signup = go_signup
        self.go_login = go_login
        self.go_guest = go_guest
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.notice = QLabel("")
        self.notice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notice.setStyleSheet("font-size:20px; color:green;")

        logo = QLabel("SINGPICK")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("font-size:40px; font-weight:bold; color:black")

        btn_signup = QPushButton("회원가입")
        btn_login = QPushButton("회원")
        btn_guest = QPushButton("비회원")

        btn_signup.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #2F80ED;   /* 메인 블루 */
                border-radius: 14px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #1C5DB6;
            }
        """)

        btn_login.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background-color: #27AE60;   /* 초록 */
                border-radius: 14px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #1E874B;
            }
        """)

        btn_guest.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background-color: #828282;   /* 그레이 */
                border-radius: 14px;
                border: none;
            }
            QPushButton:pressed {
                background-color: #5F5F5F;
            }
        """)


        btn_signup.setFixedSize(300, 55)
        btn_login.setFixedSize(140, 55)
        btn_guest.setFixedSize(140, 55)

        btn_signup.clicked.connect(self.go_signup)
        btn_login.clicked.connect(self.go_login)
        btn_guest.clicked.connect(self.go_guest)

        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(btn_login)
        h.addWidget(btn_guest)
        h.addStretch()

        layout.addWidget(self.notice)
        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(btn_signup, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(h)
        layout.addStretch()

        self.setLayout(layout)

    def show_notice(self):
        self.notice.setText("부스로 입장해주세요.")
        QTimer.singleShot(5000, lambda: self.notice.setText(""))


# ================= 회원가입 =================
class SignUpPage(QWidget):
    def __init__(self, go_home):
        super().__init__()
        self.go_home = go_home
        self.current_input = None
        self.init_ui()
        self.reset()

    def on_home_clicked(self):
        self.reset()      # 입력값 + 키보드 전부 초기화
        self.go_home()    # 홈으로 이동


    def reset(self):
        self.user_id_input.clear()
        self.phone_input.clear()
        self.password_input.clear()
        
        self.current_input = None

        while self.kb_box.count():
            item = self.kb_box.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def init_ui(self):
        main = QVBoxLayout()
        main.setSpacing(20)

        title = QLabel("회원가입")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:28px; font-weight: bold; color: black;")

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("    아이디")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("    전화번호 (숫자 11자리)")
        self.phone_input.setMaxLength(11)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("    비밀번호 (숫자 6자리)")
        self.password_input.setMaxLength(6)

        for i in (self.user_id_input, self.phone_input, self.password_input):
            i.setFixedHeight(25)
            i.setStyleSheet("""
                QLineEdit {
                    font-size: 15px;
                    padding-left: 10px;
                    background-color: #F2F2F2;
                    border: 2px solid #BDBDBD;
                    border-radius: 8px;
                    color: #212121;              /* 실제 입력 글자 색 */
                }                   
                QLineEdit::placeholder {
                    color: black;}             /* 아이디 / 비번 / 전번 글자 색 */
                QLineEdit:focus {
                    background-color: #FFFFFF;
                    border: 2px solid #2F80ED;
                }
            """)


        # 키보드 (숫자, 영어))
        self.num_kb = NumberKeyboard(None)
        self.eng_kb = EnglishKeyboard()

        self.kb_box = QVBoxLayout()

        # 입력칸 클릭 이벤트
        self.user_id_input.mousePressEvent = lambda e: self.show_eng(self.user_id_input)
        self.phone_input.mousePressEvent = lambda e: self.show_num(self.phone_input)
        self.password_input.mousePressEvent = lambda e: self.show_num(self.password_input)

        btn_home = QPushButton("홈")
        btn_submit = QPushButton("등록")

        for btn in (btn_submit, btn_home):
            btn.setFixedSize(120, 45)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                    background-color: #213555;
                    border-radius: 12px;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: #068FFF;
                }
            """)

                
        btn_home.setFixedSize(140, 45)
        btn_submit.setFixedSize(140, 45)

        btn_home.clicked.connect(self.on_home_clicked)
        btn_submit.clicked.connect(self.submit)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_submit)
        btn_row.addWidget(btn_home)

        main.addWidget(title)
        main.addWidget(self.user_id_input)
        main.addWidget(self.phone_input)
        main.addWidget(self.password_input)
        main.addLayout(self.kb_box)
        main.addLayout(btn_row)

        self.setLayout(main)

    # ---------- 키보드 제어 ----------
    def clear_kb(self):
        while self.kb_box.count():
            self.kb_box.takeAt(0).widget().setParent(None)

    def show_eng(self, target):
        self.current_input = target
        self.clear_kb()
        self.eng_kb.set_target(target)
        self.kb_box.addWidget(self.eng_kb)

    def show_num(self, target):
        self.current_input = target
        self.clear_kb()
        self.num_kb.target = target
        self.kb_box.addWidget(self.num_kb)

    def submit(self):
        # 1. 입력값 가져오기
        user_id = self.user_id_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()

        # 2. 유효성 검사 (서버 에러 방지용)
        # 아이디가 영어로만 4~20자인지 체크 (숫자 섞이면 서버에서 422 에러 남)
        if not (user_id.isalpha() and 4 <= len(user_id) <= 20):
            print(f"오류: 아이디 '{user_id}'는 영문 4~20자만 가능합니다.")
            return

        if len(phone) != 11 or not phone.isdigit():
            print("오류: 전화번호 11자리를 입력하세요.")
            return

        if len(password) != 6 or not password.isdigit():
            print("오류: 비밀번호 6자리를 입력하세요.")
            return

        # 3. 서버로 보낼 데이터 뭉치 만들기
        payload = {
            "user_id": user_id,
            "phone": phone,
            "password": password
        }

        try:
            # 4. 서버(main.py)에 데이터 쏘기
            url = "http://127.0.0.1:8000/users/signup"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                print("✅ 회원가입 성공!")
                self.go_home() # 성공하면 홈으로
            else:
                # 서버에서 보낸 에러 메시지 출력 (중복 가입 등)
                print(f"❌ 가입 실패: {response.json()}")
                
        except Exception as e:
            print(f"📡 서버 연결 실패 (서버가 켜져있나요?): {e}")


# ================= 회원 로그인 =================
class LoginPage(QWidget):
    def reset(self):
        self.phone.clear()
        self.password.clear()

        # 키보드도 치워주면 UX 좋음
        while self.kb_box.count():
            self.kb_box.takeAt(0).widget().setParent(None)

    def on_home_clicked(self):
        self.reset()
        self.go_home()

    def __init__(self, go_home, go_song):
        super().__init__()
        self.go_home = go_home
        self.go_song = go_song
        self.current_input = None
        self.init_ui()
        self.reset()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("회원 로그인")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:28px; color: black; font-weight: bold;")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("    전화번호 (숫자 11자리)")
        self.phone.setMaxLength(11)

        self.password = QLineEdit()
        self.password.setPlaceholderText("    비밀번호 (숫자 6자리)")
        self.password.setMaxLength(6)

        for w in (self.phone, self.password):
            w.setFixedHeight(40)
            w.setStyleSheet("""
                QLineEdit {
                    font-size: 15px;
                    padding-left: 10px;
                    background-color: #F2F2F2;
                    border: 2px solid #BDBDBD;
                    border-radius: 8px;
                    color: #212121;              /* 실제 입력 글자 색 */
                }
                QLineEdit::placeholder {
                    color: black;                /* 전화번호 / 비밀번호 글자 색 */
                }
                QLineEdit:focus {
                    background-color: #FFFFFF;
                    border: 2px solid #2F80ED;
                }
            """)
        
        # 숫자 키보드만
        self.num_kb = NumberKeyboard(None)
        self.kb_box = QVBoxLayout()

        # 클릭 이벤트
        self.phone.mousePressEvent = lambda e: self.show_num(self.phone)
        self.password.mousePressEvent = lambda e: self.show_num(self.password)

        

        btn_ok = QPushButton("확인")
        btn_home = QPushButton("홈")

        btn_style = """
        QPushButton {
                    background-color: #213555;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background-color: #068FFF;
                }
                QPushButton:pressed {
                    background-color: #068FFF;
                }
        """

        btn_ok.setStyleSheet(btn_style)
        btn_home.setStyleSheet(btn_style)


        btn_ok.setFixedSize(140, 45)
        btn_home.setFixedSize(140, 45)

        btn_ok.clicked.connect(self.check)
        btn_home.clicked.connect(self.on_home_clicked)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_home)

        layout.addWidget(title)
        layout.addWidget(self.phone)
        layout.addWidget(self.password)
        layout.addLayout(self.kb_box)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    # ---------- 키보드 제어 ----------
    def clear_kb(self):
        while self.kb_box.count():
            self.kb_box.takeAt(0).widget().setParent(None)

    def show_num(self, target):
        self.current_input = target
        self.clear_kb()
        self.num_kb.target = target
        self.kb_box.addWidget(self.num_kb)

class LoginPage(QWidget):
    def __init__(self, go_home, go_song):
        super().__init__()
        self.go_home = go_home
        self.go_song = go_song
        self.current_input = None
        self.fail_count = 0  # 🔹 실패 횟수 카운터 초기화
        self.init_ui()
        self.reset()

    def reset(self):
        self.phone.clear()
        self.password.clear()
        self.fail_count = 0  # 페이지 진입 시 초기화
        while self.kb_box.count():
            item = self.kb_box.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def on_home_clicked(self):
        self.reset()
        self.go_home()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("회원 로그인")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:28px; color: black; font-weight: bold;")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("    전화번호 (숫자 11자리)")
        self.phone.setMaxLength(11)

        self.password = QLineEdit()
        self.password.setPlaceholderText("    비밀번호 (숫자 6자리)")
        self.password.setMaxLength(6)

        for w in (self.phone, self.password):
            w.setFixedHeight(40)
            w.setStyleSheet("""
                QLineEdit {
                    font-size: 15px;
                    padding-left: 10px;
                    background-color: #F2F2F2;
                    border: 2px solid #BDBDBD;
                    border-radius: 8px;
                    color: #212121;
                }
                QLineEdit::placeholder { color: black; }
                QLineEdit:focus {
                    background-color: #FFFFFF;
                    border: 2px solid #2F80ED;
                }
            """)
        
        self.num_kb = NumberKeyboard(None)
        self.kb_box = QVBoxLayout()

        self.phone.mousePressEvent = lambda e: self.show_num(self.phone)
        self.password.mousePressEvent = lambda e: self.show_num(self.password)

        btn_ok = QPushButton("확인")
        btn_home = QPushButton("홈")

        btn_style = """
            QPushButton {
                background-color: #213555;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 12px;
            }
            QPushButton:pressed { background-color: #068FFF; }
        """
        btn_ok.setStyleSheet(btn_style)
        btn_home.setStyleSheet(btn_style)
        btn_ok.setFixedSize(140, 45)
        btn_home.setFixedSize(140, 45)

        btn_ok.clicked.connect(self.check)
        btn_home.clicked.connect(self.on_home_clicked)

        btn_row = QHBoxLayout()
        btn_row.addWidget(btn_ok)
        btn_row.addWidget(btn_home)

        layout.addWidget(title)
        layout.addWidget(self.phone)
        layout.addWidget(self.password)
        layout.addLayout(self.kb_box)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def clear_kb(self):
        while self.kb_box.count():
            item = self.kb_box.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def show_num(self, target):
        self.current_input = target
        self.clear_kb()
        self.num_kb.target = target
        self.kb_box.addWidget(self.num_kb)

    # ---------- 로그인 체크 및 서버 연동 ----------
    # kiosk.py 의 LoginPage 클래스 내 check 함수
    def check(self):
        import requests
        phone = self.phone.text().strip()
        password = self.password.text().strip()

        payload = {
            "phone": phone,  # 서버가 이 값을 암호화해서 phone 컬럼과 대조함
            "password": password
        }

        print(f"--- 로그인 시도 중: {phone} ---") # 확인용

        try:
            url = "http://127.0.0.1:8000/users/login"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                print("✅ 로그인 성공!")

                self.parent().current_user_phone = phone

                self.fail_count = 0
                self.go_song()
            elif response.status_code == 401:
                self.fail_count += 1
                print(f"❌ 로그인 실패 ({self.fail_count}회)")
                if self.fail_count >= 5:
                    print("⚠️ 5회 실패! 위로 멘트가 필요합니다.")
            else:
                print(f"❓ 서버 응답 오류 ({response.status_code}): {response.text}")

        except Exception as e:
            print(f"📡 연결 자체가 안 됨: {e}")


# ================= 곡 수 선택 =================
class SongSelectPage(QWidget):
    def reset(self):
        self.count = 0
        self.update()
        self.notice.hide()

    def __init__(self, go_home):
        super().__init__()
        self.go_home = go_home
        self.count = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 20, 0, 40)

        # 🔹 제목
        title = QLabel("곡 수 선택")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: black;
        """)

        # 안내 문구 (처음엔 숨김)
        self.notice = QLabel("최대 3곡까지 선택 가능합니다.")
        self.notice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notice.setStyleSheet("""
            font-size: 16px;
            color: #D32F2F;
            font-weight: bold;
        """)
        self.notice.hide()

        # 3초 타이머
        self.notice_timer = QTimer()
        self.notice_timer.setSingleShot(True)
        self.notice_timer.timeout.connect(self.notice.hide)

        # 곡 수 표시
        self.label = QLabel("0 곡")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size:32px; color:#394867;")

        # 버튼
        btn_plus = QPushButton("+")
        btn_minus = QPushButton("-")

        for btn in (btn_plus, btn_minus):
            btn.setFixedSize(90, 90)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 42px;
                    font-weight: bold;
                    color: white;
                    background-color: #2F80ED;
                    border-radius: 45px;
                }
                QPushButton:pressed {
                    background-color: #1C5DB6;
                }
            """)

        btn_plus.clicked.connect(self.plus)
        btn_minus.clicked.connect(self.minus)

        count_row = QHBoxLayout()
        count_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_row.setSpacing(60)
        count_row.addWidget(btn_minus)
        count_row.addWidget(self.label)
        count_row.addWidget(btn_plus)

        # 하단 버튼
        btn_select = QPushButton("선택")
        btn_home = QPushButton("홈")

        btn_style = """
            QPushButton {
                background-color: #213555;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 12px;
            }
            QPushButton:pressed {
                background-color: #068FFF;
            }
        """

        for btn in (btn_select, btn_home):
            btn.setFixedSize(120, 45)
            btn.setStyleSheet(btn_style)

        btn_select.clicked.connect(self.select)
        btn_home.clicked.connect(self.go_home)

        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(40)
        btn_row.addWidget(btn_select)
        btn_row.addWidget(btn_home)

        layout.addWidget(title)
        layout.addWidget(self.notice)
        layout.addLayout(count_row)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    # 안내 표시 (3초)
    def show_notice(self):
        self.notice.show()
        self.notice_timer.start(3000)

    def update(self):
        self.label.setText(f"{self.count} 곡")

    def plus(self):
        if self.count < 3:
            self.count += 1
            self.update()
            if self.count == 3:
                self.show_notice()

    def minus(self):
        if self.count > 0:
            self.count -= 1
            self.update()

    def select(self):
        if 1 <= self.count <= 3:

            payload = {
             "phone": self.parent().current_user_phone,
             "song_count": self.count
          }

        try:
            res = requests.post(
                "http://127.0.0.1:8000/kiosk/entry",
                json=payload
            )
            print("서버 응답:", res.json())

        except Exception as e:
            print("서버 연결 실패:", e)

        self.go_home(from_song=True)

    def show_song(self):
        if not hasattr(self, "song"):
            self.song = SongSelectPage(self.go_home)
            self.stack.addWidget(self.song)

        self.song.reset()


# ================= 메인 화면 =================
class KioskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SingPick Kiosk")
        self.setFixedSize(800, 480)

        self.stack = QStackedWidget()
        self.init_pages()

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.setStyleSheet("background-color:#DDE6ED;")


    def init_pages(self):
        self.home = HomePage(self.show_signup, self.show_login, self.show_song)
        self.signup = SignUpPage(self.show_home)
        self.login = LoginPage(self.show_home, self.show_song)
        self.song = SongSelectPage(self.finish)

        for p in (self.home, self.signup, self.login, self.song):
            self.stack.addWidget(p)

    def show_home(self):
        self.stack.setCurrentWidget(self.home)

    def show_signup(self):
        self.signup.reset() 
        self.stack.setCurrentWidget(self.signup)

    def show_login(self):
        self.login.reset() 
        self.stack.setCurrentWidget(self.login)

    def show_song(self):
        self.song.reset()
        self.stack.setCurrentWidget(self.song)

    def finish(self, from_song=False):
        self.stack.setCurrentWidget(self.home)
        if from_song:
            self.home.show_notice()


# ================= 실행 =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KioskApp()
    win.show()
    sys.exit(app.exec())