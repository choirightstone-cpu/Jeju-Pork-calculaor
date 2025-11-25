import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calculator
import platform

from matplotlib import font_manager, rc

# Korean Font Support
if platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
else:
    rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

import json
import os

# Set page config
st.set_page_config(page_title="가양제주맛돼지 송년회 예산 대시보드", layout="wide")

# --- Save/Load Logic ---
PRESET_FILE = 'presets.json'

def load_presets():
    if os.path.exists(PRESET_FILE):
        with open(PRESET_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_preset(name, data):
    presets = load_presets()
    presets[name] = data
    with open(PRESET_FILE, 'w', encoding='utf-8') as f:
        json.dump(presets, f, ensure_ascii=False, indent=4)

# Load presets at start
presets = load_presets()

# --- Custom CSS ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Reduce padding for a more compact look */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }
    h1 { font-size: 2.2rem !important; }
    h2 { font-size: 1.8rem !important; }
    h3 { font-size: 1.4rem !important; }
    
    /* Input field styling */
    .stNumberInput label {
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title and Calculator Button
col_title, col_calc_btn = st.columns([8, 2])
with col_title:
    st.title("🐷 가양제주맛돼지 송년회 예산 관리")
with col_calc_btn:
    if st.button("🧮 개별 계산기"):
        st.session_state.show_calculator = True
        st.rerun()

# --- Individual Calculator Overlay ---
if 'show_calculator' not in st.session_state:
    st.session_state.show_calculator = False

if st.session_state.show_calculator:
    st.markdown("---")
    c_head, c_close = st.columns([9, 1])
    with c_head:
        st.header("🧮 개별 계산기")
    with c_close:
        if st.button("❌ 닫기", key="close_calc"):
            st.session_state.show_calculator = False
            st.rerun()

    # Menu Data
    menu_data = {
        "세트메뉴": {
            "제주특별한판": 48000, "제주오겹세트": 45000, "제주갈매기세트": 45000
        },
        "고기류": {
            "오겹살": 15000, "삼겹살": 15000, "갈매기살": 16000, "항정살": 16000, "덜미살": 15000, "대구막창": 13000
        },
        "식사류": {
            "열무냉면": 5000, "비빔냉면": 5000, "열무국수": 5000, "비빔국수": 5000, "소면": 5000,
            "추억의도시락": 4000, "누룽지": 4000, "라면": 4000, "된장찌개": 1000, "공기밥": 1000
        },
        "주류": {
            "소주": 4000, "맥주": 4000, "청하": 5000, "한라산소주": 5000, "음료수": 2000
        }
    }

    total_calc_cost = 0
    
    # Create 4 columns for categories
    cols = st.columns(4)
    
    # Placeholder for total cost in the first column (to appear under Set Menu)
    with cols[0]:
        st.subheader("세트메뉴") # Re-render header manually or handle in loop?
        # Actually, let's just use the loop but capture the placeholder for col 0
        
    # We need to iterate carefully.
    # Let's just define the placeholder variable.
    total_placeholder = None

    # Iterate through categories and items
    for i, (category, items) in enumerate(menu_data.items()):
        with cols[i]:
            if i != 0: # We handle the header for col 0 differently if we want the placeholder below items
                st.subheader(category)
            else:
                st.subheader(category)
            
            for name, price in items.items():
                qty = st.number_input(f"{name} ({price:,}원)", min_value=0, step=1, key=f"calc_{name}")
                total_calc_cost += qty * price
            
            if i == 0:
                st.divider()
                total_placeholder = st.empty() # Create placeholder in col 0
    
    # Update the placeholder with the final total
    if total_placeholder:
        total_placeholder.metric("총 합계금액", f"{total_calc_cost:,} 원")
    
    st.stop() # Stop rendering the rest of the app

# --- Sidebar: Presets & Global Settings ---
st.sidebar.header("📂 설정 불러오기")
preset_names = ["선택 안함"] + list(presets.keys())
selected_preset = st.sidebar.selectbox("저장된 설정 선택", preset_names)

# Default values
defaults = {
    "total_people": 64, "people_per_table": 4, "budget_per_person": 35000,
    "special_platter_price": 48000, "special_platter_qty": 2,
    "extra_meat_price": 14000, "extra_meat_qty": 2,
    "soju_price": 4000, "soju_qty": 2,
    "beer_price": 4000, "beer_qty": 4,
    "drinks_price": 2000, "drinks_qty": 2,
    "meal_price": 20000, "meal_qty": 1
}

# Update defaults if preset selected
if selected_preset != "선택 안함":
    # Just show what would be loaded, or rely on the Load button to apply it
    pass

if st.sidebar.button("설정 불러오기"):
    if selected_preset != "선택 안함":
        data = presets[selected_preset]
        # Update session state for all keys
        for key, value in data.items():
            if key in st.session_state:
                st.session_state[key] = value
            # Also update the defaults dict just in case (though session state takes precedence)
            defaults[key] = value
        
        # Force a rerun to reflect changes
        st.rerun()
    else:
        st.sidebar.warning("불러올 설정을 선택해주세요.")

st.sidebar.divider()
st.sidebar.header("⚙️ 기본 설정")
# Note: We use st.session_state values if available to ensure persistence after Load
total_people = st.sidebar.number_input("총 참석 인원", min_value=1, value=defaults["total_people"], step=1, key="total_people")
people_per_table = st.sidebar.number_input("테이블 당 인원", min_value=1, value=defaults["people_per_table"], step=1, key="people_per_table")
budget_per_person = st.sidebar.number_input("1인당 최대 예산 (원)", min_value=10000, value=defaults["budget_per_person"], step=1000, key="budget_per_person")

# Calculate number of tables
num_tables = calculator.calculate_table_count(total_people, people_per_table)
st.sidebar.info(f"총 {num_tables}개의 테이블이 필요합니다.")

# --- Save Current Settings UI (Sidebar) ---
st.sidebar.divider()
st.sidebar.header("💾 설정 저장")
new_preset_name = st.sidebar.text_input("설정 이름 입력")
# The actual Save button logic is at the bottom of the script to capture all inputs.

st.sidebar.divider()

if 'show_menu' not in st.session_state:
    st.session_state.show_menu = False

if st.sidebar.button("지금 메뉴보기"):
    st.session_state.show_menu = True
    st.rerun()

if st.session_state.show_menu:
    col_spacer, col_close = st.columns([9, 1])
    with col_close:
        if st.button("❌ 닫기", key="close_menu_main"):
            st.session_state.show_menu = False
            st.rerun()
    
    st.image("menu.PNG", caption="메뉴판", use_container_width=True)
    st.stop()

# --- Main Area: Menu Configuration ---
st.subheader("📋 메뉴 및 가격 설정 (테이블 기준)")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### 🥩 고기류")
    special_platter_price = st.number_input("제주특별한판 가격", value=defaults["special_platter_price"], step=100, key="special_platter_price")
    special_platter_qty = st.number_input("제주특별한판 수량", value=defaults["special_platter_qty"], step=1, key="special_platter_qty")
    
    extra_meat_price = st.number_input("추가 고기류 가격 (평균)", value=defaults["extra_meat_price"], step=100, key="extra_meat_price")
    extra_meat_qty = st.number_input("추가 고기류 수량", value=defaults["extra_meat_qty"], step=1, key="extra_meat_qty")

with col2:
    st.markdown("##### 🍺 주류 및 음료")
    soju_price = st.number_input("소주 가격", value=defaults["soju_price"], step=100, key="soju_price")
    soju_qty = st.number_input("소주 수량", value=defaults["soju_qty"], step=1, key="soju_qty")
    
    beer_price = st.number_input("맥주 가격", value=defaults["beer_price"], step=100, key="beer_price")
    beer_qty = st.number_input("맥주 수량", value=defaults["beer_qty"], step=1, key="beer_qty")
    
    drinks_price = st.number_input("음료수 가격", value=defaults["drinks_price"], step=100, key="drinks_price")
    drinks_qty = st.number_input("음료수 수량", value=defaults["drinks_qty"], step=1, key="drinks_qty")

with col3:
    st.markdown("##### 🍚 식사류")
    meal_price = st.number_input("식사류 합계 (4인 기준)", value=defaults["meal_price"], step=100, key="meal_price")
    meal_qty = st.number_input("식사 세트 수량", value=defaults["meal_qty"], step=1, key="meal_qty")

# --- Save Logic Implementation (Post-Widget) ---
if st.sidebar.button("저장 (Save)"):
    if new_preset_name:
        current_data = {
            "total_people": st.session_state.total_people,
            "people_per_table": st.session_state.people_per_table,
            "budget_per_person": st.session_state.budget_per_person,
            "special_platter_price": st.session_state.special_platter_price,
            "special_platter_qty": st.session_state.special_platter_qty,
            "extra_meat_price": st.session_state.extra_meat_price,
            "extra_meat_qty": st.session_state.extra_meat_qty,
            "soju_price": st.session_state.soju_price,
            "soju_qty": st.session_state.soju_qty,
            "beer_price": st.session_state.beer_price,
            "beer_qty": st.session_state.beer_qty,
            "drinks_price": st.session_state.drinks_price,
            "drinks_qty": st.session_state.drinks_qty,
            "meal_price": st.session_state.meal_price,
            "meal_qty": st.session_state.meal_qty
        }
        save_preset(new_preset_name, current_data)
        st.sidebar.success(f"'{new_preset_name}' 저장 완료! (새로고침 필요)")
    else:
        st.sidebar.error("설정 이름을 입력해주세요.")

# Construct Menu Config Dictionary
menu_config = {
    "special_platter": {"name": "제주특별한판", "price": special_platter_price, "qty": special_platter_qty},
    "extra_meat": {"name": "추가 고기류", "price": extra_meat_price, "qty": extra_meat_qty},
    "soju": {"name": "소주", "price": soju_price, "qty": soju_qty},
    "beer": {"name": "맥주", "price": beer_price, "qty": beer_qty},
    "drinks": {"name": "음료수", "price": drinks_price, "qty": drinks_qty},
    "meal": {"name": "식사류", "price": meal_price, "qty": meal_qty},
}

# --- Calculation ---
result = calculator.calculate_total_cost(total_people, people_per_table, menu_config)

# --- Dashboard Display ---
st.divider()
st.header("📊 예산 분석 결과")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("총 예상 비용", f"{result['total_cost']:,} 원")
m2.metric("1인당 예상 비용", f"{int(result['per_person_cost']):,} 원")
delta = int(budget_per_person - result['per_person_cost'])
m3.metric("1인당 예산 잔액", f"{delta:,} 원", delta_color="normal")

# Visualization
st.subheader("비용 상세 내역")
breakdown_data = {v['name']: v['price'] * v['qty'] * result['num_tables'] for k, v in menu_config.items()}
df_breakdown = pd.DataFrame(list(breakdown_data.items()), columns=['항목', '총 비용'])

fig, ax = plt.subplots()
ax.pie(df_breakdown['총 비용'], labels=df_breakdown['항목'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# --- AI Recommendation ---
st.divider()
st.header("🤖 AI 예산 최적화 추천")
st.write("현재 설정된 예산을 초과하거나, 더 효율적인 주문 방식이 필요하신가요?")

if st.button("AI 최적화 실행"):
    optimized_config, reasoning = calculator.optimize_menu(budget_per_person, total_people, people_per_table, menu_config)
    
    opt_result = calculator.calculate_total_cost(total_people, people_per_table, optimized_config)
    
    st.success("최적화가 완료되었습니다!")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        st.subheader("🤖 AI 분석 및 제안")
        if reasoning:
            for note in reasoning:
                st.info(note)
        else:
            st.write("변경 사항이 없습니다.")
            
        st.markdown("---")
        st.write("### 변경된 메뉴 구성")
        for key, val in optimized_config.items():
            original_qty = menu_config[key]['qty']
            new_qty = val['qty']
            if original_qty != new_qty:
                st.write(f"- **{val['name']}**: {original_qty}개 → **{new_qty}개**")
            else:
                st.caption(f"- {val['name']}: {new_qty}개 (유지)")

    with col_opt2:
        st.subheader("최적화 후 예상 비용")
        st.metric("최적화 총 비용", f"{opt_result['total_cost']:,} 원")
        st.metric("최적화 1인당 비용", f"{int(opt_result['per_person_cost']):,} 원")
