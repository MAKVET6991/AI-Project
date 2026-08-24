import streamlit as st
import json
import requests

# إعدادات الصفحة المظهرية للموقع
st.set_page_config(page_title="مساعد المتجر الذكي", page_icon="🤖", layout="centered")

# تصميم عنوان الموقع بالأعلى
st.title("🤖 وكيل دعم العملاء الذكي")
st.write("أهلاً بك! أنا مساعدك الذكي، كيف يمكنني خدمتك اليوم؟")

# جلب المفتاح السري بأمان من إعدادات الموقع
API_KEY = st.secrets["GEMINI_API_KEY"]

# دالة لقراءة بيانات الطلبات من ملف JSON
def load_order_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return "لا توجد بيانات طلبات حالية."

# دالة للاتصال المباشر بالسيرفر
def get_ai_response(user_query):
    orders_context = load_order_data()
    
    # الرابط الصحيح والكامل الموجه لسيرفر جوجل مباشرة
    url = f"https://googleapis.com{API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"أنت وكيل دعم عملاء محترف في متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر: {orders_context}\n\nسؤال العميل: {user_query}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        if "candidates" in res_json:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in res_json:
            return f"خطأ من الخادم: {res_json['error'].get('message', '')}"
        return "حدث خطأ غير متوقع في استجابة الخادم."
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال: {e}"

# إنشاء صندوق إدخال النص للعميل
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.info(ai_reply)