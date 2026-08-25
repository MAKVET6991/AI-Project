import streamlit as st
import sqlite3

# 1. إعدادات مظهر واجهة التطبيق العالمية
st.set_page_config(page_title="منصة المحادثات الآمنة", page_icon="🔐", layout="centered")

# 2. إنشاء والاتصال بقاعدة البيانات وإعداد الجداول
def init_db():
    conn = sqlite3.connect("company_chat.db")
    cursor = conn.cursor()
    # جدول الرسائل
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            text TEXT
        )
    """)
    # جدول حسابات الموظفين (المستخدمين)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    # إضافة مستخدم تجريبي افتراضي للشركة (اسم المستخدم: admin / كلمة المرور: 1234)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
    except sqlite3.IntegrityError:
        pass # المستخدم موجود بالفعل
        
    conn.commit()
    conn.close()

init_db()

# 3. دالتان للتعامل مع قاعدة البيانات
def check_login(username, password):
    conn = sqlite3.connect("company_chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def save_message(sender, text):
    conn = sqlite3.connect("company_chat.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, text) VALUES (?, ?)", (sender, text))
    conn.commit()
    conn.close()

def load_messages():
    conn = sqlite3.connect("company_chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sender, text FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ai_chat_response(user_query):
    query_clean = user_query.strip().lower()
    if "مرحبا" in query_clean or "أهلا" in query_clean:
        return "أهلاً بك في نظام الشركة المحمي! أنا مساعدك الذكي والموظف الخارق. كيف يمكنني خدمتك اليوم؟"
    if "أفكار" in query_clean or "مبيعات" in query_clean:
        return (
            "إليك فكرة تسويقية عبقرية لزيادة المبيعات عبر التطبيق:\n\n"
            "🎯 *الشحن المجاني المشروط:* تقديم شحن مجاني كامل فقط للطلبات التي تتجاوز قيمتها حداً معيناً (مثل 200 ريال/درهم) لرفع قيمة الفاتورة!"
        )
    return "أهلاً بك! تفضل بطرح استفسارك وسأجيبك بدقة باللغة العربية."

# 4. التحكم في حالة تسجيل الدخول (ذاكرة الجلسة)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔒 الشاشة الأولى: إذا لم يكن المستخدم مسجلاً دخوله، نعرض واجهة الأمان
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول إلى المنصة السرية")
    st.write("الرجاء إدخال بيانات حسابك الموظف للدخول إلى غرف المحادثات وبوت الذكاء الاصطناعي.")
    
    username_input = st.text_input("اسم المستخدم (Username):")
    password_input = st.text_input("كلمة المرور (Password):", type="password")
    
    login_button = st.button("تسجيل الدخول")
    
    if login_button:
        if check_login(username_input, password_input):
            st.session_state.logged_in = True
            st.success("تم التحقق بنجاح! جاري تحويلك للمنصة...")
            st.rerun()
        else:
            st.error("خطأ: اسم المستخدم أو كلمة المرور غير صحيحة! يرجى المحاولة مجدداً.")

# 🔓 الشاشة الثانية: واجهة غرف الدردشة والمساعد الذكي (تظهر فقط بعد تسجيل الدخول الناجح)
else:
    st.title("💬 غرف المحادثات الاحترافية والمحمية")
    
    # زر لتسجيل الخروج
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state.logged_in = False
        st.rerun()
        
    # عرض الرسائل المخزنة
    saved_chats = load_messages()
    for sender, text in saved_chats:
        with st.chat_message(sender):
            st.write(text)

    # صندوق الإدخال التفاعلي
    user_input = st.chat_input("اكتب رسالتك للموظفين أو للمساعد الذكي هنا...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        save_message("user", user_input)
        
        with st.spinner("جاري تفكير المساعد..."):
            ai_reply = get_ai_chat_response(user_input)
            
        with st.chat_message("assistant"):
            st.write(ai_reply)
        save_message("assistant", ai_reply)