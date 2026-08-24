from google import genai
from arabic_reshaper import reshape
from bidi.algorithm import get_display

client = genai.Client(api_key="AQ.Ab8RN6KBi5YyjgHY8C8HUM0-5vEechtJ3CAYTqBKgKuJLn96EQ")
response = client.models.generate_content(model="gemini-3.6-flash", contents="مرحبا، كيف يمكنني الشراء من المتجر؟ أجبني بالعربية باختصار")

print(get_display(reshape(response.text)))