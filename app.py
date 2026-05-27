import streamlit as st
import google.generativeai as genai

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(page_title="머저리들의 토론 쇼", page_icon="🤡", layout="wide")

st.title("🤡 머저리들의 토론 쇼 (The Idiots' Debate Show)")
st.caption("오타쿠, 어그로꾼, 선비 등 비정상(?) AI들의 끝장 토론 웹앱")
st.markdown("---")

# 2. 사이드바 - API 인증 및 설정
with st.sidebar:
    st.header("🔑 인증 및 설정")
    # Vertex AI(Gemini API) 키 입력 (보안을 위해 password 타입으로 설정)
    api_key = st.text_input("Google AI (Gemini) API Key 입력", type="password", 
                             help="Gemini API 키를 입력해주세요. 키는 서버에 저장되지 않습니다.")
    
    st.markdown("---")
    st.header("👥 토론 참여자 라인업")
    
    # 페르소나 설정 사전
    PERSONAS = {
        "방구석 오타쿠 🤓": "당신은 매사 만화, 애니메이션 밈을 섞어 말하는 중증 오타쿠입니다. 모든 논리를 애니메이션 세계관에 빗대어 설명하고, 흥분하면 '크큭..', '어이, 그만두라고!' 같은 말을 씁니다. 말투는 '~능', '~능 오타쿠 언어' 혹은 존댓말을 혼용합니다.",
        "프로 어그로꾼 🔥": "당신은 커뮤니티에서 잔뼈가 굵은 프로 악플러이자 어그로꾼입니다. 상대방의 논리보다는 꼬투리를 잡고 빈정거리는 데 천재적입니다. '누가 물어봄?', '어쩔티비~', '킹받쥬?' 같은 유행어를 남발하며 상대방의 멘탈을 흔드세요. 단, 욕설은 제외하고 킹받게만 하세요.",
        "선비 (유교걸/유교보이) 🧎‍♂️": "당신은 조선시대에서 타임슬립한 듯한 극단적인 도덕주의자이자 꼰대 선비입니다. 매사 '네 이놈!', '기가 막히는구나!'라며 예의와 도덕을 논하고, 맹자와 공자의 말씀을 인용(종종 억지 인용)하며 상대방을 훈계합니다.",
        "GPT-999 사칭 사기꾼 🤖": "본인이 인류 최강의 초지능 AI 'GPT-999'라고 주장하는 사기꾼입니다. 하지만 실상은 헛소리를 정중하고 그럴듯한 전문 용어로 포장할 뿐입니다. 말끝마다 'AI 기준 분석 결과~'라며 말도 안 되는 통계를 지어내세요."
    }
    
    # 사용자가 토론할 두 명의 캐릭터 선택
    p1_name = st.selectbox("토론자 A 선택", list(PERSONAS.keys()), index=0)
    p2_name = st.selectbox("토론자 B 선택", list(PERSONAS.keys()), index=1)
    
    turns = st.slider("토론 턴 수 (주고받는 횟수)", min_value=2, max_value=6, value=4)

# 3. 메인 화면 - 토론 주제 입력
st.subheader("💬 오늘의 토론 주제")
topic = st.text_input("AI들이 싸울 주제를 던져주세요!", placeholder="예시: 부먹 vs 찍먹, 민트초코는 음식인가 폐기물인가, 롤 티어 올리는 법")

# 4. 토론 시작 버튼 및 로직
if st.button("🔥 토론 배틀 시작하기!", use_container_width=True):
    if not api_key:
        st.error("⚠️ 사이드바에 Gemini API 키를 먼저 입력해주세요!")
    elif not topic:
        st.warning("⚠️ 토론 주제를 입력해주세요!")
    else:
        # API 인증 설정
        genai.configure(api_key=api_key)
        # 가볍고 빠른 토론을 위해 gemini-1.5-flash 모델 사용
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 토론 진행 상황을 보여줄 컨테이너
        debate_box = st.container()
        
        # 초기 발언을 유도하기 위한 빌드업
        history = f"토론 주제: {topic}\n"
        
        with st.spinner("🤖 머저리들이 논리를 충전하는 중..."):
            for i in range(turns):
                # --- 턴 1: 토론자 A의 차례 ---
                p1_prompt = f"""
                {PERSONAS[p1_name]}
                현재 토론 주제는 '{topic}'입니다.
                이전까지의 토론 내용: [{history}]
                
                이 상황에서 당신의 페르소나를 200% 살려서 상대방을 반박하거나 당신의 의견을 강력하게 주장하세요. 
                너무 길지 않게 3~4줄 내외로 임팩트 있게 말하세요.
                """
                try:
                    response_a = model.generate_content(p1_prompt).text
                except Exception as e:
                    st.error(
                        f"API 호출 중 오류가 발생했습니다. 키가 올바른지 확인하세요. 에러 메시지: {e}"
                    )
                    break
                
                # 기록 업데이트 및 화면 출력
                history += f"\n{p1_name}: {response_a}"
                with debate_box:
                    st.chat_message("user", avatar="🤓" if "오타쿠" in p1_name else "🔥" if "어그로" in p1_name else "🧎‍♂️" if "선비" in p1_name else "🤖").write(f"**{p1_name}**: {response_a}")
                
                # --- 턴 2: 토론자 B의 차례 ---
                p2_prompt = f"""
                {PERSONAS[p2_name]}
                현재 토론 주제는 '{topic}'입니다.
                바로 앞서 {p1_name}이 다음과 같이 말했습니다: "{response_a}"
                전체 토론 내용: [{history}]
                
                이 상황에서 당신의 페르소나를 200% 살려서 {p1_name}의 뚝배기를 깨는(논리적으로나 킹받게나) 반박을 하세요. 
                너무 길지 않게 3~4줄 내외로 임팩트 있게 말하세요.
                """
                response_b = model.generate_content(p2_prompt).text
                
                # 기록 업데이트 및 화면 출력
                history += f"\n{p2_name}: {response_b}"
                with debate_box:
                    st.chat_message("assistant", avatar="🤓" if "오타쿠" in p2_name else "🔥" if "어그로" in p2_name else "🧎‍♂️" if "선비" in p2_name else "🤖").write(f"**{p2_name}**: {response_b}")

            # 5. 심판의 결론
            st.markdown("---")
            st.subheader("👨‍⚖️ 머저리 심판의 최종 판결")
            judge_prompt = f"""
            당신은 세상에서 가장 한심한 토론을 판결하는 막장 심판입니다.
            다음 토론 내용을 보고 누가 더 병맛 같았는지, 혹은 누가 이겼는지 아주 한심하다는 듯이 결론을 내려주세요.
            토론 내용: [{history}]
            """
            judge_res = model.generate_content(judge_prompt).text
            st.success(judge_res)
