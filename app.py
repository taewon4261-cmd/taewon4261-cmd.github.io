import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="대국민 쓸데없는 자격증 발급소",
    page_icon="🎖️",
    layout="centered"
)

# ==========================================
# [설정 영역]
# ==========================================

# 🅰️ 폰트 파일 설정
FONT_PATH_MAIN = "font.ttf" 
FONT_PATH_TITLE = "gungseo.ttc" 

# 🅱️ 좌표 및 크기 설정
HEADER_X, HEADER_Y = 380, 160
FONT_SIZE_HEADER = 80 

NAME_X, NAME_Y = 150, 280
TITLE_X, TITLE_Y = 150, 400
DESC_X, DESC_Y = 150, 525

MAX_WIDTH = 450
FOOTER_X, FOOTER_Y = 120, 800
STAMP_X, STAMP_Y = 400, 650
STAMP_SIZE = (250, 250)
STAMP_TEXT_X_OFFSET = 250
STAMP_TEXT_Y_OFFSET = 65

FONT_SIZE_NAME = 55
FONT_SIZE_TITLE_DEFAULT = 50
FONT_SIZE_DESC = 30
FONT_SIZE_FOOTER = 40
FONT_SIZE_STAMP = 45

TEXT_COLOR = (0, 0, 0)
STAMP_COLOR = (230, 0, 0, 220)

# 저장할 파일 이름
DONOR_FILE = "donors.csv"

# ==========================================
# [데이터베이스 및 상태 관리]
# ==========================================

CERT_DB = {
    "협곡의 지배자 1급": {"desc": "위 사람은 '오빠 갱 안와?'를 시전하며 남 탓하기의 달인이고, 키보드 샷건 치기의 장인이기에 임명함.", "footer": "전국 키보드 워리어 협회", "stamp_text": "남탓 장인"},
    "프로 먹방러 1급": {"desc": "위 사람은 치킨 뼈를 보았을 때 양념인지 후라이드인지 구분하며, '맛있으면 0칼로리'를 과학적으로 증명했기에 임명함.", "footer": "배달의 민족 VVIP", "stamp_text": "돼지 보스"},
    "3대 500 헬창 1급": {"desc": "위 사람은 근손실을 세상에서 제일 무서워하며, 닭가슴살 쉐이크를 주식으로 삼는 쇠질 중독자이기에 임명함.", "footer": "국제 프로틴 연구소", "stamp_text": "근육 돼지"},
    "집 밖은 위험해 1급": {"desc": "위 사람은 약속이 취소되면 희열을 느끼며, 전기장판 위에서 귤 까먹는 스킬이 타의 추종을 불허하기에 임명함.", "footer": "전국 집순이 집돌이 연합", "stamp_text": "이불 밖 위험"},
    "알콜 마스터 1급": {"desc": "위 사람은 간 해독 능력이 타의 추종을 불허하며, '막차 끊겼다'를 핑계로 아침 해를 보고야 마는 인재이기에 임명함.", "footer": "국제 알콜 감별사 협회", "stamp_text": "알콜 요정"},
    "월급 로그아웃 1급": {"desc": "위 사람은 월급이 통장에 들어오자마자 0.1초 만에 카드값으로 퍼가요 당하는 마술을 보였기에 임명함.", "footer": "사이버 머니 수집가", "stamp_text": "텅장 주인"},
    "카페인 중독 1급": {"desc": "위 사람은 혈관에 피 대신 아이스 아메리카노가 흐르며, 커피 없이는 인성질을 부리는 금단현상이 있기에 임명함.", "footer": "전국 얼죽아 협회", "stamp_text": "커피 수혈"},
    "민트초코 1급": {"desc": "위 사람은 치약 맛이라고 놀림받아도 굴하지 않으며, 밥 비벼 먹을 기세로 민초를 찬양하는 굳건한 미각을 가졌기에 임명함.", "footer": "민초단 우수 회원", "stamp_text": "민초가 세상을"},
    "프로 눕방러 1급": {"desc": "위 사람은 숨쉬기 운동 외에는 일절 움직이지 않으며, 등과 바닥의 물아일체 경지에 올랐기에 임명함.", "footer": "전세계 눕방 협회장 김눕방", "stamp_text": "눕방 장인"},
    "야근 요정 1급": {"desc": "위 사람은 남들 퇴근할 때 모니터와 대화하며, 회사의 전기를 수호하였기에 임명함.", "footer": "대한민국 야근 수호대", "stamp_text": "야근 노예"},
    "아가리어터 1급": {"desc": "위 사람은 '다이어트는 내일부터'라는 명언을 매일 실천하며, 운동 등록만 하고 기부천사가 되었기에 임명함.", "footer": "전국 작심삼일 연합회", "stamp_text": "입만 살음"},
    "스마트폰 중독 1급": {"desc": "위 사람은 화장실 갈 때 폰이 없으면 변비에 걸리며, 배터리 20% 미만 시 손을 떠는 금단현상을 보였기에 임명함.", "footer": "도파민의 노예들", "stamp_text": "도파민 중독"},
    "직접 입력": {"desc": "직접 입력해주세요.", "footer": "직접 입력해주세요.", "stamp_text": "내가 일짱"}
}

# --- 💾 [핵심 기능] CSV 파일 로드 및 저장 ---
def load_donors():
    """CSV 파일이 있으면 불러오고, 없으면 기본값 반환"""
    if os.path.exists(DONOR_FILE):
        try:
            df = pd.read_csv(DONOR_FILE)
            # 데이터 정제: '금액' 컬럼의 NaN을 0으로 채우고 정수로 변환
            if '금액' in df.columns:
                df['금액'] = df['금액'].fillna(0).astype(int)
            return df.to_dict('records')
        except:
            return []
    else:
        # 파일이 없을 때 기본 데이터 (처음 시작할 때)
        return [
            {"이름": "익명의 천사", "금액": 100},
            {"이름": "지나가던 행인", "금액": 10},
        ]

def save_donors(donor_list):
    """리스트를 CSV 파일로 저장"""
    df = pd.DataFrame(donor_list)
    df.to_csv(DONOR_FILE, index=False)

# 세션 상태 초기화 (앱 켜질 때 딱 한 번 실행)
if 'donors' not in st.session_state:
    st.session_state.donors = load_donors()

# 🛡️ [수정됨] 총 모금액 계산 (에러 방지 기능 추가)
def get_total_donation():
    if not st.session_state.donors:
        return 0
    
    total = 0
    for item in st.session_state.donors:
        try:
            # 금액을 가져오는데, 없거나 이상하면 0원으로 처리
            amount = item.get('금액', 0)
            if pd.isna(amount) or amount == '':
                amount = 0
            total += int(float(amount)) # float로 먼저 바꾸고 int로 (소수점 에러 방지)
        except:
            continue # 에러나면 그냥 넘어감 (멈추지 않음)
            
    return total


# --- 🛠️ 헬퍼 함수들 ---
def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        current_line = []
        for char in paragraph:
            current_line.append(char)
            test_line = "".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width > max_width:
                current_line.pop()
                lines.append("".join(current_line))
                current_line = [char]
        if current_line:
            lines.append("".join(current_line))
    return "\n".join(lines)

def get_fitted_title_font(text, max_width, draw, font_path, start_size, min_size=20):
    current_size = start_size
    try:
        font = ImageFont.truetype(font_path, current_size)
    except:
        return ImageFont.load_default()
    while current_size > min_size:
        font = ImageFont.truetype(font_path, current_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            return font
        current_size -= 2
    return ImageFont.truetype(font_path, min_size)

# ==========================================
# [메인 화면 UI 구성]
# ==========================================

with st.sidebar:
    st.header("📂 메뉴 선택")
    menu = st.radio(
        "이동할 서비스를 선택하세요:",
        ["🏆 자격증 발급소", "🔮 심리테스트 (준비중)", "🤖 AI 캐릭터 (준비중)"]
    )
    
    st.markdown("---")

    # 🟢 자격증 입력 폼
    if menu == "🏆 자격증 발급소":
        st.subheader("📝 자격증 정보 입력")
        
        user_name = st.text_input("이름", value="홍길동")
        
        cert_list = list(CERT_DB.keys())
        if "직접 입력" in cert_list:
            cert_list.remove("직접 입력")
            cert_list.insert(0, "직접 입력")
            
        selected_cert = st.selectbox("자격증 종류", cert_list)