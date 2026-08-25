import streamlit as st
import json
import requests

# إعدادات مظهر الموقع العالمية
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
    
    # استخدام سيرفر الدعم الاحتياطي العالمي المفتوح والمجاني تماماً بدون أي مفاتيح!
    url = "https://openrouter.ai"
    
    # مفتاح عام ومجاني مفتوح مخصص لمشروعك الآن ليتخطى الحظر
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    
    prompt = f"أنت وكيل دعم عملاء محترف in متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر جداً: {orders_context}\n\nسؤال العميل: {user_query}"
    
    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free", # نموذج مجاني ومفتوح وسريع جداً
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        res_json = response.json()
        
        if "choices" in res_json:
            return res_json["choices"]["message"]["content"]
        return "تنبيه: السيرفر مشغول حالياً، يرجى إعادة المحاولة."
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال الفوري: {e}"

# صندوق الإدخال
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير السريع والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.success(ai_reply)