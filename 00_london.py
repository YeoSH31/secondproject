import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# 🎈 제목 설정
st.set_page_config(page_title="런던 관광 가이드 🇬🇧", layout="wide")
st.title("런던 관광 가이드 🇬🇧")
st.markdown("런던의 매력적인 관광지들을 지도와 함께 자세히 알아봐요!")

---

# 📍 런던 주요 관광지 정보
# 각 관광지에 대한 상세한 설명과 이미지 정보도 추가할 수 있습니다.

london_landmarks = {
    "버킹엄 궁전": {
        "lat": 51.5014,
        "lon": -0.1419,
        "description": """
        **버킹엄 궁전**은 영국 군주의 공식 거처이자 행정 본부입니다. 
        런던을 방문하는 관광객들에게 가장 인기 있는 명소 중 하나로, 
        특히 근위병 교대식은 많은 사람들의 시선을 사로잡습니다. 
        여름철에는 궁전 내부 일부가 일반에 공개되기도 합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Buckingham_Palace_with_Victoria_Memorial.jpg/320px-Buckingham_Palace_with_Victoria_Memorial.jpg",
        "marker_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Buckingham_Palace_with_Victoria_Memorial.jpg/100px-Buckingham_Palace_with_Victoria_Memorial.jpg"
    },
    "런던 타워": {
        "lat": 51.5081,
        "lon": -0.0759,
        "description": """
        **런던 타워**는 영국의 역사적인 성으로, 천년이 넘는 역사를 자랑합니다. 
        궁전, 요새, 감옥, 처형장 등으로 사용되었으며, 
        현재는 왕관 보석을 보관하고 있는 박물관입니다. 
        타워의 상징적인 존재인 '비피터(Yeoman Warders)'가 안내하는 투어도 인상적입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Tower_of_London_from_Tower_Bridge.jpg/320px-Tower_of_London_from_Tower_Bridge.jpg",
        "marker_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Tower_of_London_from_Tower_Bridge.jpg/100px-Tower_of_London_from_Tower_Bridge.jpg"
    },
    "빅 벤 (국회의사당)": {
        "lat": 51.5007,
        "lon": -0.1246,
        "description": """
        **빅 벤**은 런던의 상징적인 랜드마크 중 하나로, 
        웨스트민스터 궁전(영국 국회의사당)의 시계탑에 있는 거대한 종의 별칭입니다. 
        고딕 양식의 웅장한 건축물은 테임즈 강변에서 아름다운 풍경을 자아냅니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Big_Ben_at_Dusk.jpg/320px-Big_Ben_at_Dusk.jpg",
        "marker_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Big_Ben_at_Dusk.jpg/100px-Big_Ben_at_Dusk.jpg"
    },
    "대영 박물관": {
        "lat": 51.5194,
        "lon": -0.1269,
        "description": """
        **대영 박물관**은 세계에서 가장 크고 중요한 박물관 중 하나입니다. 
        전 세계의 유물과 예술품을 소장하고 있으며, 
        특히 이집트 미라, 로제타 스톤, 파르테논 조각 등이 유명합니다. 
        인류 문명의 역사를 한눈에 볼 수 있는 곳입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/British_Museum_from_Russell_Square_garden.jpg/320px-British_Museum_from_Russell_Square_garden.jpg",
        "marker_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/British_Museum_from_Russell_Square_garden.jpg/100px-British_Museum_from_Russell_Square_garden.jpg"
    },
    "런던 아이": {
        "lat": 51.5033,
        "lon": -0.1195,
        "description": """
        **런던 아이**는 템스 강 남쪽에 위치한 거대한 관람차입니다. 
        높이 135미터로, 런던 시내의 360도 파노라마 뷰를 제공합니다. 
        특히 해 질 녘이나 밤에 탑승하면 런던의 아름다운 야경을 감상할 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/London_Eye_from_Westminster_Bridge.jpg/320px-London_Eye_from_Westminster_Bridge.jpg",
        "marker_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/London_Eye_from_Westminster_Bridge.jpg/100px-London_Eye_from_Westminster_Bridge.jpg"
    }
}

# 🗺️ 관광지 선택 드롭다운
selected_landmark_name = st.sidebar.selectbox(
    "어떤 관광지에 대해 알고 싶으신가요?",
    list(london_landmarks.keys())
)

selected_landmark = london_landmarks[selected_landmark_name]

st.subheader(f"✨ {selected_landmark_name} ✨")

# 📝 상세 설명 표시
st.write(selected_landmark["description"])

# 🖼️ 이미지 표시 (있는 경우)
if selected_landmark.get("image"):
    st.image(selected_landmark["image"], caption=selected_landmark_name, use_column_width=True)

---

# 🗺️ 지도에 관광지 위치 표시

# Folium 지도 생성
# 런던의 중심 좌표를 기준으로 지도를 만듭니다.
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12) 

# 선택된 관광지에 마커 추가 (이미지 및 작은 글씨 설명)
html = f"""
    <div style="text-align: center;">
        <img src="{selected_landmark['marker_image']}" alt="{selected_landmark_name}" width="80px" height="auto"><br>
        <p style="font-size: 12px; margin-top: 5px;"><b>{selected_landmark_name}</b></p>
    </div>
"""
iframe = folium.IFrame(html=html, width=120, height=120)
popup = folium.Popup(iframe, max_width=200)

folium.Marker(
    location=[selected_landmark["lat"], selected_landmark["lon"]],
    popup=popup,
    tooltip=selected_landmark_name,
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# 모든 관광지에 마커 추가 (옵션)
for name, data in london_landmarks.items():
    if name != selected_landmark_name: # 이미 선택된 관광지는 다른 색으로 표시
        # 다른 마커에도 이미지를 넣고 싶다면, 여기에 marker_image를 추가
        other_html = f"""
            <div style="text-align: center;">
                <img src="{data['marker_image']}" alt="{name}" width="60px" height="auto"><br>
                <p style="font-size: 10px; margin-top: 3px;">{name}</p>
            </div>
        """
        other_iframe = folium.IFrame(html=other_html, width=100, height=100)
        other_popup = folium.Popup(other_iframe, max_width=150)
        
        folium.Marker(
            location=[data["lat"], data["lon"]],
            popup=other_popup,
            tooltip=name,
            icon=folium.Icon(color='blue')
        ).add_to(m)

# 스트림릿에 Folium 지도 표시
st.markdown("### 🗺️ 지도에서 위치 확인하기")
folium_static(m, width=900, height=500)

st.markdown("""
---
Made with ❤️ by Your Name (or AI)
""")
