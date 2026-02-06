import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ==========================================
# [설정 영역] 태권님이 맞춘 좌표 적용 완료!
# ==========================================
# 1. 상장 본문 글자 위치
NAME_X, NAME_Y = 180, 350         # 이름
TITLE_X, TITLE_Y = 180, 450       # 자격증 명
DESC_X, DESC_Y = 180, 600         # 상세 내용

# 2. [중요] 하단 문구 (왼쪽 검은 글씨) 위치
FOOTER_X, FOOTER_Y = 200, 800     # 검은 글씨 위치

# 3. [중요] 도장 위치 (오른쪽 빨간 도장 그림)
STAMP_X, STAMP_Y = 400, 650       # 도장 그림 위치
STAMP_SIZE = (250, 250)           # 도장 크기 (키움)

# 4. [신규 기능] 도장 '내부 글씨' 위치 미세 조정
STAMP_TEXT_X_OFFSET = 250         # 가로 위치 조절 (오른쪽으로 많이 이동)
STAMP_TEXT_Y_OFFSET = 65          # 세로 위치 조절 (아래로 이동)

# 5. 글자 크기
FONT_SIZE_NAME = 50
FONT_SIZE_TITLE = 40
FONT_SIZE_DESC = 25
FONT_SIZE_FOOTER = 30
FONT_SIZE_STAMP = 45              # 도장 글씨 크기 (키움)

# 6. 색상
TEXT_COLOR = (0, 0, 0)
STAMP_COLOR = (230, 0, 0, 220)    # 빨간색
# ==========================================

# 📜 [데이터베이스]
CERT_DB = {
    "프로 눕방러 1급": {
        "desc": "위 사람은 숨쉬기 운동 외에는\n일절 움직이지 않으며, 등과 바닥의\n물아일체 경지에 올랐기에 임명함.",
        "footer": "전세계 눕방 협회장 김눕방",
        "stamp_text": "눕방 장인"
    },
    "알콜 마스터 1급": {
        "desc": "위 사람은 간 해독 능력이\n타의 추종을 불허하며,\n술자리 끝까지 살아남기에 임명함.",
        "footer": "국제 알콜 감별사 협회",
        "stamp_text": "알콜 요정"
    },
    "야근 요정 1급": {
        "desc": "위 사람은 남들 퇴근할 때\n모니터와 대화하며,\n회사의 전기를 수호하였기에 임명함.",
        "footer": "대한민국 야근 수호대",
        "stamp_text": "야근 노예"
    },
    "아가리어터 1급": {
        "desc": "위 사람은 '다이어트는 내일부터'라는\n명언을 매일 실천하며, 치킨 앞에서는\n이성을 잃는 능력이 탁월하기에 임명함.",
        "footer": "전국 작심삼일 연합회",
        "stamp_text": "입만 살음"
    },
    "월급 로그아웃 1급": {
        "desc": "위 사람은 월급이 통장에 들어오자마자\n0.1초 만에 잔고가 사라지는 마술을 보였기에 임명함.",
        "footer": "사이버 머니 수집가",
        "stamp_text": "텅장 주인"
    },
    "스마트폰 중독 1급": {
        "desc": "위 사람은 폰이 없으면 불안 증세를 보이며,\n배터리 20% 미만 시 손을 떠는 금단현상을 보였기에 임명함.",
        "footer": "도파민의 노예들",
        "stamp_text": "도파민 중독"
    },
    "직접 입력": {
        "desc": "직접 입력해주세요.",
        "footer": "직접 입력해주세요.",
        "stamp_text": "내가 일짱"
    }
}

st.title("🎖️ 대국민 쓸데없는 자격증 발급소 (Final)")

# --- 사이드바 ---
st.sidebar.header("정보 입력")

user_name = st.sidebar.text_input("이름", value="이름")
selected_cert = st.sidebar.selectbox("자격증 종류 선택", list(CERT_DB.keys()))

if selected_cert == "직접 입력":
    cert_title = st.sidebar.text_input("자격증 이름", value="코딩 천재 1급")
    cert_desc = st.sidebar.text_area("내용", value="그냥 천재임.")
    footer_text = st.sidebar.text_input("하단 문구", value="코딩 협회장")
    stamp_text_input = st.sidebar.text_input("도장 문구 (띄어쓰기로 줄바꿈)", value="최고 존엄")
else:
    cert_title = selected_cert
    cert_desc = CERT_DB[selected_cert]["desc"]
    footer_text = CERT_DB[selected_cert]["footer"]
    stamp_text_input = CERT_DB[selected_cert]["stamp_text"]
    st.sidebar.info(f"💡 내용 미리보기:\n{cert_desc}")

# --- 배너 (100원 후원 유도) ---
st.sidebar.markdown("---")
st.sidebar.header("☕ 개발자에게 믹스커피 사주기")

# 1. 멘트 수정 (부담 없이 100원만!)
st.sidebar.markdown("""
재밌게 즐기셨나요?  
**'100원'**만 후원해주시면  
서버 유지비에 큰 힘이 됩니다! 🙇‍♂️  
(100원의 기적을 보여주세요!)
""")

# 2. 계좌번호 복사 버튼
st.sidebar.code("1000-4564-3898", language="text") # 본인 계좌
st.sidebar.caption("토스/카뱅에서 복사해서 보내주세요!")
# --- 메인 로직 ---
if st.button("자격증 발급하기 🖨️"):
    try:
        bg_image = Image.open("certificate_bg.png")
        draw = ImageDraw.Draw(bg_image)
        
        # 폰트 로드
        try:
            font_name = ImageFont.truetype("font.ttf", FONT_SIZE_NAME)
            font_title = ImageFont.truetype("font.ttf", FONT_SIZE_TITLE)
            font_desc = ImageFont.truetype("font.ttf", FONT_SIZE_DESC)
            font_footer = ImageFont.truetype("font.ttf", FONT_SIZE_FOOTER)
            font_stamp = ImageFont.truetype("font.ttf", FONT_SIZE_STAMP)
        except:
            st.error("🚨 'font.ttf' 필요! 기본 폰트로 나옵니다.")
            font_name = ImageFont.load_default()
            font_title = ImageFont.load_default()
            font_desc = ImageFont.load_default()
            font_footer = ImageFont.load_default()
            font_stamp = ImageFont.load_default()

        # 1. 상장 글씨 쓰기
        draw.text((NAME_X, NAME_Y), f"성 명 : {user_name}", fill=TEXT_COLOR, font=font_name)
        draw.text((TITLE_X, TITLE_Y), f"자 격 : {cert_title}", fill=TEXT_COLOR, font=font_title)
        draw.text((DESC_X, DESC_Y), cert_desc, fill=TEXT_COLOR, font=font_desc, spacing=15)
        
        # 하단 문구 (독립 위치)
        draw.text((FOOTER_X, FOOTER_Y), footer_text, fill=TEXT_COLOR, font=font_footer)

        # 2. 도장 만들기 (미세 조정 적용)
        try:
            stamp_image = Image.open("stamp_frame.png").convert("RGBA")
            stamp_draw = ImageDraw.Draw(stamp_image)
            
            # (1) 띄어쓰기를 줄바꿈으로 변경
            final_stamp_text = stamp_text_input.replace(" ", "\n")
            
            # (2) 글자 중앙 정렬 계산
            stamp_w, stamp_h = stamp_image.size
            left, top, right, bottom = stamp_draw.multiline_textbbox((0, 0), final_stamp_text, font=font_stamp, spacing=10, align='center')
            text_w = right - left
            text_h = bottom - top
            
            # (3) 기본 중앙 위치 + 사용자 미세 조정값(OFFSET) 더하기
            text_x = (stamp_w - text_w) / 2 + STAMP_TEXT_X_OFFSET
            text_y = (stamp_h - text_h) / 2 + STAMP_TEXT_Y_OFFSET

            # (4) 글씨 쓰기
            stamp_draw.multiline_text((text_x, text_y), final_stamp_text, fill=STAMP_COLOR, font=font_stamp, spacing=10, align='center')
            
            # 완성된 도장 합성
            stamp_image = stamp_image.resize(STAMP_SIZE)
            bg_image.paste(stamp_image, (STAMP_X, STAMP_Y), stamp_image)
            
        except Exception as e:
             st.warning(f"👉 'stamp_frame.png' 오류: {e}")

        # 결과 출력 및 다운로드
        st.image(bg_image, caption="최종 완성!", use_column_width=True)
        buf = io.BytesIO()
        bg_image.save(buf, format="PNG")
        st.download_button("이미지 저장 📥", buf.getvalue(), f"{user_name}_{cert_title}.png", "image/png")
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.warning("'certificate_bg.png'와 'font.ttf' 파일을 확인해주세요!")