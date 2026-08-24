import os
import json
from dotenv import load_dotenv  # 1. استدعاء مكتبة قراءة الملفات المخفية
load_dotenv()                   # 2. تفعيل قراءة ملف الـ .env تلقائياً

from google import genai
from google.genai import types

# 1. تهيئة العميل بمفتاح الـ API الخاص بك
client = genai.Client()

# إنشاء مجلد لحفظ ملفات العملاء إذا لم يكن موجوداً
os.makedirs("customer_profiles", exist_ok=True)

# 2. أداة فحص حالة الطلب (من المرحلة D)
def get_order_status(order_id: str) -> str:
    """يبحث عن تفاصيل وحالة طلب العميل في قاعدة البيانات باستخدام رقم الطلب."""
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)
        if order_id in orders:
            order_info = orders[order_id]
            return f"الطلب {order_id} مؤكد للعميل {order_info['name']} في دورة {order_info['course']}. الحالة الحالية: {order_info['status']}."
        else:
            return f"لم يتم العثور على الطلب رقم {order_id} في النظام."
    except Exception as e:
        return f"خطأ في الوصول لقاعدة البيانات: {e}"

# 3. أداة جديدة: حفظ أو تحديث بيانات العميل (المرحلة E)
def save_customer_profile(customer_id: str, notes: str) -> str:
    """
    تقوم بحفظ أو تحديث ملاحظات ومعلومات وتفضيلات العميل بناءً على معرف العميل (رقم هاتفه أو إيميله أو اسمه).
    
    Args:
        customer_id: معرف العميل الفريد مثل اسم العميل أو هاتفه (مثال: 'أحمد')
        notes: الملاحظات أو التفضيلات الجديدة المراد حفظها (مثال: 'مهتم بدورة الذكاء الاصطناعي')
    """
    file_path = f"customer_profiles/{customer_id}.json"
    profile = {"notes": notes}
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(profile, file, ensure_ascii=False, indent=4)
        return f"تم تحديث وحفظ ملف العميل {customer_id} بنجاح في النظام."
    except Exception as e:
        return f"خطأ أثناء حفظ الملف: {e}"

# 4. أداة جديدة: قراءة بيانات العميل (المرحلة E)
def load_customer_profile(customer_id: str) -> str:
    """تقرأ معلومات وملاحظات العميل السابقة من النظام لمساعدة الـ Agent على تذكره."""
    file_path = f"customer_profiles/{customer_id}.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                profile = json.load(file)
            return f"معلومات سابقة عن العميل {customer_id}: [{profile['notes']}]."
        except Exception as e:
            return f"خطأ في قراءة ملف العميل: {e}"
    else:
        return f"لا توجد معلومات سابقة مسجلة للعميل {customer_id}، هذا أول تواصل له."

# 5. تحديد تعليمات الـ Agent الشاملة (System Instruction)
system_instruction = """
أنت موظف خدمة عملاء ذكي ومحترف للغاية في "أكاديمية التقنية للتدريب"، وتمتلك ذاكرة برمجية لحفظ ملفات العملاء.
مهمتك:
1. مساعدة العملاء في فحص طلباتهم باستخدام أداة (get_order_status).
2. عندما يتحدث معك عميل، اسأله عن اسمه أو معرفه أولاً، واستخدم أداة (load_customer_profile) فوراً لترى إن كان لديه ملف سابق وتتذكره بلطف.
3. إذا ذكر العميل تفضيلات جديدة (مثل: إنه يريد التسجيل الشهر القادم، أو مهتم بالبرمجة، أو لديه شكوى)، استخدم أداة (save_customer_profile) فوراً لحفظ هذه الملاحظات في ملفه لكي لا تنساها الشركة.
أجب دائماً بأدب واختصار، واستخدم الأدوات بذكاء وتلقائية.
"""

print("🤖 جاري تشغيل مساعد خدمة العملاء الذكي (المرحلة E)...")
print("💾 الـ Agent مجهز الآن بذاكرة برمجية وأدوات إدارة ملفات العملاء!")
print("✨ اكتب 'خروج' للإنهاء.\n" + "—" * 40)

# 6. بدء المحادثة المجهزة بجميع الأدوات
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1,
    )
)

# قائمة الأدوات المتاحة للـ Agent
available_tools = [get_order_status, save_customer_profile, load_customer_profile]

# 7. حلقة المحادثة التفاعلية المستمرة
while True:
    user_input = input("👤 أنت: ")
    
    if user_input.strip().lower() in ['خروج', 'exit', 'quit']:
        print("🤖 الـ Agent: شكراً لتواصلك معنا، يومك سعيد!")
        break
        
    if not user_input.strip():
        continue
        
    try:
        response = chat.send_message(
            user_input, 
            config=types.GenerateContentConfig(tools=available_tools)
        )
        
        # حلقة معالجة الأدوات إذا طلبها الـ Agent
        if response.function_calls:
            for call in response.function_calls:
                tool_result = ""
                if call.name == "get_order_status":
                    tool_result = get_order_status(order_id=call.args.get("order_id"))
                elif call.name == "save_customer_profile":
                    tool_result = save_customer_profile(
                        customer_id=call.args.get("customer_id"), 
                        notes=call.args.get("notes")
                    )
                elif call.name == "load_customer_profile":
                    tool_result = load_customer_profile(customer_id=call.args.get("customer_id"))
                
                # إرسال النتيجة مجدداً للموديل ليصيغ الرد النهائي
                response = chat.send_message(tool_result)
        
        print(f"🤖 الـ Agent: {response.text}")
        print("—" * 40)
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الاتصال: {e}")