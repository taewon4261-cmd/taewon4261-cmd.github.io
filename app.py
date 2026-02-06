import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ==========================================
# [설정 영역]
# ==========================================
# 1. 위치 좌표
NAME_X, NAME_Y = 150, 280
TITLE_X, TITLE_Y = 150, 400
DESC_X, DESC_Y = 150, 525

# 2. [중요] 가로 한계선 (이 넓이를 넘어가면 제목은 작아지고, 내용은 줄바꿈됨)
MAX_WIDTH = 450 

# 3. 하단 문구 및 도장
FOOTER_X, FOOTER_Y = 120, 800
STAMP_X, STAMP_Y = 400, 650
STAMP_SIZE = (250, 250)
STAMP_TEXT_X_OFFSET = 250   # 도장 텍스트 위치 미세조정 필요시 변경
STAMP_TEXT_Y_OFFSET = 65

# 4. 기본 글자 크기
FONT_SIZE_NAME = 55
FONT_SIZE_TITLE_DEFAULT = 50 # 제목 기본 크기 (여기서부터 줄어듦)
FONT_SIZE_DESC = 30
FONT_SIZE_FOOTER = 40
FONT_SIZE_STAMP = 45

# 5. 폰트 파일 경로 (같은 폴더에 있어야 함)
FONT_PATH = "font.ttf" 

# 6. 색상
TEXT_COLOR = (0, 0, 0)
STAMP_COLOR = (230, 0, 0, 220)
# ==========================================

# 📜 [데이터베이스]
CERT_DB = {
    "협곡의 지배자 1급": {
        "desc": "위 사람은 '오빠 갱 안와?'를 시전하며 남 탓하기의 달인이고, 키보드 샷건 치기의 장인이기에 임명함.",
        "footer": "전국 키보드 워리어 협회",
        "stamp_text": "남탓 장인"
    },
    "프로 먹방러 1급": {
        "desc": "위 사람은 치킨 뼈를 보았을 때 양념인지 후라이드인지 구분하며, '맛있으면 0칼로리'를 과학적으로 증명했기에 임명함.",
        "footer": "배달의 민족 VVIP",
        "stamp_text": "돼지 보스"
    },
    "3대 500 헬창 1급": {
        "desc": "위 사람은 근손실을 세상에서 제일 무서워하며, 닭가슴살 쉐이크를 주식으로 삼는 쇠질 중독자이기에 임명함.",
        "footer": "국제 프로틴 연구소",
        "stamp_text": "근육 돼지"
    },
    "집 밖은 위험해 1급": {
        "desc": "위 사람은 약속이 취소되면 희열을 느끼며, 전기장판 위에서 귤 까먹는 스킬이 타의 추종을 불허하기에 임명함.",
        "footer": "전국 집순이 집돌이 연합",
        "stamp_text": "이불 밖 위험"
    },
    "알콜 마스터 1급": {
        "desc": "위 사람은 간 해독 능력이 타의 추종을 불허하며, '막차 끊겼다'를 핑계로 아침 해를 보고야 마는 인재이기에 임명함.",
        "footer": "국제 알콜 감별사 협회",
        "stamp_text": "알콜 요정"
    },
    "월급 로그아웃 1급": {
        "desc": "위 사람은 월급이 통장에 들어오자마자 0.1초 만에 카드값으로 퍼가요 당하는 마술을 보였기에 임명함.",
        "footer": "사이버 머니 수집가",
        "stamp_text": "텅장 주인"
    },
    "카페인 중독 1급": {
        "desc": "위 사람은 혈관에 피 대신 아이스 아메리카노가 흐르며, 커피 없이는 인성질을 부리는 금단현상이 있기에 임명함.",
        "footer": "전국 얼죽아 협회",
        "stamp_text": "커피 수혈"
    },
    "민트초코 1급": {
        "desc": "위 사람은 치약 맛이라고 놀림받아도 굴하지 않으며, 밥 비벼 먹을 기세로 민초를 찬양하는 굳건한 미각을 가졌기에 임명함.",
        "footer": "민초단 우수 회원",
        "stamp_text": "민초가 세상을"
    },
    "프로 눕방러 1급": {
        "desc": "위 사람은 숨쉬기 운동 외에는 일절 움직이지 않으며, 등과 바닥의 물아일체 경지에 올랐기에 임명함.",
        "footer": "전세계 눕방 협회장 김눕방",
        "stamp_text": "눕방 장인"
    },
    "야근 요정 1급": {
        "desc": "위 사람은 남들 퇴근할 때 모니터와 대화하며, 회사의 전기를 수호하였기에 임명함.",
        "footer": "대한민국 야근 수호대",
        "stamp_text": "야근 노예"
    },
    "아가리어터 1급": {
        "desc": "위 사람은 '다이어트는 내일부터'라는 명언을 매일 실천하며, 운동 등록만 하고 기부천사가 되었기에 임명함.",
        "footer": "전국 작심삼일 연합회",
        "stamp_text": "입만 살음"
    },
    "스마트폰 중독 1급": {
        "desc": "위 사람은 화장실 갈 때 폰이 없으면 변비에 걸리며, 배터리 20% 미만 시 손을 떠는 금단현상을 보였기에 임명함.",
        "footer": "도파민의 노예들",
        "stamp_text": "도파민 중독"
    },
    "직접 입력": {
        "desc": "직접 입력해주세요.",
        "footer": "직접 입력해주세요.",
        "stamp_text": "내가 일짱"
    }
}

# --- 🛠️ [기능 1] 설명 부분 자동 줄바꿈 함수 ---
def wrap_text(text, font, max_width, draw):
    lines = []
    # 사용자가 입력한 강제 줄바꿈(\n)은 먼저 유지
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        current_line = []
        for char in paragraph:
            current_line.append(char)
            # 현재까지의 길이 측정
            test_line = "".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width > max_width:
                # 넘치면 마지막 글자 빼고 줄바꿈 처리
                current_line.pop()
                lines.append("".join(current_line))
                current_line = [char] # 뺀 글자는 다음 줄 첫 글자로
        
        # 남은 글자들 추가
        if current_line:
            lines.append("".join(current_line))
            
    return "\n".join(lines)

# --- 🛠️ [기능 2] 글자 크기 자동 축소 함수 (제목 & 이름 공용) ---
def get_fitted_title_font(text, max_width, draw, font_path, start_size, min_size=20):
    current_size = start_size
    
    # 폰트 파일이 없으면 기본 폰트 반환 (축소 불가)
    try:
        font = ImageFont.truetype(font_path, current_size)
    except:
        return ImageFont.load_default()

    while current_size > min_size:
        font = ImageFont.truetype(font_path, current_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            return font # 범위 안에 들어오면 이 폰트 반환
        
        current_size -= 2 # 2픽셀씩 줄임
        
    return ImageFont.truetype(font_path, min_size) # 최소 사이즈 반환


# ==========================================
# [메인 화면 구성]
# ==========================================
st.title("🎖️ 대국민 쓸데없는 자격증 발급소")

# --- 사이드바 ---
st.sidebar.header("정보 입력")

user_name = st.sidebar.text_input("이름", value="홍길동")
selected_cert = st.sidebar.selectbox("자격증 종류 선택", list(CERT_DB.keys()))

if selected_cert == "직접 입력":
    cert_title_input = st.sidebar.text_input("자격증 이름", value="코딩 천재 1급")
    cert_desc_input = st.sidebar.text_area("내용 (길면 자동 줄바꿈 됨)", value="이 사람은 코딩을 너무 잘해서...")
    footer_text = st.sidebar.text_input("하단 문구", value="코딩 협회장")
    stamp_text_input = st.sidebar.text_input("도장 문구", value="참 잘했어요")
else:
    cert_title_input = selected_cert
    cert_desc_input = CERT_DB[selected_cert]["desc"]
    footer_text = CERT_DB[selected_cert]["footer"]
    stamp_text_input = CERT_DB[selected_cert]["stamp_text"]
    st.sidebar.info(f"내용: {cert_desc_input}")

# --- 배너 ---
st.sidebar.markdown("---")
st.sidebar.header("☕ 개발자에게 믹스커피 사주기")
st.sidebar.markdown("""
재밌게 즐기셨나요?  
**딱 '100원'**만 후원해주시면  
서버 유지비에 큰 힘이 됩니다! 🙇‍♂️  
""")
st.sidebar.code("1000-4564-3898", language="text")
st.sidebar.caption("토스/카뱅에서 복사해서 보내주세요!")

# --- 메인 로직 ---
if st.button("자격증 발급하기 🖨️"):
    try:
        # 배경 이미지 로드
        bg_image = Image.open("certificate_bg.png") # 배경 파일명 확인!
        draw = ImageDraw.Draw(bg_image)
        
        # 폰트 로드 (기본 폰트 설정)
        try:
            # 이름 폰트와 제목 폰트는 아래에서 동적으로 다시 로드하므로 여기선 기본값만 설정
            font_desc = ImageFont.truetype(FONT_PATH, FONT_SIZE_DESC)
            font_footer = ImageFont.truetype(FONT_PATH, FONT_SIZE_FOOTER)
            font_stamp = ImageFont.truetype(FONT_PATH, FONT_SIZE_STAMP)
        except:
            st.error(f"🚨 '{FONT_PATH}' 폰트 파일이 없습니다! 기본 폰트로 실행됩니다.")
            font_desc = ImageFont.load_default()
            font_footer = ImageFont.load_default()
            font_stamp = ImageFont.load_default()

        # 1. [수정됨] 이름 쓰기 (글자 수에 맞춰 폰트 크기 자동 조절)
        full_name = f"성 명 : {user_name}"
        # 이름도 제목과 같은 함수를 사용하여 크기 조절 (기본 크기 FONT_SIZE_NAME=50 부터 시작)
        fitted_name_font = get_fitted_title_font(full_name, MAX_WIDTH, draw, FONT_PATH, FONT_SIZE_NAME)
        draw.text((NAME_X, NAME_Y), full_name, fill=TEXT_COLOR, font=fitted_name_font)
        
        # 2. [기존 유지] 제목 쓰기 (글자 수에 맞춰 폰트 크기 자동 조절)
        full_title = f"자 격 : {cert_title_input}"
        fitted_title_font = get_fitted_title_font(full_title, MAX_WIDTH, draw, FONT_PATH, FONT_SIZE_TITLE_DEFAULT)
        draw.text((TITLE_X, TITLE_Y), full_title, fill=TEXT_COLOR, font=fitted_title_font)
        
        # 3. [기존 유지] 본문 쓰기 (칸 넘어가면 자동 줄바꿈)
        wrapped_desc = wrap_text(cert_desc_input, font_desc, MAX_WIDTH, draw)
        draw.text((DESC_X, DESC_Y), wrapped_desc, fill=TEXT_COLOR, font=font_desc, spacing=15)
        
        # 4. 하단 문구
        draw.text((FOOTER_X, FOOTER_Y), footer_text, fill=TEXT_COLOR, font=font_footer)

        # 5. 도장 찍기
        try:
            stamp_image = Image.open("stamp_frame.png").convert("RGBA") # 도장 틀 이미지
            stamp_draw = ImageDraw.Draw(stamp_image)
            
            # 도장 텍스트 (줄바꿈 처리)
            final_stamp_text = stamp_text_input.replace(" ", "\n")
            
            # 도장 중앙 정렬
            stamp_w, stamp_h = stamp_image.size
            left, top, right, bottom = stamp_draw.multiline_textbbox((0, 0), final_stamp_text, font=font_stamp, spacing=10, align='center')
            text_w = right - left
            text_h = bottom - top
            
            text_x = (stamp_w - text_w) / 2 + STAMP_TEXT_X_OFFSET
            text_y = (stamp_h - text_h) / 2 + STAMP_TEXT_Y_OFFSET

            stamp_draw.multiline_text((text_x, text_y), final_stamp_text, fill=STAMP_COLOR, font=font_stamp, spacing=10, align='center')
            
            # 배경에 도장 합성
            stamp_image = stamp_image.resize(STAMP_SIZE)
            bg_image.paste(stamp_image, (STAMP_X, STAMP_Y), stamp_image)
            
        except Exception as e:
             st.warning(f"도장 이미지 오류: {e}")

        # 결과 출력 및 다운로드
        st.image(bg_image, caption="완성된 자격증", use_column_width=True)
        
        buf = io.BytesIO()
        bg_image.save(buf, format="PNG")
        st.download_button("이미지 저장 📥", buf.getvalue(), f"{user_name}_자격증.png", "image/png")
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.info("폴더에 'certificate_bg.png', 'stamp_frame.png', 'font.ttf' 파일이 있는지 확인해주세요.")