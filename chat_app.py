# توليد رد الذكاء الاصطناعي الفعلي بناءً على السؤال الحالي والتاريخ
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    # نرسل كامل المحادثة المخزنة في الذاكرة للـ API ليتذكر السياق كاملاً
                    formatted_history = []
                    for msg in st.session_state.messages[:-1]: # نرسل التاريخ القديم أولاً
                        role = "user" if msg["role"] == "user" else "model"
                        formatted_history.append({"role": role, "parts": [msg["content"]]})
                    
                    # بدء المحادثة مع إرسال التاريخ (هنا المسافات الإضافية)
                    chat = model.start_chat(history=formatted_history)
                    response = chat.send_message(user_input)
                    bot_response = response.text
                    
                    st.write(bot_response)
                except Exception as e:
                    # هنا المسافات الإضافية لرد الخطأ
                    bot_response = "AQ.Ab8RN6IIJ8M2519orDMl_-yHxpzBYvirNcg_XrRVR7StE1TuJg."
                    st.write(bot_response)