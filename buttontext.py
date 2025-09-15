import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt 탭 메뉴 예제")
        self.setGeometry(100, 100, 600, 400)
        self.current_tab = 0
        
        self.setup_ui()
        self.setup_tabs()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 세그먼트 컨트롤
        self.segment_container = QWidget()
        self.segment_container.setFixedHeight(50)
        self.segment_container.setStyleSheet("""
            QWidget {
                background-color: #fff;
                border: 2px dashed #d0d0d0;
                border-radius: 25px;
            }
        """)
        
        segment_layout = QHBoxLayout(self.segment_container)
        segment_layout.setContentsMargins(5, 5, 5, 5)
        segment_layout.setSpacing(0)
        
        # 버튼 생성
        self.buttons = []
        self.contents = []
        
        tab_data = [("홈", "home"), ("입력폼", "form"), ("설정", "settings")]
        
        for i, (text, tab_type) in enumerate(tab_data):
            button = QPushButton(text)
            button.setFixedHeight(40)
            button.clicked.connect(lambda checked, idx=i: self.switch_tab(idx))
            self.buttons.append(button)
            
            # 탭 타입에 따라 다른 콘텐츠 생성
            content = self.create_tab_content(tab_type)
            self.contents.append(content)
            
            segment_layout.addWidget(button)
        
        main_layout.addWidget(self.segment_container)
        main_layout.addSpacing(20)

        # 콘텐츠 영역
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        for content in self.contents:
            self.content_layout.addWidget(content)
        
        main_layout.addWidget(self.content_widget)

    def create_tab_content(self, tab_type):
        """탭 타입에 따라 다른 콘텐츠 생성"""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        if tab_type == "home":
            # 홈 탭: 간단한 라벨과 버튼들
            title = QLabel("홈 화면")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
            layout.addWidget(title)
            
            welcome = QLabel("환영합니다! 다양한 위젯 예제를 확인해보세요.")
            welcome.setAlignment(Qt.AlignCenter)
            welcome.setStyleSheet("font-size: 16px; color: #666; margin-bottom: 30px;")
            layout.addWidget(welcome)
            
            # 버튼들
            btn_layout = QHBoxLayout()
            btn1 = QPushButton("새로고침")
            btn2 = QPushButton("도움말")
            btn3 = QPushButton("정보")
            
            btn_layout.addWidget(btn1)
            btn_layout.addWidget(btn2)
            btn_layout.addWidget(btn3)
            layout.addLayout(btn_layout)
            
        elif tab_type == "form":
            # 입력폼 탭: 다양한 입력 위젯들
            title = QLabel("입력 폼")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
            layout.addWidget(title)
            
            # 이름 입력
            name_label = QLabel("이름:")
            name_input = QLineEdit()
            name_input.setPlaceholderText("이름을 입력하세요")
            layout.addWidget(name_label)
            layout.addWidget(name_input)
            
            # 나이 입력
            age_label = QLabel("나이:")
            age_spin = QSpinBox()
            age_spin.setRange(1, 100)
            age_spin.setValue(25)
            layout.addWidget(age_label)
            layout.addWidget(age_spin)
            
            # 성별 선택
            gender_label = QLabel("성별:")
            gender_combo = QComboBox()
            gender_combo.addItems(["남성", "여성", "기타"])
            layout.addWidget(gender_label)
            layout.addWidget(gender_combo)
            
            # 체크박스
            check_label = QLabel("약관 동의:")
            agree_check = QCheckBox("개인정보 처리방침에 동의합니다")
            layout.addWidget(check_label)
            layout.addWidget(agree_check)
            
            # 텍스트 영역
            text_label = QLabel("메모:")
            text_area = QTextEdit()
            text_area.setPlaceholderText("추가 메모를 입력하세요...")
            text_area.setMaximumHeight(100)
            layout.addWidget(text_label)
            layout.addWidget(text_area)
            
            # 제출 버튼
            submit_btn = QPushButton("제출")
            submit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            layout.addWidget(submit_btn)
            
        elif tab_type == "settings":
            # 설정 탭: 설정 옵션들
            title = QLabel("설정")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
            layout.addWidget(title)
            
            # 테마 설정
            theme_label = QLabel("테마:")
            theme_combo = QComboBox()
            theme_combo.addItems(["라이트", "다크", "자동"])
            layout.addWidget(theme_label)
            layout.addWidget(theme_combo)
            
            # 언어 설정
            lang_label = QLabel("언어:")
            lang_combo = QComboBox()
            lang_combo.addItems(["한국어", "English", "日本語"])
            layout.addWidget(lang_label)
            layout.addWidget(lang_combo)
            
            # 알림 설정
            notif_label = QLabel("알림 설정:")
            notif_check1 = QCheckBox("이메일 알림")
            notif_check2 = QCheckBox("푸시 알림")
            notif_check3 = QCheckBox("SMS 알림")
            layout.addWidget(notif_label)
            layout.addWidget(notif_check1)
            layout.addWidget(notif_check2)
            layout.addWidget(notif_check3)
            
            # 저장 버튼
            save_btn = QPushButton("설정 저장")
            save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            layout.addWidget(save_btn)
        
        return content_widget

    def setup_tabs(self):
        # 초기 상태: 첫 번째 탭만 보이게 설정
        for i, content in enumerate(self.contents):
            content.setVisible(i == 0)
        
        # 첫 번째 버튼을 선택된 상태로 설정
        for i, button in enumerate(self.buttons):
            button.setStyleSheet(self.get_button_style(i == 0))

    def get_button_style(self, is_selected):
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
        if self.current_tab == index:
            return
            
        self.current_tab = index
        
        # 콘텐츠 전환
        for i, content in enumerate(self.contents):
            content.setVisible(i == index)
        
        # 버튼 스타일 업데이트
        for i, button in enumerate(self.buttons):
            button.setStyleSheet(self.get_button_style(i == index))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
