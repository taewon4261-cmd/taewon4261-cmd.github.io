import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import pandas as pd
import os

# ==========================================
# [페이지 기본 설정]
# 🚀 초기 상태: 사이드바 닫힘 (collapsed)
# ==========================================
st.set_page_config(
    page_title="대국민 쓸데없는 자격증 발급소",
    page_icon="🎖️",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# ==========================================
# [설정 영역]
# ==========================================
FONT_PATH_MAIN = "gungseo.ttc" 
FONT_PATH_TITLE = "gungseo.ttc" 

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

DONOR_FILE = "donors.csv"

# ==========================================
# [데이터베이스]
# ==========================================
CERT_DB = {
    "직접 입력": {"desc": "직접 입력해주세요.", "footer": "직접 입력해주세요.", "stamp_text": "내가 일짱"},
    "집밥 미슐랭 1급": {"desc": "위 사람은 눈대중과 손맛만으로 5성급 호텔 요리를 선사하며, '맛없으면 먹지 마'라고 해도 밥 두 공기를 비우게 만들기에 임명함.", "footer": "전국 확찐자 연합회", "stamp_text": "신의 손맛"},
    "우리집 구글 1급": {"desc": "위 사람은 '엄마 내 양말 어딨어?'라고 물으면 3초 만에 찾아내며, 집안의 모든 물건 위치를 GPS처럼 꿰뚫고 있기에 임명함.", "footer": "국제 분실물 센터", "stamp_text": "다 찾아냄"},
    "우주 최강 엄마 1급": {"desc": "위 사람은 존재 자체만으로 우리 집의 빛과 소금이며, 자식의 투정도 태평양 같은 마음으로 받아주는 든든한 버팀목이기에 임명함.", "footer": "아들래미 팬클럽", "stamp_text": "효도 할게"},
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
}

# ==========================================
# [함수 정의]
# ==========================================

# 1. 파일 불러오기 (안전장치 추가)
def load_donors():
    if os.path.exists(DONOR_FILE):
        try:
            df = pd.read_csv(DONOR_FILE)
            # 금액 컬럼이 없으면 생성, 이상한 값은 0으로 처리
            if '금액' not in df.columns:
                df['금액'] = 0
            df['금액'] = pd.to_numeric(df['금액'], errors='coerce').fillna(0).astype(int)
            return df.to_dict('records')
        except:
            return []
    else:
        return [
            {"이름": "익명의 천사", "금액": 100},
            {"이름": "지나가던 행인", "금액": 10},
        ]

def save_donors(donor_list):
    df = pd.DataFrame(donor_list)
    df.to_csv(DONOR_FILE, index=False)

# 2. 🔥 [에러 수정됨] 총 모금액 계산 함수
# 숫자가 아닌 게 들어와도 에러 안 나게 'try-except'로 감쌌습니다.
def get_total_donation():
    if not st.session_state.donors:
        return 0
    total = 0
    for item in st.session_state.donors:
        try:
            amount = item.get('금액', 0)
            if pd.isna(amount) or amount == '':
                amount = 0
            total += int(float(str(amount))) # 문자열이어도 숫자로 변환 시도
        except:
            continue # 변환 실패하면 무시하고 다음으로
    return total

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
# [상태 관리 초기화]
# ==========================================
if 'donors' not in st.session_state:
    st.session_state.donors = load_donors()

if 'page_state' not in st.session_state:
    st.session_state.page_state = 'HOME'


# ==========================================
# [화면 구성 로직]
# ==========================================

# 1. 🏠 시작 화면 (HOME) - 사이드바 닫힘
if st.session_state.page_state == 'HOME':
    st.title("🎖️ 대국민 쓸데없는 자격증 발급소")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdtY2J6eHoxMXZ6bHoxMXZ6bHoxMXZ6bHoxMXZ6bHoxMXZ6bHoxMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bu3XilJ5BOiSGic/giphy.gif", width=300)
    st.markdown("### 당신의 잉여력을 증명하세요!")
    
    st.markdown("---")
    
    # 이 버튼을 누르면 입력 화면으로 이동
    if st.button("🚀 자격증 생성하러 가기", type="primary", use_container_width=True):
        st.session_state.page_state = 'INPUT'
        st.rerun()


# 2. 📝 입력 화면 (INPUT) - 사이드바 열림
elif st.session_state.page_state == 'INPUT':
    
    # 메인 화면 안내
    st.title("📝 정보 입력 단계")
    st.info("👈 **왼쪽 사이드바**가 열렸습니다! 정보를 입력해주세요.")
    
    # 사이드바 내용 구성
    with st.sidebar:
        st.header("📝 정보 입력")
        
        user_name = st.text_input("이름", value="홍길동")
        
        cert_list = list(CERT_DB.keys())
        if "직접 입력" in cert_list:
            cert_list.remove("직접 입력")
        cert_list.insert(0, "직접 입력")
            
        selected_cert = st.selectbox("자격증 종류", cert_list)

        if selected_cert == "직접 입력":
            cert_title_input = st.text_input("자격증 이름", value="코딩 천재 1급")
            cert_desc_input = st.text_area("내용", value="내용을 입력하세요.")
            footer_text = st.text_input("발급 기관", value="코딩 협회")
            stamp_text_input = st.text_input("도장 문구 (띄어쓰기로 줄바꿈)", value="참 잘했어요")
        else:
            cert_title_input = selected_cert
            cert_desc_input = CERT_DB[selected_cert]["desc"]
            footer_text = CERT_DB[selected_cert]["footer"]
            stamp_text_input = CERT_DB[selected_cert]["stamp_text"]

        st.markdown("---")
        
        # 🔥 [핵심] 사이드바 안의 "제작하기" 버튼
        if st.button("✨ 제작하기 (완료)", type="primary", use_container_width=True):
            # 입력값을 저장하고 결과 화면으로 이동
            st.session_state.input_data = {
                "name": user_name,
                "title": cert_title_input,
                "desc": cert_desc_input,
                "footer": footer_text,
                "stamp": stamp_text_input
            }
            st.session_state.page_state = 'RESULT'
            st.rerun()
            
        # 취소 버튼
        if st.button("🏠 처음으로"):
            st.session_state.page_state = 'HOME'
            st.rerun()


# 3. 🎉 결과 화면 (RESULT) - 사이드바 닫고 결과 보여줌
elif st.session_state.page_state == 'RESULT':
    st.title("🎉 자격증 발급 완료!")
    st.balloons() # 축하 효과

    # 저장된 데이터 사용
    data = st.session_state.input_data

    # 이미지 생성
    try:
        bg_image = Image.open("certificate_bg.png")
        draw = ImageDraw.Draw(bg_image)
        
        try:
            try:
                font_header = ImageFont.truetype(FONT_PATH_TITLE, FONT_SIZE_HEADER)
            except:
                font_header = ImageFont.truetype(FONT_PATH_TITLE, FONT_SIZE_HEADER, index=0)

            font_desc = ImageFont.truetype(FONT_PATH_MAIN, FONT_SIZE_DESC)
            font_footer = ImageFont.truetype(FONT_PATH_MAIN, FONT_SIZE_FOOTER)
            font_stamp = ImageFont.truetype(FONT_PATH_MAIN, FONT_SIZE_STAMP)
        except:
            st.error("🚨 폰트 로드 실패!")
            font_header = ImageFont.load_default()
            font_desc = ImageFont.load_default()
            font_footer = ImageFont.load_default()
            font_stamp = ImageFont.load_default()

        draw.text((HEADER_X, HEADER_Y), "자 격 증", fill=TEXT_COLOR, font=font_header, anchor="mm")

        full_name = f"성 명 : {data['name']}"
        fitted_name_font = get_fitted_title_font(full_name, MAX_WIDTH, draw, FONT_PATH_MAIN, FONT_SIZE_NAME)
        draw.text((NAME_X, NAME_Y), full_name, fill=TEXT_COLOR, font=fitted_name_font)
        
        full_title = f"자 격 : {data['title']}"
        fitted_title_font = get_fitted_title_font(full_title, MAX_WIDTH, draw, FONT_PATH_MAIN, FONT_SIZE_TITLE_DEFAULT)
        draw.text((TITLE_X, TITLE_Y), full_title, fill=TEXT_COLOR, font=fitted_title_font)
        
        wrapped_desc = wrap_text(data['desc'], font_desc, MAX_WIDTH, draw)
        draw.text((DESC_X, DESC_Y), wrapped_desc, fill=TEXT_COLOR, font=font_desc, spacing=15)
        
        draw.text((FOOTER_X, FOOTER_Y), data['footer'], fill=TEXT_COLOR, font=font_footer)

        try:
            stamp_image = Image.open("stamp_frame.png").convert("RGBA")
            stamp_draw = ImageDraw.Draw(stamp_image)
            final_stamp_text = data['stamp'].replace(" ", "\n")
            
            left, top, right, bottom = stamp_draw.multiline_textbbox((0, 0), final_stamp_text, font=font_stamp, spacing=10, align='center')
            text_w, text_h = right - left, bottom - top
            
            stamp_w, stamp_h = stamp_image.size
            text_x = (stamp_w - text_w) / 2 + STAMP_TEXT_X_OFFSET
            text_y = (stamp_h - text_h) / 2 + STAMP_TEXT_Y_OFFSET
            
            stamp_draw.multiline_text((text_x, text_y), final_stamp_text, fill=STAMP_COLOR, font=font_stamp, spacing=10, align='center')
            stamp_image = stamp_image.resize(STAMP_SIZE)
            bg_image.paste(stamp_image, (STAMP_X, STAMP_Y), stamp_image)
        except Exception as e:
            st.warning(f"도장 오류: {e}")

        # 결과 이미지 표시
        st.image(bg_image, caption=f"{data['name']}님의 자격증", use_container_width=True)
        
        # 버튼 배치 (이미지 저장 / 새로 만들기)
        col1, col2 = st.columns(2)
        with col1:
            buf = io.BytesIO()
            bg_image.save(buf, format="PNG")
            st.download_button(
                label="📥 이미지 다운로드",
                data=buf.getvalue(),
                file_name=f"{data['name']}_자격증.png",
                mime="image/png",
                type="primary",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 새로운 자격증 만들기", use_container_width=True):
                st.session_state.page_state = 'INPUT'
                st.rerun()
                
    except Exception as e:
        st.error(f"오류 발생: {e}")


# ==========================================
# [공통 사이드바 요소]
# 입력 화면(INPUT)일 때만 밑에 후원/문의 탭을 보여줍니다.
# ==========================================
if st.session_state.page_state == 'INPUT':
    with st.sidebar:
        st.markdown("---")
        total_money = get_total_donation()
        
        st.header(" 티끌모아 노트북 💻 ")
        st.markdown(f"""
         코딩하다가 자꾸 렉이 걸려요... 😭  

    여러분의 **소중한 100원**을 모아  

    **개발용 노트북**을 장만하겠습니다!🙇‍♂️
        **(모금액: {total_money:,}원 / 1,500,000원)**
        """)
        st.code("1000-4564-3898", language="text")
        st.caption("토스/카뱅 복사해서 '엔터키' 하나 사주기 ⌨️")
        
        # 후원자 목록
        with st.expander("📜 명예의 전당"):
            is_admin = st.checkbox("관리자 모드")
            if st.session_state.donors:
                df = pd.DataFrame(st.session_state.donors)
            else:
                df = pd.DataFrame(columns=["이름", "금액"])

            if is_admin:
                password = st.text_input("관리자 비밀번호", type="password")
                if password == "1234":
                    edited_df = st.data_editor(
                        df, 
                        num_rows="dynamic",
                        use_container_width=True,
                        column_config={"금액": st.column_config.NumberColumn(format="%d원")},
                        key="editor"
                    )
                    if st.button("저장하기 💾"):
                        # 여기서도 안전장치 추가
                        if '금액' in edited_df.columns:
                            edited_df['금액'] = pd.to_numeric(edited_df['금액'], errors='coerce').fillna(0).astype(int)
                            
                        new_data = edited_df.to_dict("records")
                        st.session_state.donors = new_data
                        save_donors(new_data)
                        st.success("저장 완료!")
                        st.rerun()
                    
                    csv_data = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📂 명단 다운로드", csv_data, "donors.csv", "text/csv")
                elif password:
                    st.error("비밀번호 오류")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.caption("📧 문의/제보: mmm4261@naver.com")