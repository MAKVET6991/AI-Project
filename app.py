import subprocess
import sys

# كود سحري يجبر السيرفر على تثبيت المكتبة الرسمية فوراً وبقوة عند التشغيل
try:
    from google import genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])
    from google import genai

import streamlit as st
import json

# إعدادات الصفحة المظهرية للموقع
st.set_page_config(page_title="مساعد المتجر الذكي", page_icon="🤖", layout="centered")

# تصميم عنوان الموقع بالأعلى
st.title("🤖 وكيل دعم العملاء الذكي")
st.write("أهلاً بك! أنا مساعدك الذكي، كيف يمكنني خدمتك اليوم؟")

# تهيئة عميل جوجل بمفتاحك الخاص
client = genai.Client(api_key="AQ.AbBRN6LWBFrM5ChcQE4JNDHLWI1ugAy_aJKNSJJKuemlobOw")

# دالة لقراءة بيانات الطلبات من ملف JSON
def load_order_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return "لا توجد بيانات طلبات حالية."

# دالة لإرسال واستقبال الرسائل من الذكاء الاصطناعي
def get_ai_response(user_query):
    orders_context = load_order_data()
    try:
        chat = client.chats.create(model='gemini-3.6-flash')
        prompt = f"أنت وكيل دعم عملاء محترف في متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر: {orders_context}\n\nسؤال العميل: {user_query}"
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e) or "Quota" in str(e):
            return "عذراً، لقد استهلكت الحصة المجانية المؤقتة للموقع حالياً، يرجى المحاولة بعد قليل أو الترقية للحساب التجاري."
        return f"حدث خطأ أثناء الاتصال: {e}"

# إنشاء صندوق إدخال النص للعميل
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.info(ai_reply)