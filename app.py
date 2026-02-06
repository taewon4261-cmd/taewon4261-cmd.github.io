import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ==========================================
# [설정 영역] 좌표를 상장 가운데로 맞췄습니다!
# ==========================================
# 1. 글자 위치 (X를 가운데 쯤으로 설정)
NAME_X, NAME_Y = 180, 350         # 이름
TITLE_X, TITLE_Y = 180, 450       # 자격증 명
DESC_X, DESC_Y = 180, 600         # 상세 내용

# 2. 하단 문구 및 도장 위치
FOOTER_X, FOOTER_Y = 180, 800     # 맨 밑 추가 문구
STAMP_X, STAMP_Y = 450, 700       # 도장 위치
STAMP_SIZE = (200, 200)           # 도장 크기

# 3. 글자 크기
FONT_SIZE_NAME = 50
FONT_SIZE_TITLE = 40
FONT_SIZE_DESC = 25
FONT_SIZE_FOOTER = 30             # 하단 문구 크기
TEXT_COLOR = (0, 0, 0)
# ==========================================

# 📜 [데이터베이스 업그레이드] 재미있는 종목 대거 추가!
CERT_DB = {
    "프로 눕방러 1급": {
        "desc": "위 사람은 숨쉬기 운동 외에는\n일절 움직이지 않으며, 등과 바닥의\n물아일체 경지에 올랐기에 임명함.",
        "footer": "전세계 눕방 협회장 김눕방"
    },
    "알콜 마스터 1급": {
        "desc": "위 사람은 간 해독 능력이\n타의 추종을 불허하며,\n술자리 끝까지 살아남기에 임명함.",
        "footer": "국제 알콜 감별사 협회"
    },
    "야근 요정 1급": {
        "desc": "위 사람은 남들 퇴근할 때\n모니터와 대화하며,\n회사의 전기를 수호하였기에 임명함.",
        "footer": "대한민국 야근 수호대"
    },
    "아가리어터 1급": {
        "desc": "위 사람은 '다이어트는 내일부터'라는\n명언을 매일 실천하며, 치킨 앞에서는\n이성을 잃는 능력이 탁월하기에 임명함.",
        "footer": "전국 작심삼일 연합회"
    },
    "월급 로그아웃 1급": {
        "desc": "위 사람은 월급이 통장에 들어오자마자\n카드값이 퍼가요~ 하며 0.1초 만에\n잔고가 사라지는 마술을 보였기에 임명함.",
        "footer": "사이버 머니 수집가"
    },
    "연애 이론 박사 1급": {
        "desc": "위 사람은 실전 경험은 전무하나\n남의 연애 상담에는 기가 막힌 솔루션을\n제시하는 모태솔로이기에 임명함.",
        "footer": "글로 배운 연애 학회"
    },
    "스마트폰 중독 1급": {
        "desc": "위 사람은 화장실 갈 때도 폰이 없으면\n불안 증세를 보이며, 배터리 20% 미만 시\n손을 떠는 금단현상을 보였기에 임명함.",
        "footer": "도파민의 노예들"
    },
    "분노 조절 장애 1급": {
        "desc": "위 사람은 평소엔 온화하나 게임만 하면\n키보드를 부수며, 운전대만 잡으면\nF1 레이서로 돌변하기에 임명함.",
        "footer": "급발진 연구소장"
    },
    "직접 입력": {
        "desc": "직접 입력해주세요.",
        "footer": "직접 입력해주세요."
    }
}

st.title("🎖️ 대국민 쓸데없는 자격증 발급소 (Final)")

# --- 사이드바 (사진 업로드 제거됨) ---
st.sidebar.header("정보 입력")

user_name = st.sidebar.text_input("이름", value="이름")
selected_cert = st.sidebar.selectbox("자격증 종류 선택", list(CERT_DB.keys()))

if selected_cert == "직접 입력":
    cert_title = st.sidebar.text_input("자격증 이름", value="코딩 천재 1급")
    cert_desc = st.sidebar.text_area("내용", value="그냥 천재임.")
    footer_text = st.sidebar.text_input("하단 문구 (예: 협회장 OOO)", value="코딩 협회장")
else:
    cert_title = selected_cert
    cert_desc = CERT_DB[selected_cert]["desc"]
    footer_text = CERT_DB[selected_cert]["footer"]
    st.sidebar.info(f"💡 내용:\n{cert_desc}\n\n💡 하단:\n{footer_text}")

# --- 메인 화면 ---
if st.button("자격증 발급하기 🖨️"):
    try:
        bg_image = Image.open("certificate_bg.png")
        draw = ImageDraw.Draw(bg_image)
        
        # 폰트 설정
        try:
            font_name = ImageFont.truetype("font.ttf", FONT_SIZE_NAME)
            font_title = ImageFont.truetype("font.ttf", FONT_SIZE_TITLE)
            font_desc = ImageFont.truetype("font.ttf", FONT_SIZE_DESC)
            font_footer = ImageFont.truetype("font.ttf", FONT_SIZE_FOOTER)
        except:
            st.error("🚨 'font.ttf'를 못 찾았어요! 기본 폰트로 나옵니다.")
            font_name = ImageFont.load_default()
            font_title = ImageFont.load_default()
            font_desc = ImageFont.load_default()
            font_footer = ImageFont.load_default()

        # 1. 글씨 쓰기 (중앙 정렬)
        draw.text((NAME_X, NAME_Y), f"성 명 : {user_name}", fill=TEXT_COLOR, font=font_name)
        draw.text((TITLE_X, TITLE_Y), f"자 격 : {cert_title}", fill=TEXT_COLOR, font=font_title)
        draw.text((DESC_X, DESC_Y), cert_desc, fill=TEXT_COLOR, font=font_desc, spacing=15)
        draw.text((FOOTER_X, FOOTER_Y), footer_text, fill=TEXT_COLOR, font=font_footer)

        # 2. 도장 찍기 (stamp.png가 있으면 찍음)
        try:
            stamp_image = Image.open("stamp.png").convert("RGBA") # 투명 배경 유지
            stamp_image = stamp_image.resize(STAMP_SIZE)
            # 도장을 찍을 때는 배경 이미지에 '마스크'를 씌워서 투명하게 합성
            bg_image.paste(stamp_image, (STAMP_X, STAMP_Y), stamp_image)
        except:
            st.warning("👉 'stamp.png' 파일이 없어서 도장은 안 찍혔어요!")

        # 결과 보여주기
        st.image(bg_image, caption="최종 완성!", use_column_width=True)
        
        buf = io.BytesIO()
        bg_image.save(buf, format="PNG")
        st.download_button("이미지 저장 📥", buf.getvalue(), f"{user_name}_{cert_title}.png", "image/png")
        
    except Exception as e:
        st.error(f"오류 발생: {e}")
        st.warning("'certificate_bg.png'와 'font.ttf' 파일을 확인해주세요!")