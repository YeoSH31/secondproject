import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="도쿄 관광 가이드", layout="wide")

st.title("🇯🇵 도쿄 주요 관광지 가이드")
st.markdown("도쿄의 대표 관광지를 지도와 함께 소개합니다. 각 장소를 클릭하면 설명이 표시됩니다!")

# 도쿄 중심 좌표
tokyo_center = [35.682839, 139.759455]

# 관광지 데이터 (설명 + 이미지 URL 포함)
places = [
    {
        "name": "도쿄 타워",
        "location": [35.6585805, 139.7454329],
        "description": "도쿄의 상징적인 철탑으로, 야경이 특히 아름답습니다. 전망대에서 도쿄 시내를 한눈에 볼 수 있어요.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Tokyo_Tower_and_around_Skyscrapers.jpg/640px-Tokyo_Tower_and_around_Skyscrapers.jpg"
    },
    {
        "name": "아사쿠사 & 센소지",
        "location": [35.714765, 139.796655],
        "description": "도쿄에서 가장 오래된 절인 센소지와 전통 상점 거리 '나카미세도리'가 유명한 지역입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Sensoji_Temple%2C_Tokyo%2C_Japan.jpg/640px-Sensoji_Temple%2C_Tokyo%2C_Japan.jpg"
    },
    {
        "name": "시부야 스크램블 교차로",
        "location": [35.659494, 139.700553],
        "description": "세계에서 가장 붐비는 교차로 중 하나. 근처에 하치공 동상도 있어요!",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Shibuya_Scramble_Crossing_2018.jpg/640px-Shibuya_Scramble_Crossing_2018.jpg"
    },
    {
        "name": "메이지 신궁",
        "location": [35.6764, 139.6993],
        "description": "울창한 숲 속에 자리한 신사로, 고요한 분위기 속에서 산책하기 좋아요.",
        "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nrtIZd1DAKL90f9pZZ2PoskK5EnVL0A1JLHygu9-ihUFYykfzCTCNotE5eJaqHOPixb9aF1t7GaSok-EOO0oqLmnIBxl3Z7e9NafLOFvfleSyzamo9gWZ7enqIwuXNEhTDR1VA=w270-h312-n-k-no"
    },
    {
        "name": "신주쿠 교엔",
        "location": [35.685175, 139.710052],
        "description": "넓은 정원이 인상적인 도쿄 도심 속의 힐링 공간입니다. 봄에는 벚꽃이 아름답습니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Shinjuku_Gyoen_Pond.jpg/640px-Shinjuku_Gyoen_Pond.jpg"
    }
]

# 지도 생성
m = folium.Map(location=tokyo_center, zoom_start=12)

# 관광지 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"<b>{place['name']}</b><br>{place['description']}",
        tooltip=place["name"]
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=1000, height=600)

# 관광지 리스트 출력
st.header("📍 관광지 요약")

for place in places:
    st.markdown(f"### {place['name']}")
    st.image(place["image_url"], width=500)
    st.markdown(f"<p style='font-size: 14px;'>{place['description']}</p>", unsafe_allow_html=True)
    st.markdown("---")
