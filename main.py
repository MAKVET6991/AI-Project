import streamlit as st
import json
import requests

# إعدادات مظهر الموقع
st.set_page_config(page_title="مساعد المتجر الذكي", page_icon="🤖", layout="centered")

st.title("🤖 وكيل دعم العملاء الذكي")
st.write("أهلاً بك! أنا مساعدك الذكي، كيف يمكنني خدمتك اليوم؟")

# 💡 ضع مفتاح جوجل الجديد النظيف هنا مباشرة بين علامتي التنصيص
API_KEY = "AQ.Ab8RN6IIJ8M2519orDMl_-yHxpzBYvirNcg_XrRVR7StE1TuJg"

def load_order_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return "لا توجد بيانات طلبات حالية."

def get_ai_response(user_query):
    if not API_KEY or API_KEY == "AQ.Ab8RN6IIJ8M2519orDMl_-yHxpzBYvirNcg_XrRVR7StE1TuJg":
        return "خطأ: يرجى كتابة مفتاح API السري الخاص بك داخل ملف main.py أولاً!"
        
    orders_context = load_order_data()
    
    # الرابط المباشر والنظيف بدون أي تعقيدات
    base_url = "https://googleapis.com"
    full_url = f"{base_url}?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    prompt = f"أنت وكيل دعم عملاء محترف في متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر: {orders_context}\n\nسؤال العميل: {user_query}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(full_url, headers=headers, json=payload, timeout=15)
        
        if response.status_code != 200:
            return f"خطأ من خادم جوجل (كود {response.status_code}): يرجى التأكد من صحة المفتاح المكتوب داخل الكود."
            
        res_json = response.json()
        if "candidates" in res_json:
            return res_json["candidates"]["content"]["parts"]["text"]
        elif "error" in res_json:
            return f"خطأ من خادم جوجل: {res_json['error'].get('message', 'خطأ غير معروف')}"
        return "تنبيه: استجابة الخادم غير متوافقة."
    except Exception as e:
        return f"حدث خطأ أثناء الاتصال: {e}"

# صندوق الإدخال
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.success(ai_reply)