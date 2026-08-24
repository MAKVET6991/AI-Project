import streamlit as st
import json
import requests

# إعدادات الصفحة
st.set_page_config(page_title="مساعد المتجر الذكي", page_icon="🤖", layout="centered")

st.title("🤖 وكيل دعم العملاء الذكي")
st.write("أهلاً بك! أنا مساعدك الذكي، كيف يمكنني خدمتك اليوم؟")

# جلب المفتاح السري بأمان من إعدادات الموقع
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

def load_order_data():
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return "لا توجد بيانات طلبات حالية أو الملف غير صالح."

def get_ai_response(user_query):
    if not API_KEY:
        return "خطأ حاسم: لم يتم العثور على المفتاح السري GEMINI_API_KEY في إعدادات Secrets لموقع Streamlit!"
        
    orders_context = load_order_data()
    
    # رابط نظيف ومباشر ومقسم لضمان عدم حدوث أي خطأ مطبعي في الدمج
base_url = "https://googleapis.com"
    full_url = f"{base_url}?key={API_KEY}"    
    prompt = f"أنت وكيل دعم عملاء محترف في متجر إلكتروني. استخدم بيانات الطلبات التالية للإجابة على استفسار العميل بدقة باللغة العربية وبأسلوب مهذب ومختصر: {orders_context}\n\nسؤال العميل: {user_query}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(full_url, headers=headers, json=payload, timeout=15)
        
        # حماية ضد الانهيار: التحقق من كود نجاح الاتصال أولاً قبل فك التشفير
        if response.status_code != 200:
            return f"خطأ من خادم جوجل (كود {response.status_code}): يرجى التأكد من صحة المفتاح السري المكتوب داخل إعدادات Secrets بموقع Streamlit وعدم احتوائه على مسافات."
            
        res_json = response.json()
        
        if "candidates" in res_json:
            return res_json["candidates"]["content"]["parts"]["text"]
        elif "error" in res_json:
            return f"خطأ في محتوى الاستجابة: {res_json['error'].get('message', 'خطأ غير معروف')}"
        return "تنبيه: استجابة الخادم غير متوافقة مع الصيغة المطلوبة."
    except requests.exceptions.RequestException as e:
        return f"فشل الاتصال بالسيرفر، يرجى المحاولة لاحقاً: {e}"
    except Exception as e:
        return f"حدث خطأ غير متوقع: {e}"

# صندوق الإدخال
user_input = st.text_input("اكتب استفسارك هنا ثم اضغط Enter:", placeholder="أريد معرفة حالة الطلب رقم 1024؟")

if user_input:
    with st.spinner("جاري التفكير والرد..."):
        ai_reply = get_ai_response(user_input)
        st.subheader("🤖 رد المساعد:")
        st.success(ai_reply)