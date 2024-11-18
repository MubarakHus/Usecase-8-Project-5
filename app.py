import streamlit as st
import requests

# Set up the Streamlit app
st.title("Players Clusters")
   
# User inputs
publication_date = st.number_input("تاريخ النشر", min_value=1800, max_value=2024, value=2000)
num_pages = st.number_input("عدد الصفحات", min_value=20, max_value=1400, value=100)
price = st.number_input("السعر", min_value=2, max_value=550, value=50)  # Add other types as necessary
IsNew = st.checkbox(label="كتاب جديد", value=False) 
category = st.selectbox("التصنيف", ["الادارة والاعمال", "الادب والشعر", "التاريخ والجغرافيا", "التراجم والسير", "التقنية والكمبيوتر", "الخيال العلمي", "العلوم الاجتماعية والسياسية", "العلوم والرياضيات", "القانون", "القصة والرواية", "الكتب الطبية", "تطوير الذات", "دراسات اسلامية"])  # Add other makes as needed
cover = st.selectbox("الغلاف", ["غلاف ورقي", "غلاف مقوى", "غلاف مقوى فني", "كتاب الكتروني"])  # Add other makes as needed
Lang1 = st.checkbox(label="عربي", key="اللغة", value=True) 
Lang2 = st.checkbox(label="انجليزي", key="اللغة", value=False) 

# Prediction button
if st.button("Predict"):
    # API request URL
    url = "https://jarir-books.onrender.com"

        
    # Data for the POST request
    data = {
        "publication_date" : publication_date,
        "num_pages" : num_pages,
        "price" : price,
        "IsNew" : IsNew,
        "mng_cate": 0,
        "poet_cate": 0,
        "hist_cate": 0,
        "tr_cate": 0,
        "tec_cate":0,
        "fan_cate":0,
        "pol_cate":0,
        "math_cate":0,
        "law_cate":0,
        "story_cate":0,
        "midec_cate":0,
        "dev_cate":0,
        "islam_cate":0,
        "hard_cvr":0,
        "art_cvr":0,
        "ppr_cvr":0,
        "e_cvr":0,
        "ar":Lang1,
        "e":Lang2
    }
    if category == "الادارة والاعمال":
        data["mng_cate"] = 1
        
    elif category == "الادب والشعر":
        data["poet_cate"] = 1
        
    elif category =="التاريخ والجغرافيا":
        data["hist_cate"] = 1
        
    elif category ==  "التراجم والسير":
        data["tr_cate"] = 1
        
    elif category == "التقنية والكمبيوتر":
        data["tec_cate"] = 1
        
    elif category ==  "الخيال العلمي":
        data["fan_cate"] = 1
        
    elif category == "العلوم الاجتماعية والسياسية":
        data["pol_cate"] = 1
        
    elif category == "العلوم والرياضيات":
        data["math_cate"] = 1
        
    elif category == "القانون":
        data["law_cate"] = 1
        
    elif category == "القصة والرواية":
        data["story_cate"] = 1
        
    elif category == "الكتب الطبية":
        data["midec_cate"] = 1
    elif category == "تطوير الذات":
        data["dev_cate"] = 1
    elif category == "دراسات اسلامية":
        data["islam_cate"] = 1
        
    if cover == "غلاف ورقي":
        data["ppr_cvr"] = 1

    elif cover == "غلاف مقوى":
        data["hard_cvr"] = 1

    elif cover == "غلاف مقوى فني":
        data["art_cvr"] = 1

    elif cover == "كتاب الكتروني":
        data["e_cvr"] = 1

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Check for request errors
        prediction = response.json()  # Parse JSON response
        # {'Cheap_Price': 0, 'Good_Price': 1, 'High_Price': 2} 

        st.header("Recommended Books")
        
        # Display all recommended books with their images
        for i in range(len(prediction["titles"])):
            st.subheader(f"Book {i+1}: {prediction['titles'][i]}")
            st.image(prediction["img_urls"][i], caption=f"Book {i+1} Image", use_column_width=True)

    except requests.exceptions.RequestException as e:
        st.error("Error requesting prediction from API. Please try again.")
        st.write(e)