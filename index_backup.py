## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLineEdit

class MyApp(QMainWindow):
    # 초기화 함수
    def __init__(self):
        super().__init__()
        self.current_tab = 0
        self.initUI()

    # 창 설정 함수
    def initUI(self):
        self.setWindowTitle('Livescore_tool_v1.0')
        self.setWindowIcon(QIcon('./assets/images/rocket.png'))
        self.move(300, 150)
        self.resize(1280, 960)
        self.center()





        # 탭 컨테이너
        self.tab_container = QWidget()
        self.tab_container.setFixedHeight(50)
        self.tab_container.setStyleSheet("""
            QWidget {
                background-color: #fff;
                border: 2px dashed #d0d0d0;
                border-radius: 25px;
            }
        """)
        
        tab_layout = QHBoxLayout(self.tab_container)
        tab_layout.setContentsMargins(5, 5, 5, 5)
        tab_layout.setSpacing(0)
        
        # 탭 버튼들 생성
        self.tab_buttons = []
        self.tab_contents = []
        
        tab_data = [("홈", "home"), ("감지목록", "detect")]
        
        for i, (text, tab_type) in enumerate(tab_data):
            button = QPushButton(text)
            button.setFixedHeight(40)
            button.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            self.tab_buttons.append(button)
            
            # 탭 타입에 따라 다른 콘텐츠 생성
            content = self.create_tab_content(tab_type)
            self.tab_contents.append(content)
            
            tab_layout.addWidget(button)
        
        # 기존 버튼들 (알림/신고 목록, 프록시 불러오기)
        report = QPushButton("알림/신고 목록")
        proxy = QPushButton("프록시 불러오기")
        proxycount = QLabel("0개 불러옴")
        
        tab_layout.addWidget(report)
        tab_layout.addWidget(proxy)
        tab_layout.addWidget(proxycount)
        
        

        # 탭 컨테이너를 윈도우에 추가하고 위치 설정
        self.tab_container.setParent(self)
        self.tab_container.move(0, 20)  # 위치 설정
        self.tab_container.resize(1280, 60)  # 크기 설정








        
        startbutton = QPushButton("시작")
        stopbutton = QPushButton("정지")

        startbutton.setStyleSheet("""
            QPushButton {
                width: 100px;
                height: 30px;
                background-color: #0078d4;
                color: white;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        stopbutton.setStyleSheet("""
            QPushButton {
                width: 100px;
                height: 30px;
                background-color: #0078d4;
                color: white;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # 체크박스들 생성
        checkbutton1 = QCheckBox("자동댓글(알림용)")
        checkbutton2 = QCheckBox("자동댓글(신고용)")
        checkbutton3 = QCheckBox("신고활성화")
        checkbutton4 = QCheckBox("신고활성화(앱)")
        checkbutton5 = QCheckBox("소리활성화")
        checkbutton6 = QCheckBox("팝업활성화")
        checkbutton7 = QCheckBox("텔레그램활성화")
        checkbutton8 = QCheckBox("프록시활성화")


        
        tg_apikey_label = QLabel("텔레그램 API KEY")
        tg_apikey_label.resize(139, 30)  # 크기 직접 설정
        tg_apikey_label.setStyleSheet("""    
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        password_label = QLabel("암호 변경")
        password_label.resize(139, 30)  # 크기 직접 설정
        password_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)



        tg_apikey_input = QLineEdit()
        tg_apikey_input.resize(100, 30)
        tg_apikey_input.setStyleSheet("""    
            QLineEdit {
                font-size: 12px;
                background-color: white;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        tg_apikey_button = QPushButton("적용")
        tg_apikey_button.resize(40, 30)
        tg_apikey_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: white;
        tg_apikey_button.setPlaceholderText("텔레그램 API KEY")
        """)
        tg_apikey_button.setParent(styled_box3)
        tg_apikey_button.move(20, 260)

        password_input = QLineEdit()
        password_input.resize(100, 30)
        password_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: white;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        password_button = QPushButton("ChatID")
        password_button.resize(40, 30)
        password_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
            }
        """)
        password_button.setParent(styled_box3)
        password_button.move(150, 260)

        # 모든 요소를 styled_box3에 추가하고 절대 위치 설정
        startbutton.setParent(styled_box3)
        stopbutton.setParent(styled_box3)
        startbutton.resize(100, 30)
        stopbutton.resize(100, 30)
        startbutton.move(20, 20)  # 버튼 위치
        stopbutton.move(130, 20)
        
        # 체크박스들 위치 설정
        checkbutton1.setParent(styled_box3)
        checkbutton1.move(20, 70)
        checkbutton2.setParent(styled_box3)
        checkbutton2.move(150, 70)
        checkbutton3.setParent(styled_box3)
        checkbutton3.move(20, 100)
        checkbutton4.setParent(styled_box3)
        checkbutton4.move(150, 100)
        checkbutton5.setParent(styled_box3)
        checkbutton5.move(20, 130)
        checkbutton6.setParent(styled_box3)
        checkbutton6.move(150, 130)
        checkbutton7.setParent(styled_box3)
        checkbutton7.move(20, 160)
        checkbutton8.setParent(styled_box3)
        checkbutton8.move(150, 160)
        
        # 라벨과 입력필드 위치 설정
        tg_apikey_label.setParent(styled_box3)
        password_label.setParent(styled_box3)
        tg_apikey_label.move(10, 200)
        password_label.move(150, 200)

        tg_apikey_input.setParent(styled_box3)
        password_input.setParent(styled_box3)
        tg_apikey_input.move(10, 230)
        password_input.move(150, 230)

        tg_apikey_button.setParent(styled_box3)
        password_button.setParent(styled_box3)
        tg_apikey_button.move(110, 230)
        password_button.move(250, 230)


        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box3.setParent(self)
        styled_box3.move(0, 130)  # 위치 설정 (원래 위치로 복원)
        styled_box3.resize(300, 800)  # 크기 설정


        styled_box4 = QWidget()
        styled_box4.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)






        styled_layout4 = QHBoxLayout()
        styled_box4.setLayout(styled_layout4)


        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box4.setParent(self)
        styled_box4.move(300, 130)  # 위치 설정
        styled_box4.resize(300, 800)  # 크기 설정


        styled_box5 = QWidget()
        styled_box5.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)


        styled_layout5 = QHBoxLayout()
        styled_box5.setLayout(styled_layout5)


        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box5.setParent(self)
        styled_box5.move(600, 130)  # 위치 설정
        styled_box5.resize(680, 400)  # 크기 설정





        styled_box6 = QWidget()
        styled_box6.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)


        styled_layout6 = QHBoxLayout()
        styled_box6.setLayout(styled_layout6)




        delay_label = QLabel("딜레이 (초)")
        delay_label.resize(90, 30)  # 크기 직접 설정
        delay_label.setStyleSheet("""    
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        auto_comment_label = QLabel("자동댓글수")
        auto_comment_label.resize(90, 30)  # 크기 직접 설정
        auto_comment_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        delay_input = QLineEdit()
        delay_input.resize(50, 30)
        delay_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: white;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        auto_comment_input = QLineEdit()
        auto_comment_input.resize(50, 30)
        auto_comment_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: white;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)

        delay_label.setParent(styled_box3)
        auto_comment_label.setParent(styled_box3)
        delay_input.setParent(styled_box3)
        auto_comment_input.setParent(styled_box3)
        delay_label.move(10, 265)
        delay_input.move(100, 265)
        auto_comment_label.move(150, 265)
        auto_comment_input.move(240, 265)






        # 상용구 박스 생성
        preset_phrase_box = QWidget()
        preset_phrase_box.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #ffffff;
                padding: 10px;
            }
        """)
        preset_phrase_box.setParent(styled_box3)
        preset_phrase_box.move(10, 345)
        preset_phrase_box.resize(280, 450)

        preset_phrase_label = QLabel("상용구")
        preset_phrase_label.resize(90, 30)  # 크기 직접 설젱
        preset_phrase_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        preset_phrase_label.setParent(styled_box3)
        preset_phrase_label.move(10, 310)



        preset_phrase_add_button = QPushButton("추가")
        preset_phrase_add_button.resize(40, 30)  # 크기 직접 설젱
        preset_phrase_add_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        preset_phrase_add_button.setParent(styled_box3)
        preset_phrase_add_button.move(210, 310)


        preset_phrase_delete_button = QPushButton("삭제")
        preset_phrase_delete_button.resize(40, 30)  # 크기 직접 설젱
        preset_phrase_delete_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                background-color: #f0f8ff;
                border: 1px solid #0078d4;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        preset_phrase_delete_button.setParent(styled_box3)
        preset_phrase_delete_button.move(250, 310)



        # 체크박스들 생성
        preset_phrase_checkallbutton = QCheckBox("전체선택")
        preset_phrase_checkallbutton.resize(100, 30)
        preset_phrase_checkallbutton.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton1   = QCheckBox("안녕하세요")
        preset_phrase_checkbutton1.resize(100, 30)
        preset_phrase_checkbutton1.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton2 = QCheckBox("ㅋㅋㅋㅋㅋㅋ")
        preset_phrase_checkbutton2.resize(100, 30)
        preset_phrase_checkbutton2.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton3 = QCheckBox("ㅎㅇㅎㅇ")
        preset_phrase_checkbutton3.resize(100, 30)
        preset_phrase_checkbutton3.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton4 = QCheckBox("아싸~!")
        preset_phrase_checkbutton4.resize(100, 30)
        preset_phrase_checkbutton4.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)

        preset_phrase_checkallbutton.setParent(preset_phrase_box)
        preset_phrase_checkallbutton.move(10, 30)
        preset_phrase_checkbutton1.setParent(preset_phrase_box)
        preset_phrase_checkbutton1.move(10, 60)
        preset_phrase_checkbutton2.setParent(preset_phrase_box)
        preset_phrase_checkbutton2.move(10, 90)
        preset_phrase_checkbutton3.setParent(preset_phrase_box)
        preset_phrase_checkbutton3.move(10, 120)
        preset_phrase_checkbutton4.setParent(preset_phrase_box)
        preset_phrase_checkbutton4.move(10, 150)



        # 체크박스들 작성버튼
        
        preset_phrase_write_button1 = QPushButton("작성")
        preset_phrase_write_button1.resize(50, 28)
        preset_phrase_write_button1.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 0px;
            }
        """)
        
        preset_phrase_write_button2 = QPushButton("작성")
        preset_phrase_write_button2.resize(50, 28)
        preset_phrase_write_button2.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 0px;
            }
        """)
        
        preset_phrase_write_button3 = QPushButton("작성")
        preset_phrase_write_button3.resize(50, 28)
        preset_phrase_write_button3.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 0px;
            }
        """)
        
        preset_phrase_write_button4 = QPushButton("작성")
        preset_phrase_write_button4.resize(50, 28)
        preset_phrase_write_button4.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 0px;
            }
        """)
               

        preset_phrase_write_button1.setParent(preset_phrase_box)
        preset_phrase_write_button1.move(210, 61)
        preset_phrase_write_button2.setParent(preset_phrase_box)
        preset_phrase_write_button2.move(210, 91)
        preset_phrase_write_button3.setParent(preset_phrase_box)
        preset_phrase_write_button3.move(210, 121)
        preset_phrase_write_button4.setParent(preset_phrase_box)
        preset_phrase_write_button4.move(210, 151)
        


        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box6.setParent(self)
        styled_box6.move(600, 530)  # 위치 설정
        styled_box6.resize(680, 400)  # 크기 설정

        # 탭 초기 설정
        self.setup_tabs()
        
        self.show()

    def create_tab_content(self, tab_type):
        """탭 타입에 따라 다른 콘텐츠 생성"""
        content_widget = QWidget()
        content_widget.setParent(self)
        content_widget.move(0, 100)  # 탭 아래 위치
        content_widget.resize(1280, 860)  # 전체 크기
        
        if tab_type == "home":
            # 홈 탭: 기존의 모든 콘텐츠
            self.create_home_content(content_widget)
        elif tab_type == "detect":
            # 감지목록 탭: 감지 관련 콘텐츠
            self.create_detect_content(content_widget)
        
        return content_widget

    def create_home_content(self, parent):
        """홈 탭 콘텐츠 생성"""
        # 기존의 모든 styled_box들을 홈 탭에 추가
        # styled_box2
        styled_box2 = QWidget()
        banlist = QLabel('차단 목록')
        banlist.setStyleSheet("""
            QLabel {
                margin-left: 390px;
            }
        """)
        reportlist = QLabel('신고 계정 목록 / 댓글 계정 목록')
        reportlist.setStyleSheet("""
            QLabel {
                margin-left: 60px;
            }
        """)
        styled_layout2 = QHBoxLayout()
        styled_box2.setLayout(styled_layout2)
        styled_layout2.addWidget(banlist)
        styled_layout2.addWidget(reportlist)
        styled_box2.setParent(parent)
        styled_box2.move(0, 0)
        styled_box2.resize(1280, 40)

        # styled_box3 (왼쪽 컨트롤 패널)
        styled_box3 = QWidget()
        styled_box3.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 1px;
            }
        """)
        styled_box3.setParent(parent)
        styled_box3.move(0, 30)
        styled_box3.resize(300, 800)
        
        # styled_box3의 모든 콘텐츠를 여기에 추가
        self.add_control_panel_content(styled_box3)

        # styled_box4 (중간 패널)
        styled_box4 = QWidget()
        styled_box4.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)
        styled_box4.setParent(parent)
        styled_box4.move(300, 30)
        styled_box4.resize(300, 800)

        # styled_box5 (오른쪽 패널)
        styled_box5 = QWidget()
        styled_box5.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)
        styled_box5.setParent(parent)
        styled_box5.move(600, 30)
        styled_box5.resize(680, 400)

        # styled_box6 (하단 패널)
        styled_box6 = QWidget()
        styled_box6.setStyleSheet("""
            QWidget {
                border: 2px solid #0078d4;
                border-radius: 5px;
                background-color: #f0f8ff;
                padding: 10px;
            }
        """)
        styled_box6.setParent(parent)
        styled_box6.move(600, 430)
        styled_box6.resize(680, 400)

    def create_detect_content(self, parent):
        """감지목록 탭 콘텐츠 생성"""
        # 감지목록 전용 콘텐츠
        title = QLabel("감지목록")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        title.setParent(parent)
        title.move(50, 50)
        title.resize(200, 40)
        
        # 감지목록 리스트 (예시)
        detect_list = QLabel("감지된 항목들이 여기에 표시됩니다.")
        detect_list.setParent(parent)
        detect_list.move(50, 100)
        detect_list.resize(600, 200)
        detect_list.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                padding: 10px;
                background-color: white;
            }
        """)

    def add_control_panel_content(self, parent):
        """컨트롤 패널 콘텐츠 추가"""
        # 시작/정지 버튼
        startbutton = QPushButton("시작")
        stopbutton = QPushButton("정지")
        
        startbutton.setStyleSheet("""
            QPushButton {
                width: 100px;
                height: 30px;
                background-color: #0078d4;
                color: white;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        stopbutton.setStyleSheet("""
            QPushButton {
                width: 100px;
                height: 30px;
                background-color: #0078d4;
                color: white;
                border-radius: 5px;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        startbutton.setParent(parent)
        stopbutton.setParent(parent)
        startbutton.resize(100, 30)
        stopbutton.resize(100, 30)
        startbutton.move(20, 20)
        stopbutton.move(130, 20)
        
        # 체크박스들
        checkbutton1 = QCheckBox("자동댓글(알림용)")
        checkbutton2 = QCheckBox("자동댓글(신고용)")
        checkbutton3 = QCheckBox("신고활성화")
        checkbutton4 = QCheckBox("신고활성화(앱)")
        checkbutton5 = QCheckBox("소리활성화")
        checkbutton6 = QCheckBox("팝업활성화")
        checkbutton7 = QCheckBox("텔레그램활성화")
        checkbutton8 = QCheckBox("프록시활성화")
        
        checkbutton1.setParent(parent)
        checkbutton1.move(20, 70)
        checkbutton2.setParent(parent)
        checkbutton2.move(150, 70)
        checkbutton3.setParent(parent)
        checkbutton3.move(20, 100)
        checkbutton4.setParent(parent)
        checkbutton4.move(150, 100)
        checkbutton5.setParent(parent)
        checkbutton5.move(20, 130)
        checkbutton6.setParent(parent)
        checkbutton6.move(150, 130)
        checkbutton7.setParent(parent)
        checkbutton7.move(20, 160)
        checkbutton8.setParent(parent)
        checkbutton8.move(150, 160)

    def setup_tabs(self):
        """탭 초기 설정"""
        # 초기 상태: 첫 번째 탭만 보이게 설정
        for i, content in enumerate(self.tab_contents):
            content.setVisible(i == 0)
        
        # 첫 번째 버튼을 선택된 상태로 설정
        for i, button in enumerate(self.tab_buttons):
            button.setStyleSheet(self.get_button_style(i == 0))

    def get_button_style(self, is_selected):
        """버튼 스타일 반환"""
        if is_selected:
            return """
                QPushButton {
                    background-color: #e0e0e0;
                    color: #0066cc;
                    border: none;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    color: #666666;
                    border: none;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """

    def switch_tab(self, index):
        """탭 전환"""
        if self.current_tab == index:
            return
            
        self.current_tab = index
        
        # 콘텐츠 전환
        for i, content in enumerate(self.tab_contents):
            content.setVisible(i == index)
        
        # 버튼 스타일 업데이트
        for i, button in enumerate(self.tab_buttons):
            button.setStyleSheet(self.get_button_style(i == index))

    # 창을 가운데 위치시키는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# 메인 함수
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
