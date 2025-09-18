## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QCheckBox
from PyQt5.QtGui import QIcon, QRegion, QPainterPath
from PyQt5.QtCore import QCoreApplication, Qt, QRectF
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRect, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QFont

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.is_hovered = False
        self.is_pressed = False
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(100)  # 50ms마다 업데이트
        self.animation_frame = 0
        
        # 스케일 애니메이션을 위한 속성
        self._scale_factor = 1.0
        self.scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation.setDuration(50)  # 150ms 애니메이션
        self.scale_animation.setEasingCurve(QEasingCurve.Linear)
        
        # 기본 스타일 설정
        self.setStyleSheet("""
            QPushButton {
                background-color: #212121;
                border: 4px solid transparent;
                border-radius: 30px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
        """)
    
    def update_animation(self):
        self.animation_frame += 1
        self.update()  # 페인트 이벤트 발생
    
    @pyqtProperty(float)
    def scale_factor(self):
        return self._scale_factor
    
    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self.update()
    
    def animate_scale(self, target_scale):
        """스케일 애니메이션 실행"""
        self.scale_animation.stop()
        self.scale_animation.setStartValue(self._scale_factor)
        self.scale_animation.setEndValue(target_scale)
        self.scale_animation.start()
    
    def enterEvent(self, event):
        self.is_hovered = True
        self.animate_scale(1)  # 호버 시 1% 확대
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.is_hovered = False
        self.animate_scale(1)  # 원래 크기로 복원
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        self.is_pressed = True
        self.animate_scale(0.985)  # 클릭 시 5% 축소
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.is_pressed = False
        if self.is_hovered:
            self.animate_scale(1)  # 호버 상태라면 1% 확대
        else:
            self.animate_scale(1)  # 아니면 원래 크기
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # 애니메이션된 스케일 적용
        if self._scale_factor != 1.0:
            center_x = rect.width() / 2
            center_y = rect.height() / 2
            new_width = int(rect.width() * self._scale_factor)
            new_height = int(rect.height() * self._scale_factor)
            new_rect = QRect(
                int(center_x - new_width // 2),
                int(center_y - new_height // 2),
                new_width,
                new_height
            )
            rect = new_rect
        
        # 그라데이션 테두리 그리기
        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        
        # 애니메이션에 따른 그라데이션 위치 변경
        offset = (self.animation_frame % 100) / 100.0
        
        # 색상 위치를 0-1 범위로 제한
        positions = [
            (0.0 + offset) % 1.0,
            (0.25 + offset) % 1.0,
            (0.5 + offset) % 1.0,
            (0.75 + offset) % 1.0,
            (1.0 + offset) % 1.0
        ]
        
        # 중복 제거 및 정렬
        unique_positions = []
        for pos in positions:
            if pos not in unique_positions:
                unique_positions.append(pos)
        unique_positions.sort()
        
        # 색상 설정 (노란색 → 분홍색 → 파란색)
        colors = [
            QColor(255, 219, 59),   # #ffdb3b (노란색)
            QColor(254, 83, 186),   # #fe53bb (분홍색)
            QColor(143, 81, 234),   # #8f51ea (보라색)
            QColor(0, 68, 255),     # #0044ff (파란색)
            QColor(255, 219, 59)    # #ffdb3b (노란색)
        ]
        
        for i, pos in enumerate(unique_positions):
            gradient.setColorAt(pos, colors[i % len(colors)])
        
        # 테두리 그리기 (그라데이션)
        pen_width = 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        
        # 호버 상태에 따라 다른 border-radius 적용
        if self.is_hovered:
            # 호버 시 사각형 (border-radius = 0)
            painter.drawRoundedRect(rect, 0, 0)
        else:
            # 일반 상태는 둥근 모서리
            painter.drawRoundedRect(rect, 5, 5)
        
        # 내부 배경 (클릭 상태에 따라 색상 변경)
        inner_rect = rect.adjusted(pen_width, pen_width, -pen_width, -pen_width)
        if self.is_pressed:
            # 클릭 시 더 밝은 색상
            painter.setBrush(QColor(60, 60, 60))  # 더 밝은 회색
        else:
            # 일반 상태
            painter.setBrush(QColor(33, 33, 33))  # #212121
        
        # 내부 배경도 호버 상태에 따라 다른 border-radius 적용
        if self.is_hovered:
            # 호버 시 사각형 (border-radius = 0)
            painter.drawRoundedRect(inner_rect, 0, 0)
        else:
            # 일반 상태는 둥근 모서리
            painter.drawRoundedRect(inner_rect, 5, 5)
        
        # 텍스트 그리기
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        
        # 별 효과 (호버 시)
        if self.is_hovered:
            self.draw_stars(painter, rect)
    
    def draw_stars(self, painter, rect):
        # 별들을 그리기
        painter.setPen(QColor(255, 255, 255, 200))
        for i in range(20):
            x = (rect.x() + i * 15 + self.animation_frame * 2) % rect.width()
            y = rect.y() + (i * 7) % rect.height()
            painter.drawPoint(x, y)

class MyApp(QMainWindow):
    # 초기화 함수
    def __init__(self):
        super().__init__()
        self.initUI()

    # 창 설정 함수
    def initUI(self):
        self.setWindowTitle('Livescore_tool_v1.0')
        self.setWindowIcon(QIcon('./assets/images/rocket.png'))
        self.move(300, 150)
        self.resize(1800, 960)
        
        # 커스텀 타이틀바 설정
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # 메인 윈도우 배경 설정 (타이틀바와 동일한 그라데이션)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border-radius: 10px;
            }
        """)
        
        # 커스텀 타이틀바 생성
        self.create_custom_titlebar()
        
        self.center()

        # UI 구성
        self.setup_top_menu()
        self.setup_home_ui()
        self.setup_detect_ui()
        self.setup_tabs()
        self.show()





    # 상단 메뉴 설정
    def setup_top_menu(self):
        # CSS 스타일 박스 - 전체 컨테이너
        styled_box1 = QWidget()
        styled_box1.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: 2px solid #8707ff;
                border-radius: 5px;
                padding: 10px;
                color: white;
            }
        """)
        styled_layout = QHBoxLayout(styled_box1)
        styled_layout.setContentsMargins(5, 5, 5, 5)
        styled_layout.setSpacing(10)
        
        # 탭 컨테이너 (홈/감지목록만)
        tab_container = QWidget()
        tab_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: 2px dashed #d0d0d0;
                border-radius: 25px;
                color: white;
            }
        """)
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(5, 5, 5, 5)
        tab_layout.setSpacing(0)
        
        # 탭 버튼들 (홈/감지목록만)
        self.tab_buttons = []
        self.current_tab = 0
        
        home = QPushButton("홈")
        home.setFixedHeight(40)
        home.clicked.connect(lambda: self.switch_tab(0))
        self.tab_buttons.append(home)
        
        detect = QPushButton("감지목록")
        detect.setFixedHeight(40)
        detect.clicked.connect(lambda: self.switch_tab(1))
        self.tab_buttons.append(detect)
        
        # 탭 레이아웃에 버튼들 추가
        tab_layout.addWidget(home)
        tab_layout.addWidget(detect)
        
        # 일반 버튼들 (탭에서 분리)
        report = CustomButton("알림/신고 목록")
        report.setFixedHeight(40)
        report.clicked.connect(self.show_report_popup)  # 팝업 이벤트 연결
        
        proxy = CustomButton("프록시 불러오기")
        proxy.setFixedHeight(40)
        proxy.clicked.connect(self.load_proxy_file)  # 파일 선택 이벤트 연결
        
        proxycount = QLabel("0개 불러옴")
        proxycount.setStyleSheet("""
            QLabel {
                font-size: 12px;
                border: none;
                padding: 20px;
                margin-top: 20px;
                margin-right: 400px;
                color: white;
            }
        """)
        proxycount.setFixedHeight(40)
        proxycount.setAlignment(Qt.AlignCenter)
        
        # 전체 레이아웃에 탭 컨테이너와 일반 버튼들 추가
        styled_layout.addWidget(tab_container)
        styled_layout.addWidget(report)
        styled_layout.addWidget(proxy)
        styled_layout.addWidget(proxycount)

        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box1.setParent(self)
        styled_box1.move(0, 40)  # 타이틀바 아래로 위치 조정
        styled_box1.resize(1800, 60)  # 크기 설정

    # 홈화면 UI 설정
    def setup_home_ui(self):
        # 탭 콘텐츠 위젯들 생성
        self.tab_content_widgets = []
        
        # 홈 탭은 기존 박스들만 사용 (콘텐츠 위젯 없음)
        self.tab_content_widgets.append(None)  # 홈 탭은 None으로 표시
        
        # 홈화면의 모든 박스들 생성
        self.create_home_boxes()
        
        # 탭 콘텐츠를 윈도우에 추가하고 위치 설정
        for i, content_widget in enumerate(self.tab_content_widgets):
            if content_widget is not None:  # None이 아닌 경우만 처리
                content_widget.setParent(self)
                if i == 0:  # 홈 탭
                    content_widget.move(300, 150)  # styled_box4 위치와 동일
                    content_widget.resize(300, 800)  # styled_box4 크기와 동일
                if i != 0:  # 첫 번째 탭(홈)만 보이게 설정
                    content_widget.hide()

    # 홈화면의 박스들 생성
    def create_home_boxes(self):
        # styled_box2 생성
        styled_box2 = QWidget()

        banlist = QLabel('차단 목록')
        banlist.setStyleSheet("""
            QLabel {
                margin-left: 300px;
                font-weight: bold;
                color: white;
            }
        """)

        reportblock = CustomButton("신고계정차단")

        
        reportblock.setFixedSize(120, 30)
        reportblock.setParent(self)  # 부모를 메인 윈도우로 변경
        reportblock.move(508, 119)  # 타이틀바 아래로 위치 조정
        reportblock.raise_()  # 버튼을 맨 앞으로 가져오기
        reportblock.show()  # 버튼을 보이게 하기
        self.reportblock = reportblock  # 인스턴스 변수로 저장


        clearbutton = CustomButton("비우기")
        clearbutton.setFixedSize(80, 30) 
        clearbutton.setParent(self)  # 부모를 메인 윈도우로 변경
        clearbutton.move(630, 119)  # 타이틀바 아래로 위치 조정
        clearbutton.raise_()  # 버튼을 맨 앞으로 가져오기
        clearbutton.show()  # 버튼을 보이게 하기
        self.clearbutton = clearbutton  # 인스턴스 변수로 저장
        reportlist = QLabel('신고 계정 목록 / 댓글 계정 목록')
        reportlist.setStyleSheet("""
            QLabel {
                margin-left: 700px;
                font-weight: bold;
                color: white;
            }
        """)

        styled_layout2 = QHBoxLayout()
        styled_box2.setLayout(styled_layout2)


        # 레이아웃에 버튼들 추가 (reportblock과 clearbutton은 제외)
        styled_layout2.addWidget(banlist)
        styled_layout2.addWidget(reportlist)

        # 스타일 박스를 윈도우에 추가하고 위치 설정
        styled_box2.setParent(self)
        styled_box2.move(0, 120)  # 타이틀바와 메뉴들 아래로 위치 조정
        styled_box2.resize(1800, 40)  # 크기 설정
        styled_box2.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 마우스 이벤트 비활성화
        
        # styled_box2를 참조용으로 저장
        self.styled_box2 = styled_box2




        styled_box3 = QWidget()
        styled_box3.setStyleSheet("""
            QWidget {
                border: 2px solid #8707ff;
                border-radius: 5px;
                background-color: transparent;
                padding: 1px;
                color: white;
            }
        """)



        
        # ===== 시작/정지 버튼 관련 코드 =====
        startbutton = CustomButton("시작")
        stopbutton = CustomButton("정지")
        
        # 시작/정지 버튼 위치 설정
        startbutton.setParent(styled_box3)
        stopbutton.setParent(styled_box3)
        startbutton.resize(125, 30)
        stopbutton.resize(125, 30)
        startbutton.move(20, 20)
        stopbutton.move(155, 20)

        # ===== 체크박스들 관련 코드 =====
        checkbutton1 = QCheckBox("자동댓글(알림용)")
        checkbutton1.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton2 = QCheckBox("자동댓글(신고용)")
        checkbutton2.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton3 = QCheckBox("신고활성화")
        checkbutton3.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton4 = QCheckBox("신고활성화(앱)")
        checkbutton4.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton5 = QCheckBox("소리활성화")
        checkbutton5.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton6 = QCheckBox("팝업활성화")
        checkbutton6.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton7 = QCheckBox("텔레그램활성화")
        checkbutton7.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        checkbutton8 = QCheckBox("프록시활성화")
        checkbutton8.setStyleSheet("""
            QCheckBox {
                border: none;
            }
        """)
        
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


        # ===== 텔레그램 API 관련 코드 =====
        # 텔레그램 API 라벨
        tg_apikey_label = QLabel("텔레그램 API KEY")
        tg_apikey_label.resize(139, 30)
        tg_apikey_label.setStyleSheet("""    
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        tg_apikey_label.setParent(styled_box3)
        tg_apikey_label.move(10, 200)

        # ChatID 라벨
        password_label = QLabel("암호 변경")
        password_label.resize(139, 30)
        password_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        password_label.setParent(styled_box3)
        password_label.move(150, 200)

        # 텔레그램 API 입력 필드
        tg_apikey_input = QLineEdit()
        tg_apikey_input.resize(90, 30)
        tg_apikey_input.setStyleSheet("""    
            QLineEdit {
                font-size: 12px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        tg_apikey_input.setParent(styled_box3)
        tg_apikey_input.move(10, 230)

        # ChatID 입력 필드
        password_input = QLineEdit()
        password_input.resize(90, 30)
        password_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        password_input.setParent(styled_box3)
        password_input.move(150, 230)

        # 적용 버튼
        tg_apikey_button = QPushButton("적용")
        tg_apikey_button.resize(50, 30)
        tg_apikey_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f8ff;
            }
            QPushButton:pressed {
                background-color: #e6f3ff;
                border: 2px solid #8707ff;
            }
        """)
        tg_apikey_button.setParent(styled_box3)
        tg_apikey_button.move(100, 230)

        # ChatID 버튼
        password_button = QPushButton("ChatID")
        password_button.resize(50, 30)
        password_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f8ff;
            }
            QPushButton:pressed {
                background-color: #e6f3ff;
                border: 2px solid #8707ff;
            }
        """)
        password_button.setParent(styled_box3)
        password_button.move(240, 230)

        # ===== 딜레이/자동댓글 관련 코드 =====
        delay_label = QLabel("딜레이 (초)")
        delay_label.resize(90, 30)
        delay_label.setStyleSheet("""    
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        delay_label.setParent(styled_box3)
        delay_label.move(10, 265)

        auto_comment_label = QLabel("자동댓글수")
        auto_comment_label.resize(90, 30)
        auto_comment_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        auto_comment_label.setParent(styled_box3)
        auto_comment_label.move(150, 265)

        delay_input = QLineEdit()
        delay_input.resize(50, 30)
        delay_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        delay_input.setParent(styled_box3)
        delay_input.move(100, 265)
        
        auto_comment_input = QLineEdit()
        auto_comment_input.resize(50, 30)
        auto_comment_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                background-color: transparent;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        auto_comment_input.setParent(styled_box3)
        auto_comment_input.move(240, 265)


        # ===== 박스 레이아웃 관련 코드 =====
        # styled_box3 (왼쪽 컨트롤 박스) 설정
        styled_box3.setParent(self)
        styled_box3.move(10, 150)  # 타이틀바와 메뉴들 아래로 위치 조정
        styled_box3.resize(300, 800)
        self.styled_box3 = styled_box3


        # styled_box4 (차단 목록 박스) 설정
        styled_box4 = QWidget()
        styled_box4.setStyleSheet("""
            QWidget {
                border: 2px solid #8707ff;
                border-radius: 5px;
                background-color: transparent;
                padding: 10px;
            }
        """)
        styled_layout4 = QHBoxLayout()
        styled_box4.setLayout(styled_layout4)
        styled_box4.setParent(self)
        styled_box4.move(310, 150)  # 타이틀바와 메뉴들 아래로 위치 조정
        styled_box4.resize(400, 800)
        self.styled_box4 = styled_box4


        # styled_box5 (신고 계정 목록 박스) 설정
        styled_box5 = QWidget()
        styled_box5.setStyleSheet("""
            QWidget {
                border: 2px solid #8707ff;
                border-radius: 5px;
                background-color: transparent;
                padding: 10px;
            }
        """)
        styled_layout5 = QHBoxLayout()
        styled_box5.setLayout(styled_layout5)
        styled_box5.setParent(self)
        styled_box5.move(710, 150)  # 타이틀바와 메뉴들 아래로 위치 조정
        styled_box5.resize(1080, 400)
        self.styled_box5 = styled_box5





        # styled_box6 (하단 박스) 설정
        styled_box6 = QWidget()
        styled_box6.setStyleSheet("""
            QWidget {
                border: 2px solid #8707ff;
                border-radius: 5px;
                background-color: transparent;
                padding: 10px;
            }
        """)
        styled_layout6 = QHBoxLayout()
        styled_box6.setLayout(styled_layout6)










        # ===== 상용구 관련 코드 =====
        # 상용구 박스 생성
        preset_phrase_box = QWidget()
        preset_phrase_box.setStyleSheet("""
            QWidget {
                border: 2px solid #8707ff;
                border-radius: 5px;
                background-color: transparent;  
                padding: 10px;
            }
        """)
        preset_phrase_box.setParent(styled_box3)
        preset_phrase_box.move(10, 345)
        preset_phrase_box.resize(280, 450)

        # 상용구 라벨
        preset_phrase_label = QLabel("상용구")
        preset_phrase_label.resize(90, 30)
        preset_phrase_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }
        """)
        preset_phrase_label.setParent(styled_box3)
        preset_phrase_label.move(10, 315)

        # 추가/삭제 버튼
        preset_phrase_add_button = CustomButton("추가")
        preset_phrase_add_button.resize(40, 30)
        preset_phrase_add_button.setParent(styled_box3)
        preset_phrase_add_button.move(210, 310)

        preset_phrase_delete_button = CustomButton("삭제")
        preset_phrase_delete_button.resize(40, 30)
        preset_phrase_delete_button.setParent(styled_box3)
        preset_phrase_delete_button.move(250, 310)



        # 작성 버튼들은 CustomButton 사용

        # 상용구 체크박스들 생성
        preset_phrase_checkallbutton = QCheckBox("전체선택")
        preset_phrase_checkallbutton.resize(100, 30)
        preset_phrase_checkallbutton.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkallbutton.setParent(preset_phrase_box)
        preset_phrase_checkallbutton.move(10, 30)

        # 첫 번째 묶음: 안녕하세요 체크박스 + 작성 버튼
        preset_phrase_checkbutton1 = QCheckBox("안녕하세요")
        preset_phrase_checkbutton1.resize(100, 30)
        preset_phrase_checkbutton1.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton1.setParent(preset_phrase_box)
        preset_phrase_checkbutton1.move(10, 60)

        preset_phrase_write_button1 = CustomButton("작성")
        preset_phrase_write_button1.resize(50, 28)
        preset_phrase_write_button1.setParent(preset_phrase_box)
        preset_phrase_write_button1.move(210, 61)

        # 두 번째 묶음: ㅋㅋㅋㅋㅋㅋ 체크박스 + 작성 버튼
        preset_phrase_checkbutton2 = QCheckBox("ㅋㅋㅋㅋㅋㅋ")
        preset_phrase_checkbutton2.resize(100, 30)
        preset_phrase_checkbutton2.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton2.setParent(preset_phrase_box)
        preset_phrase_checkbutton2.move(10, 90)

        preset_phrase_write_button2 = CustomButton("작성")
        preset_phrase_write_button2.resize(50, 28)
        preset_phrase_write_button2.setParent(preset_phrase_box)
        preset_phrase_write_button2.move(210, 91)

        # 세 번째 묶음: ㅎㅇㅎㅇ 체크박스 + 작성 버튼
        preset_phrase_checkbutton3 = QCheckBox("ㅎㅇㅎㅇ")
        preset_phrase_checkbutton3.resize(100, 30)
        preset_phrase_checkbutton3.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton3.setParent(preset_phrase_box)
        preset_phrase_checkbutton3.move(10, 120)

        preset_phrase_write_button3 = CustomButton("작성")
        preset_phrase_write_button3.resize(50, 28)
        preset_phrase_write_button3.setParent(preset_phrase_box)
        preset_phrase_write_button3.move(210, 121)

        # 네 번째 묶음: 아싸~! 체크박스 + 작성 버튼
        preset_phrase_checkbutton4 = QCheckBox("아싸~!")
        preset_phrase_checkbutton4.resize(100, 30)
        preset_phrase_checkbutton4.setStyleSheet("""
            QCheckBox {
                padding: 2px;
            }
        """)
        preset_phrase_checkbutton4.setParent(preset_phrase_box)
        preset_phrase_checkbutton4.move(10, 150)

        preset_phrase_write_button4 = CustomButton("작성")
        preset_phrase_write_button4.resize(50, 28)
        preset_phrase_write_button4.setParent(preset_phrase_box)
        preset_phrase_write_button4.move(210, 151)

        # 체크박스들을 리스트로 저장 (전체선택 기능을 위해)
        self.preset_phrase_checkboxes = [
            preset_phrase_checkbutton1,
            preset_phrase_checkbutton2,
            preset_phrase_checkbutton3,
            preset_phrase_checkbutton4
        ]
        
        # 전체선택 체크박스에 클릭 이벤트 연결
        preset_phrase_checkallbutton.clicked.connect(self.toggle_all_preset_phrases)
        


        styled_box6.setParent(self)
        styled_box6.move(710, 550)  # 타이틀바와 메뉴들 아래로 위치 조정
        styled_box6.resize(1080, 400)
        self.styled_box6 = styled_box6


    # 감지목록화면 UI 설정
    def setup_detect_ui(self):
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton
        
        # 감지목록 탭 콘텐츠 - 전체 화면 구성
        detect_content = QWidget()
        detect_content.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                border: 2px solid #8707ff;
            }
        """)
        
        # 감지목록 메인 컨테이너
        detect_main_container = QWidget()
        detect_main_container.setStyleSheet("""
            QWidget {
                background-color: #fff;
                border: 2px solid #8707ff;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        # 왼쪽 박스 - 일반감지 단어목록
        detect_words_container = QWidget()
        detect_words_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 오른쪽 박스 - 일반감지 단어제외목록
        exclude_words_container = QWidget()
        exclude_words_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 신고감지 단어목록 박스
        report_words_container = QWidget()
        report_words_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 신고감지 제외목록 박스
        report_exclude_container = QWidget()
        report_exclude_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 자동댓글 단어목록 박스
        comment_words_container = QWidget()
        comment_words_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 자동댓글 제외목록 박스
        comment_exclude_container = QWidget()
        comment_exclude_container.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        
        # 제목과 버튼을 담을 컨테이너 위젯
        title_container = QWidget()
        title_container.setParent(detect_words_container)
        title_container.move(0, 0)
        title_container.resize(295, 50)
        
        # 왼쪽 제목 - 일반감지 단어목록
        detect_title = QLabel("일반감지 단어목록")
        detect_title.setParent(title_container)
        detect_title.move(10, 10)
        detect_title.resize(200, 30)
        detect_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #8707ff;
                font-weight: bold;
            }
        """)
        
        # 일반감지 단어목록 추가 버튼
        detect_add_button = QPushButton("추가")
        detect_add_button.setParent(title_container)
        detect_add_button.move(220, 12)
        detect_add_button.resize(50, 25)
        detect_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #8707ff;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
            }
            QPushButton:pressed {
                background-color: #d1e7ff;
                border: 2px solid #8707ff;
            }
        """)
        detect_add_button.clicked.connect(lambda: self.add_word_to_list('detect'))
        
        # 일반감지 단어제외목록 컨테이너
        exclude_title_container = QWidget()
        exclude_title_container.setParent(exclude_words_container)
        exclude_title_container.move(0, 0)
        exclude_title_container.resize(300, 50)
        
        # 오른쪽 제목 - 일반감지 단어제외목록
        exclude_title = QLabel("일반감지 단어제외목록")
        exclude_title.setParent(exclude_title_container)
        exclude_title.move(10, 10)
        exclude_title.resize(200, 30)
        exclude_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                font-weight: bold;
            }
        """)
        
        # 일반감지 단어제외목록 추가 버튼
        exclude_add_button = QPushButton("추가")
        exclude_add_button.setParent(exclude_title_container)
        exclude_add_button.move(220, 12)
        exclude_add_button.resize(50, 25)
        exclude_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #e74c3c;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
            QPushButton:pressed {
                background-color: #ffcccc;
                border: 2px solid #e74c3c;
            }
        """)
        exclude_add_button.clicked.connect(lambda: self.add_word_to_list('exclude'))
        
        # 신고감지 단어목록 컨테이너
        report_title_container = QWidget()
        report_title_container.setParent(report_words_container)
        report_title_container.move(0, 0)
        report_title_container.resize(295, 50)
        
        # 신고감지 단어목록 제목
        report_title = QLabel("신고감지 단어목록")
        report_title.setParent(report_title_container)
        report_title.move(10, 10)
        report_title.resize(200, 30)
        report_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #8e44ad;
                font-weight: bold;
            }
        """)
        
        # 신고감지 단어목록 추가 버튼
        report_add_button = QPushButton("추가")
        report_add_button.setParent(report_title_container)
        report_add_button.move(220, 12)
        report_add_button.resize(50, 25)
        report_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #8e44ad;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #f0e6ff;
            }
            QPushButton:pressed {
                background-color: #e6ccff;
                border: 2px solid #8e44ad;
            }
        """)
        report_add_button.clicked.connect(lambda: self.add_word_to_list('report'))
        
        # 신고감지 제외목록 컨테이너
        report_exclude_title_container = QWidget()
        report_exclude_title_container.setParent(report_exclude_container)
        report_exclude_title_container.move(0, 0)
        report_exclude_title_container.resize(295, 50)
        
        # 신고감지 제외목록 제목
        report_exclude_title = QLabel("신고감지 제외목록")
        report_exclude_title.setParent(report_exclude_title_container)
        report_exclude_title.move(10, 10)
        report_exclude_title.resize(200, 30)
        report_exclude_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #c0392b;
                font-weight: bold;
            }
        """)
        
        # 신고감지 제외목록 추가 버튼
        report_exclude_add_button = QPushButton("추가")
        report_exclude_add_button.setParent(report_exclude_title_container)
        report_exclude_add_button.move(220, 12)
        report_exclude_add_button.resize(50, 25)
        report_exclude_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #c0392b;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
            QPushButton:pressed {
                background-color: #ffcccc;
                border: 2px solid #c0392b;
            }
        """)
        report_exclude_add_button.clicked.connect(lambda: self.add_word_to_list('report_exclude'))
        
        # 자동댓글 단어목록 컨테이너
        comment_title_container = QWidget()
        comment_title_container.setParent(comment_words_container)
        comment_title_container.move(0, 0)
        comment_title_container.resize(295, 50)
        
        # 자동댓글 단어목록 제목
        comment_title = QLabel("자동댓글 단어목록")
        comment_title.setParent(comment_title_container)
        comment_title.move(10, 10)
        comment_title.resize(200, 30)
        comment_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        
        # 자동댓글 단어목록 추가 버튼
        comment_add_button = QPushButton("추가")
        comment_add_button.setParent(comment_title_container)
        comment_add_button.move(220, 12)
        comment_add_button.resize(50, 25)
        comment_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #27ae60;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #e6f7e6;
            }
            QPushButton:pressed {
                background-color: #ccffcc;
                border: 2px solid #27ae60;
            }
        """)
        comment_add_button.clicked.connect(lambda: self.add_word_to_list('comment'))
        
        # 자동댓글 제외목록 컨테이너
        comment_exclude_title_container = QWidget()
        comment_exclude_title_container.setParent(comment_exclude_container)
        comment_exclude_title_container.move(0, 0)
        comment_exclude_title_container.resize(295, 50)
        
        # 자동댓글 제외목록 제목
        comment_exclude_title = QLabel("자동댓글 제외목록")
        comment_exclude_title.setParent(comment_exclude_title_container)
        comment_exclude_title.move(10, 10)
        comment_exclude_title.resize(200, 30)
        comment_exclude_title.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #d35400;
                font-weight: bold;
            }
        """)
        
        # 자동댓글 제외목록 추가 버튼
        comment_exclude_add_button = QPushButton("추가")
        comment_exclude_add_button.setParent(comment_exclude_title_container)
        comment_exclude_add_button.move(220, 12)
        comment_exclude_add_button.resize(50, 25)
        comment_exclude_add_button.setStyleSheet("""
            QPushButton {
                font-size: 11px;
                background-color: #f0f8ff;
                border: 1px solid #d35400;
                border-radius: 3px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #fff0e6;
            }
            QPushButton:pressed {
                background-color: #ffe6cc;
                border: 2px solid #d35400;
            }
        """)
        comment_exclude_add_button.clicked.connect(lambda: self.add_word_to_list('comment_exclude'))
        
        # 일반감지 단어목록 테이블
        self.detect_table = QTableWidget()
        self.detect_table.setParent(detect_words_container)
        self.detect_table.move(10, 60)
        self.detect_table.resize(275, 300)
        self.detect_table.setColumnCount(2)
        self.detect_table.setColumnWidth(0, 220)
        self.detect_table.setColumnWidth(1, 40)
        self.detect_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.detect_table.horizontalHeader().setStretchLastSection(True)
        self.detect_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.detect_table.setRowCount(0)
        self.detect_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        # search_label = QLabel("검색:")
        # search_label.setParent(detect_words_container)
        # search_label.move(20, 670)
        # search_label.resize(30, 20)
        
        self.detect_search_input = QLineEdit()
        self.detect_search_input.setParent(detect_words_container)
        self.detect_search_input.move(50, 370)
        self.detect_search_input.resize(150, 25)
        self.detect_search_input.setPlaceholderText("단어를 검색하세요...")
        self.detect_search_input.textChanged.connect(lambda: self.search_words('detect'))
        
        # 검색 결과 테이블
        self.detect_search_table = QTableWidget()
        self.detect_search_table.setParent(detect_words_container)
        self.detect_search_table.move(10, 400)
        self.detect_search_table.resize(275, 200)
        self.detect_search_table.setColumnCount(2)
        self.detect_search_table.setColumnWidth(0, 220)
        self.detect_search_table.setColumnWidth(1, 40)
        self.detect_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.detect_search_table.horizontalHeader().setStretchLastSection(True)
        self.detect_search_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.detect_search_table.setRowCount(0)
        self.detect_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 일반감지 단어제외목록 테이블
        self.exclude_table = QTableWidget()
        self.exclude_table.setParent(exclude_words_container)
        self.exclude_table.move(10, 60)
        self.exclude_table.resize(275, 300)
        self.exclude_table.setColumnCount(2)
        self.exclude_table.setColumnWidth(0, 220)
        self.exclude_table.setColumnWidth(1, 40)
        self.exclude_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.exclude_table.horizontalHeader().setStretchLastSection(True)
        self.exclude_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.exclude_table.setRowCount(0)
        self.exclude_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        self.exclude_search_input = QLineEdit()
        self.exclude_search_input.setParent(exclude_words_container)
        self.exclude_search_input.move(50, 370)
        self.exclude_search_input.resize(150, 25)
        self.exclude_search_input.setPlaceholderText("단어를 검색하세요...")
        self.exclude_search_input.textChanged.connect(lambda: self.search_words('exclude'))
        
        # 검색 결과 테이블
        self.exclude_search_table = QTableWidget()
        self.exclude_search_table.setParent(exclude_words_container)
        self.exclude_search_table.move(10, 400)
        self.exclude_search_table.resize(275, 200)
        self.exclude_search_table.setColumnCount(2)
        self.exclude_search_table.setColumnWidth(0, 220)
        self.exclude_search_table.setColumnWidth(1, 40)
        self.exclude_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.exclude_search_table.horizontalHeader().setStretchLastSection(True)
        self.exclude_search_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.exclude_search_table.setRowCount(0)
        self.exclude_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 신고감지 단어목록 테이블
        self.report_table = QTableWidget()
        self.report_table.setParent(report_words_container)
        self.report_table.move(10, 60)
        self.report_table.resize(275, 300)
        self.report_table.setColumnCount(2)
        self.report_table.setColumnWidth(0, 220)
        self.report_table.setColumnWidth(1, 40)
        self.report_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.report_table.horizontalHeader().setStretchLastSection(True)
        self.report_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.report_table.setRowCount(0)
        self.report_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        self.report_search_input = QLineEdit()
        self.report_search_input.setParent(report_words_container)
        self.report_search_input.move(50, 370)
        self.report_search_input.resize(150, 25)
        self.report_search_input.setPlaceholderText("단어를 검색하세요...")
        self.report_search_input.textChanged.connect(lambda: self.search_words('report'))
        
        # 검색 결과 테이블
        self.report_search_table = QTableWidget()
        self.report_search_table.setParent(report_words_container)
        self.report_search_table.move(10, 400)
        self.report_search_table.resize(275, 200)
        self.report_search_table.setColumnCount(2)
        self.report_search_table.setColumnWidth(0, 220)
        self.report_search_table.setColumnWidth(1, 40)
        self.report_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.report_search_table.horizontalHeader().setStretchLastSection(True)
        self.report_search_table.verticalHeader().setVisible(False)  # 행 번호 숨기기
        self.report_search_table.setRowCount(0)
        self.report_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 신고감지 제외목록 테이블
        self.report_exclude_table = QTableWidget()
        self.report_exclude_table.setParent(report_exclude_container)
        self.report_exclude_table.move(10, 60)
        self.report_exclude_table.resize(275, 300)
        self.report_exclude_table.setColumnCount(2)
        self.report_exclude_table.setColumnWidth(0, 220)
        self.report_exclude_table.setColumnWidth(1, 40)
        self.report_exclude_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.report_exclude_table.horizontalHeader().setStretchLastSection(True)
        self.report_exclude_table.verticalHeader().setVisible(False)
        self.report_exclude_table.setRowCount(0)
        self.report_exclude_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        self.report_exclude_search_input = QLineEdit()
        self.report_exclude_search_input.setParent(report_exclude_container)
        self.report_exclude_search_input.move(50, 370)
        self.report_exclude_search_input.resize(150, 25)
        self.report_exclude_search_input.setPlaceholderText("단어를 검색하세요...")
        self.report_exclude_search_input.textChanged.connect(lambda: self.search_words('report_exclude'))
        
        # 검색 결과 테이블
        self.report_exclude_search_table = QTableWidget()
        self.report_exclude_search_table.setParent(report_exclude_container)
        self.report_exclude_search_table.move(10, 400)
        self.report_exclude_search_table.resize(275, 200)
        self.report_exclude_search_table.setColumnCount(2)
        self.report_exclude_search_table.setColumnWidth(0, 220)
        self.report_exclude_search_table.setColumnWidth(1, 40)
        self.report_exclude_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.report_exclude_search_table.horizontalHeader().setStretchLastSection(True)
        self.report_exclude_search_table.verticalHeader().setVisible(False)
        self.report_exclude_search_table.setRowCount(0)
        self.report_exclude_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 자동댓글 단어목록 테이블
        self.comment_table = QTableWidget()
        self.comment_table.setParent(comment_words_container)
        self.comment_table.move(10, 60)
        self.comment_table.resize(275, 300)
        self.comment_table.setColumnCount(2)
        self.comment_table.setColumnWidth(0, 220)
        self.comment_table.setColumnWidth(1, 40)
        self.comment_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.comment_table.horizontalHeader().setStretchLastSection(True)
        self.comment_table.verticalHeader().setVisible(False)
        self.comment_table.setRowCount(0)
        self.comment_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        self.comment_search_input = QLineEdit()
        self.comment_search_input.setParent(comment_words_container)
        self.comment_search_input.move(50, 370)
        self.comment_search_input.resize(150, 25)
        self.comment_search_input.setPlaceholderText("단어를 검색하세요...")
        self.comment_search_input.textChanged.connect(lambda: self.search_words('comment'))
        
        # 검색 결과 테이블
        self.comment_search_table = QTableWidget()
        self.comment_search_table.setParent(comment_words_container)
        self.comment_search_table.move(10, 400)
        self.comment_search_table.resize(275, 200)
        self.comment_search_table.setColumnCount(2)
        self.comment_search_table.setColumnWidth(0, 220)
        self.comment_search_table.setColumnWidth(1, 40)
        self.comment_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.comment_search_table.horizontalHeader().setStretchLastSection(True)
        self.comment_search_table.verticalHeader().setVisible(False)
        self.comment_search_table.setRowCount(0)
        self.comment_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 자동댓글 제외목록 테이블
        self.comment_exclude_table = QTableWidget()
        self.comment_exclude_table.setParent(comment_exclude_container)
        self.comment_exclude_table.move(10, 60)
        self.comment_exclude_table.resize(275, 300)
        self.comment_exclude_table.setColumnCount(2)
        self.comment_exclude_table.setColumnWidth(0, 220)
        self.comment_exclude_table.setColumnWidth(1, 40)
        self.comment_exclude_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.comment_exclude_table.horizontalHeader().setStretchLastSection(True)
        self.comment_exclude_table.verticalHeader().setVisible(False)
        self.comment_exclude_table.setRowCount(0)
        self.comment_exclude_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # 검색 입력 필드
        self.comment_exclude_search_input = QLineEdit()
        self.comment_exclude_search_input.setParent(comment_exclude_container)
        self.comment_exclude_search_input.move(50, 370)
        self.comment_exclude_search_input.resize(150, 25)
        self.comment_exclude_search_input.setPlaceholderText("단어를 검색하세요...")
        self.comment_exclude_search_input.textChanged.connect(lambda: self.search_words('comment_exclude'))
        
        # 검색 결과 테이블
        self.comment_exclude_search_table = QTableWidget()
        self.comment_exclude_search_table.setParent(comment_exclude_container)
        self.comment_exclude_search_table.move(10, 400)
        self.comment_exclude_search_table.resize(275, 200)
        self.comment_exclude_search_table.setColumnCount(2)
        self.comment_exclude_search_table.setColumnWidth(0, 220)
        self.comment_exclude_search_table.setColumnWidth(1, 40) 
        self.comment_exclude_search_table.setHorizontalHeaderLabels(['단어', '삭제'])
        self.comment_exclude_search_table.horizontalHeader().setStretchLastSection(True)
        self.comment_exclude_search_table.verticalHeader().setVisible(False)
        self.comment_exclude_search_table.setRowCount(0)
        self.comment_exclude_search_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        

        
        # 레이아웃 제거하고 절대 위치로 설정 - 2x3 그리드
        detect_words_container.setParent(detect_main_container)
        exclude_words_container.setParent(detect_main_container)
        report_words_container.setParent(detect_main_container)
        report_exclude_container.setParent(detect_main_container)
        comment_words_container.setParent(detect_main_container)
        comment_exclude_container.setParent(detect_main_container)
        
        # 1행 6열로 박스들 위치 조정
        detect_words_container.move(9, 20)      # (1,1)
        exclude_words_container.move(305, 20)    # (1,2)
        report_words_container.move(606, 20)     # (1,3)
        report_exclude_container.move(902, 20)   # (1,4)
        comment_words_container.move(1198, 20)   # (1,5)
        comment_exclude_container.move(1494, 20) # (1,6)
        
        # 위젯 크기 고정 (각 박스 250x750)
        detect_words_container.setFixedSize(295, 850)
        exclude_words_container.setFixedSize(300, 850)
        report_words_container.setFixedSize(295, 850)
        report_exclude_container.setFixedSize(295, 850)
        comment_words_container.setFixedSize(295, 850)
        comment_exclude_container.setFixedSize(295, 850)
        
        # 각 박스 내부 레이아웃 설정
        detect_left_layout = QVBoxLayout(detect_words_container)
        detect_left_layout.addWidget(title_container)
        detect_left_layout.addWidget(self.detect_table)
        detect_left_layout.addWidget(self.detect_search_input)
        detect_left_layout.addWidget(self.detect_search_table)
        title_container.setFixedSize(295, 50)
        
        exclude_right_layout = QVBoxLayout(exclude_words_container)
        exclude_right_layout.addWidget(exclude_title_container)
        exclude_right_layout.addWidget(self.exclude_table)
        exclude_right_layout.addWidget(self.exclude_search_input)
        exclude_right_layout.addWidget(self.exclude_search_table)
        exclude_title_container.setFixedSize(300, 50)
        
        report_left_layout = QVBoxLayout(report_words_container)
        report_left_layout.addWidget(report_title_container)
        report_left_layout.addWidget(self.report_table)
        report_left_layout.addWidget(self.report_search_input)
        report_left_layout.addWidget(self.report_search_table)
        report_title_container.setFixedSize(295, 50)
        
        report_exclude_layout = QVBoxLayout(report_exclude_container)
        report_exclude_layout.addWidget(report_exclude_title_container)
        report_exclude_layout.addWidget(self.report_exclude_table)
        report_exclude_layout.addWidget(self.report_exclude_search_input)
        report_exclude_layout.addWidget(self.report_exclude_search_table)
        report_exclude_title_container.setFixedSize(295, 50)
        
        comment_left_layout = QVBoxLayout(comment_words_container)
        comment_left_layout.addWidget(comment_title_container)
        comment_left_layout.addWidget(self.comment_table)
        comment_left_layout.addWidget(self.comment_search_input)
        comment_left_layout.addWidget(self.comment_search_table)
        comment_title_container.setFixedSize(295, 50)
        
        comment_exclude_layout = QVBoxLayout(comment_exclude_container)
        comment_exclude_layout.addWidget(comment_exclude_title_container)
        comment_exclude_layout.addWidget(self.comment_exclude_table)
        comment_exclude_layout.addWidget(self.comment_exclude_search_input)
        comment_exclude_layout.addWidget(self.comment_exclude_search_table)
        comment_exclude_title_container.setFixedSize(295, 50)

        # 절대 위치로 설정
        detect_main_container.setParent(detect_content)
        detect_main_container.resize(1800, 880)  # 크기 조정
        
        # 감지목록 콘텐츠를 탭 위젯에 추가
        self.tab_content_widgets.append(detect_content)
        
        # 감지목록 콘텐츠를 윈도우에 추가하고 위치 설정
        detect_content.setParent(self)
        detect_content.move(0, 100)  # 타이틀바와 상단 메뉴 아래부터
        detect_content.resize(1800, 860)  # 윈도우 크기에 맞춤 (960-100=860)
        detect_content.hide()  # 초기에는 숨김

    def get_button_style(self, is_selected):
        if is_selected:
            return """
                QPushButton {
                    background-color: #212121;
                    color: #0059FF;
                    border: 3px solid #8707ff;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #191c32;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 16px;
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
        
        # 버튼 스타일 업데이트
        for i, button in enumerate(self.tab_buttons):
            button.setStyleSheet(self.get_button_style(i == index))
        
        # 탭 콘텐츠 전환
        for i, content_widget in enumerate(self.tab_content_widgets):
            if content_widget is not None:  # None이 아닌 경우만 처리
                if i == index:
                    content_widget.show()
                else:
                    content_widget.hide()
        
        # 기존 레이아웃들 숨기기/보이기 (홈 탭일 때만 보이게)
        if index == 0:  # 홈 탭
            self.styled_box4.show()
            # 다른 박스들도 보이게
            for box_name in ['styled_box2', 'styled_box3', 'styled_box5', 'styled_box6']:
                if hasattr(self, box_name):
                    getattr(self, box_name).show()
        else:  # 감지목록 탭 - 기존 레이아웃 모두 숨기기
            self.styled_box4.hide()
            # 다른 박스들도 숨기기
            for box_name in ['styled_box2', 'styled_box3', 'styled_box5', 'styled_box6']:
                if hasattr(self, box_name):
                    getattr(self, box_name).hide()

    def toggle_all_preset_phrases(self):
        # 전체선택 체크박스의 상태를 확인
        sender = self.sender()
        is_checked = sender.isChecked()
        
        # 모든 상용구 체크박스들을 전체선택 상태와 동일하게 설정
        for checkbox in self.preset_phrase_checkboxes:
            checkbox.setChecked(is_checked)

    def add_word_to_list(self, list_type):
        # 단어 입력 다이얼로그 표시
        from PyQt5.QtWidgets import QInputDialog
        
        word, ok = QInputDialog.getText(self, '단어 추가', f'{list_type} 목록에 추가할 단어를 입력하세요:')
        if ok and word.strip():
            # 단어 목록에 추가
            if not hasattr(self, 'word_lists'):
                self.word_lists = {
                    'detect': [],
                    'exclude': [],
                    'report': [],
                    'report_exclude': [],
                    'comment': [],
                    'comment_exclude': []
                }
            
            self.word_lists[list_type].append(word.strip())
            self.update_word_list_display(list_type)
            print(f"'{word}' 단어를 {list_type} 목록에 추가했습니다.")

    def update_word_list_display(self, list_type):
        # 단어 목록 표시 업데이트
        from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
        
        # 각 섹션별 테이블 매핑
        table_mapping = {
            'detect': 'detect_table',
            'exclude': 'exclude_table',
            'report': 'report_table',
            'report_exclude': 'report_exclude_table',
            'comment': 'comment_table',
            'comment_exclude': 'comment_exclude_table'
        }
        
        table_name = table_mapping.get(list_type)
        if table_name and hasattr(self, table_name):
            table = getattr(self, table_name)
            table.setRowCount(len(self.word_lists[list_type]))
            for i, word in enumerate(self.word_lists[list_type]):
                # 단어 열
                word_item = QTableWidgetItem(word)
                table.setItem(i, 0, word_item)
                
                # 삭제 버튼 열
                delete_btn = QPushButton("X")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff4444;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 2px 6px;
                    }
                    QPushButton:hover {
                        background-color: #ff6666;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, w=word, lt=list_type: self.delete_word(lt, w))
                table.setCellWidget(i, 1, delete_btn)

    def search_words(self, list_type):
        # 단어 검색 기능
        from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
        
        # 각 섹션별 검색 입력과 검색 결과 테이블 매핑
        search_mapping = {
            'detect': ('detect_search_input', 'detect_search_table'),
            'exclude': ('exclude_search_input', 'exclude_search_table'),
            'report': ('report_search_input', 'report_search_table'),
            'report_exclude': ('report_exclude_search_input', 'report_exclude_search_table'),
            'comment': ('comment_search_input', 'comment_search_table'),
            'comment_exclude': ('comment_exclude_search_input', 'comment_exclude_search_table')
        }
        
        search_input_name, search_table_name = search_mapping.get(list_type, (None, None))
        if search_input_name and search_table_name and hasattr(self, search_input_name):
            search_input = getattr(self, search_input_name)
            search_table = getattr(self, search_table_name)
            
            search_text = search_input.text().lower()
            if not hasattr(self, 'word_lists'):
                return
                
            filtered_words = [word for word in self.word_lists[list_type] 
                            if search_text in word.lower()]
            
            search_table.setRowCount(len(filtered_words))
            for i, word in enumerate(filtered_words):
                # 단어 열
                word_item = QTableWidgetItem(word)
                search_table.setItem(i, 0, word_item)
                
                # 삭제 버튼 열
                delete_btn = QPushButton("X")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff4444;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 2px 6px;
                    }
                    QPushButton:hover {
                        background-color: #ff6666;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, w=word, lt=list_type: self.delete_word(lt, w))
                search_table.setCellWidget(i, 1, delete_btn)

    def delete_word(self, list_type, word):
        # 단어 삭제 기능
        if word in self.word_lists[list_type]:
            self.word_lists[list_type].remove(word)
            self.update_word_list_display(list_type)
            
            # 검색 결과도 업데이트
            search_mapping = {
                'detect': 'detect_search_input',
                'exclude': 'exclude_search_input',
                'report': 'report_search_input',
                'report_exclude': 'report_exclude_search_input',
                'comment': 'comment_search_input',
                'comment_exclude': 'comment_exclude_search_input'
            }
            
            search_input_name = search_mapping.get(list_type)
            if search_input_name and hasattr(self, search_input_name):
                self.search_words(list_type)
            print(f"'{word}' 단어를 {list_type} 목록에서 삭제했습니다.")

    def setup_tabs(self):
        # 첫 번째 버튼을 선택된 상태로 설정
        for i, button in enumerate(self.tab_buttons):
            button.setStyleSheet(self.get_button_style(i == 0))

    # 창 크기 변경 시 둥근 모서리 적용
    def resizeEvent(self, event):
        # 둥근 사각형 경로 생성
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), 10, 10)
        
        # 경로를 QRegion으로 변환
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        
        super().resizeEvent(event)

    # 창을 가운데 위치시키는 함수
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 알림/신고 목록 팝업 창
    def show_report_popup(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHeaderView, QWidget
        from PyQt5.QtCore import Qt
        
        # 팝업 창 생성
        popup = QDialog(self)
        popup.setWindowTitle("알림/신고 목록")
        popup.setModal(True)
        popup.resize(1200, 800)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(popup)
        
        # 제목
        title_label = QLabel("알림/신고 목록")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #8707ff;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 2x2 그리드 레이아웃
        grid_layout = QGridLayout()
        
        # 각 섹션을 위한 함수
        def create_section(title, bg_color="#f9f9f9"):
            section_widget = QWidget()
            section_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {bg_color};
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
            """)
            
            section_layout = QVBoxLayout(section_widget)
            section_layout.setContentsMargins(10, 10, 10, 10)
            
            # 제목
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                    padding: 5px;
                }
            """)
            section_layout.addWidget(title_label)
            
            # 내용 영역 (회색 박스)
            content_area = QWidget()
            content_area.setStyleSheet("""
                QWidget {
                    background-color: #e0e0e0;
                    border: 1px solid #fff;
                    border-radius: 3px;
                }
            """)
            content_area.setMinimumHeight(400)
            section_layout.addWidget(content_area)
            
            return section_widget
        
        # 4개 섹션 생성
        section1 = create_section("알림용 [감지목록] 댓글 남은 시간 : 0")
        section2 = create_section("신고용 [감지목록] 댓글 남은 시간 : 0")
        section3 = create_section("알림용 [감지목록] 제외 목록")
        section4 = create_section("신고용 [감지목록] 자동댓글 목록")
        
        # 그리드에 섹션들 추가
        grid_layout.addWidget(section1, 0, 0)  # 왼쪽 위
        grid_layout.addWidget(section2, 0, 1)  # 오른쪽 위
        grid_layout.addWidget(section3, 1, 0)  # 왼쪽 아래
        grid_layout.addWidget(section4, 1, 1)  # 오른쪽 아래
        
        # 그리드 레이아웃을 메인 레이아웃에 추가
        main_layout.addLayout(grid_layout)
        
        # 하단 버튼들
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("새로고침")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f8ff;
                border: 1px solid #8707ff;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
            }
        """)
        
        clear_btn = QPushButton("전체 삭제")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        
        close_btn = QPushButton("닫기")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """)
        close_btn.clicked.connect(popup.close)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        main_layout.addLayout(button_layout)
        
        # 팝업 창을 화면 중앙에 표시
        popup.exec_()

    # 커스텀 타이틀바 생성
    def create_custom_titlebar(self):
        from PyQt5.QtCore import QPoint
        
        # 타이틀바 위젯
        self.titlebar = QWidget()
        self.titlebar.setFixedHeight(40)
        self.titlebar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        
        # 타이틀바 레이아웃
        titlebar_layout = QHBoxLayout()
        titlebar_layout.setContentsMargins(15, 5, 5, 5)
        
        # 앱 아이콘과 제목
        self.app_icon = QLabel("🚀")
        self.app_icon.setStyleSheet("""
            QLabel {
                color: #fe53bb;
                font-size: 18px;
                background: transparent;
            }
        """)
        
        self.title_label = QLabel("Livescore_tool_v1.0")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                margin-left: 8px;
            }
        """)
        
        # 우측 버튼들
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(30, 30)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2f3b;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #323741;
            }
        """)
        self.minimize_btn.clicked.connect(self.showMinimized)
        
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(30, 30)
        self.maximize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2f3b;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #323741;
            }
        """)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        
        # 레이아웃에 추가
        titlebar_layout.addWidget(self.app_icon)
        titlebar_layout.addWidget(self.title_label)
        titlebar_layout.addStretch()
        titlebar_layout.addWidget(self.minimize_btn)
        titlebar_layout.addWidget(self.maximize_btn)
        titlebar_layout.addWidget(self.close_btn)
        
        self.titlebar.setLayout(titlebar_layout)
        
        # 타이틀바를 메인 윈도우에 추가
        self.titlebar.setParent(self)
        self.titlebar.move(0, 0)
        self.titlebar.resize(1800, 40)
        
        # 드래그 가능하도록 설정
        self.titlebar.mousePressEvent = self.titlebar_mouse_press
        self.titlebar.mouseMoveEvent = self.titlebar_mouse_move
        self.titlebar.mouseDoubleClickEvent = self.titlebar_double_click
        
        self.dragging = False
        self.drag_position = QPoint(0, 0)
    
    def titlebar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def titlebar_mouse_move(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
    
    def titlebar_double_click(self, event):
        self.toggle_maximize()
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setText("□")
        else:
            self.showMaximized()
            self.maximize_btn.setText("❐")

    # 프록시 파일 불러오기
    def load_proxy_file(self):
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        
        # 파일 선택 다이얼로그
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "프록시 파일 선택",
            "",
            "텍스트 파일 (*.txt);;모든 파일 (*.*)"
        )
        
        if file_path:
            try:
                # 파일 읽기
                with open(file_path, 'r', encoding='utf-8') as file:
                    proxy_lines = file.readlines()
                
                # 빈 줄 제거 및 유효한 프록시만 필터링
                valid_proxies = []
                for line in proxy_lines:
                    line = line.strip()
                    if line and ':' in line:  # IP:PORT 형태인지 확인
                        valid_proxies.append(line)
                
                # 프록시 개수 업데이트
                if hasattr(self, 'proxycount'):
                    self.proxycount.setText(f"{len(valid_proxies)}개 불러옴")
                
                # 성공 메시지
                QMessageBox.information(
                    self,
                    "파일 불러오기 완료",
                    f"프록시 파일을 성공적으로 불러왔습니다.\n\n파일: {file_path}\n불러온 프록시: {len(valid_proxies)}개"
                )
                
                # 프록시 데이터를 클래스 변수로 저장 (나중에 사용할 수 있도록)
                self.proxy_list = valid_proxies
                
            except Exception as e:
                # 오류 메시지
                QMessageBox.warning(
                    self,
                    "파일 읽기 오류",
                    f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}"
                )
        else:
            # 파일을 선택하지 않은 경우
            print("파일 선택이 취소되었습니다.")


# 메인 함수
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
