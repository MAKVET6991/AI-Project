import streamlit as st
import json
from google import genai

# إعدادات مظهر الموقع
st.set_page_config(page_title="مساعد المتجر الذكي", page_icon="🤖", layout="centered")

st.title("🤖 وكيل دعم العملاء الذكي")
st.write("أهلاً بك! أنا مساعدك الذكي، كيف يمكنني خدمتك اليوم؟")

def load_order_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return "لا توجد بيانات طلبات حالية."

def get_ai_response(user_query):
    orders_context = load_order_data()
    try:
        # الاتصال التلقائي بالمفتاح الافتراضي للسيرفر
        client = genai.Client()
        
        prompt = f"أنت وكيل دعم عملاء محترف في متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر: {orders_context}\n\nسؤال العميل: {user_query}"
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"تنبيه: تأكد من كتابة المفتاح الجديد باسم GEMINI_API_KEY داخل الإعدادات. تفاصيل: {e}"

# صندوق الإدخال
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.success(ai_reply)