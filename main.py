from google import genai

# اصق مفتاحك السري هنا مباشرة بين علامتي التنصيص
MY_API_KEY ="AQ.Ab8RN6KMjmlAqqCjNxNqUAtY4UT_Qk91E_5tVELzV86MrQvjvw"

# إعداد عميل جوجل بالمفتاح الخاص بك
client = genai.Client(api_key=MY_API_KEY)

try:
    # إرسال سؤال للنموذج الذكي المجاني
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents='Write a short welcome message for an AI programmer in Arabic.',
    )
    
    # طباعة الإجابة الحية بالأسفل
    print("\n🤖 Gemini Response:")
    print(response.text)

except Exception as e:
    print(f"\n❌ Error: {e}")