import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Visual Programming - Ultimate Quiz", page_icon="💻")

# تصميم الخطوط والواجهة (خطوط ضخمة وعريضة جداً)
st.markdown("""
    <style>
    .big-font { font-size:34px !important; font-weight: bold; color: #1E1E1E; line-height: 1.3; }
    .ar-font { font-size:26px !important; color: #4A4A4A; font-weight: bold; margin-bottom: 20px; }
    .stRadio [data-testid="stWidgetLabel"] p { font-size: 28px; font-weight: bold; color: #000; }
    .stButton>button { font-size: 24px; font-weight: bold; border-radius: 15px; padding: 15px 35px; background-color: #FF4B4B; color: white; }
    .stage-title { font-size: 45px; font-weight: bold; color: #FF4B4B; text-align: center; border-bottom: 3px solid #FF4B4B; }
    .result-text { font-size: 38px; font-weight: bold; color: #2E7D32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# تهيئة المتغيرات
if 'step' not in st.session_state:
    st.session_state.step = "login"
    st.session_state.score = 0
    st.session_state.current_q = 0
    st.session_state.gender = ""
    st.session_state.user_name = ""
    st.session_state.stage_score = 0

# 40 سؤال تغطي كل المادة (10 لكل مرحلة)
all_questions = [
    # المرحلة 1: أساسيات ومفاهيم (لطيفة وخفيفة)
    {"q": "What does Visual Programming mean?", "ar": "شنو يعني برمجة مرئية؟", "ops": ["Writing text only", "Building with windows and buttons", "Drawing only"], "ans": "Building with windows and buttons"},
    {"q": "Is Code::Blocks an IDE?", "ar": "هل يعتبر Code::Blocks بيئة تطوير متكاملة؟", "ops": ["Yes", "No", "Only for images"], "ans": "Yes"},
    {"q": "What is the result of 5 + 5 in code?", "ar": "شنو نتيجة 5 + 5 بالكود؟", "ops": ["10", "55", "Error"], "ans": "10"},
    {"q": "Does FLTK work with C++?", "ar": "هل مكتبة FLTK تشتغل ويه لغة C++؟", "ops": ["Yes", "No", "Maybe"], "ans": "Yes"},
    {"q": "A 'Window' is a visual element.", "ar": "النافذة (Window) هي عنصر مرئي.", "ops": ["True", "False"], "ans": "True"},
    {"q": "What is the prefix for FLTK functions?", "ar": "شنو هي البادئة لدوال مكتبة FLTK؟", "ops": ["cb_", "fl_", "gui_"], "ans": "fl_"},
    {"q": "Visual Studio is from which company?", "ar": "فيجوال ستوديو من يا شركة؟", "ops": ["Google", "Microsoft", "Apple"], "ans": "Microsoft"},
    {"q": "Is FLTK 'Fast' and 'Light'?", "ar": "هل FLTK سريعة وخفيفة؟", "ops": ["Yes", "No"], "ans": "Yes"},
    {"q": "What color is the console window usually?", "ar": "شنو لون شاشة الكونسول عادةً؟", "ops": ["White", "Black", "Blue"], "ans": "Black"},
    {"q": "Can we drag and drop in Visual C++?", "ar": "نكدر نسوي سحب وإفلات بـ Visual C++؟", "ops": ["Yes", "No"], "ans": "Yes"},

    # المرحلة 2: أدوات وخصائص (المهمة)
    {"q": "Which widget is for user typing?", "ar": "يا أداة نستخدمها حتى المستخدم يكتب بيها؟", "ops": ["Fl_Output", "Fl_Input", "Fl_Box"], "ans": "Fl_Input"},
    {"q": "To change background color, we use:", "ar": "حتى نغير لون الخلفية نستخدم خاصية:", "ops": ["Font", "Color", "Size"], "ans": "Color"},
    {"q": "Fl_Output content can be edited by user.", "ar": "المستخدم يكدر يغير محتوى Fl_Output.", "ops": ["True", "False"], "ans": "False"},
    {"q": "What does 'atoi' convert to?", "ar": "دالة 'atoi' شتحول النص؟", "ops": ["Integer", "Float", "String"], "ans": "Integer"},
    {"q": "Header file for buttons is:", "ar": "ملف الهيدر الخاص بالأزرار هو:", "ops": ["Fl.H", "Fl_Button.H", "cstdlib"], "ans": "Fl_Button.H"},
    {"q": "Position is defined by which values?", "ar": "الموقع يتحدد بيا قيم؟", "ops": ["X and Y", "W and H", "Color"], "ans": "X and Y"},
    {"q": "Which function shows a message?", "ar": "يا دالة تظهر لنا رسالة؟", "ops": ["fl_message()", "cout", "printf"], "ans": "fl_message()"},
    {"q": "To hide a widget, Visible is:", "ar": "حتى نخفي أداة، الـ Visible لازم يكون:", "ops": ["True", "False"], "ans": "False"},
    {"q": "What is the return type of value()?", "ar": "شنو نوع القيمة الراجعة من دالة value()؟", "ops": ["int", "const char*", "float"], "ans": "const char*"},
    {"q": "Size is defined by:", "ar": "الحجم يتحدد بـ:", "ops": ["X/Y", "Width/Height", "Name"], "ans": "Width/Height"},

    # المرحلة 3: دوال وبرمجة (الصعبة)
    {"q": "The first parameter in callback is:", "ar": "أول باراميتر بالـ callback يمثل شنو؟", "ops": ["The Window", "The Widget pointer", "Extra Data"], "ans": "The Widget pointer"},
    {"q": "What does 'void*' mean?", "ar": "شنو معنى 'void*' بالكود؟", "ops": ["Empty", "Generic pointer", "Error"], "ans": "Generic pointer"},
    {"q": "Why use '3.0' for average?", "ar": "ليش نستخدم '3.0' بحساب المعدل؟", "ops": ["Faster", "Ensure float result", "Rule"], "ans": "Ensure float result"},
    {"q": "Function for integer to string is:", "ar": "الدالة اللي تحول الرقم لنص هي:", "ops": ["IntToStr()", "atoi()", "atof()"], "ans": "IntToStr()"},
    {"q": "Does a callback return a value?", "ar": "هل الـ callback ترجع قيمة؟", "ops": ["Yes", "No (void)"], "ans": "No (void)"},
    {"q": "Fl_Button btn(...) creates a:", "ar": "هذا السطر Fl_Button btn(...) يصنع شنو؟", "ops": ["Class", "Object (Widget)", "Function"], "ans": "Object (Widget)"},
    {"q": "Which library started with 'fl_'?", "ar": "يا مكتبة جانت تبدأ بـ 'fl_' قبل FLTK؟", "ops": ["Qt", "Forms Library", "GTK"], "ans": "Forms Library"},
    {"q": "How to clear input 'g1'?", "ar": "شلون نمسح نص بداخل المدخل 'g1'؟", "ops": ["g1->value(\"\")", "g1->clear()", "g1->delete()"], "ans": "g1->value(\"\")"},
    {"q": "What does 'atof' convert to?", "ar": "دالة 'atof' شتحول النص؟", "ops": ["Integer", "Double/Float", "String"], "ans": "Double/Float"},
    {"q": "Every FLTK program needs:", "ar": "كل برنامج FLTK يحتاج هيدر أساسي هو:", "ops": ["Fl_Window.H", "Fl.H", "iostream"], "ans": "Fl.H"},

    # المرحلة 4: تفاصيل الملازم (الاحترافية)
    {"q": "Who chose the name FLTK?", "ar": "منو اختار اسم FLTK؟", "ops": ["Microsoft", "Bill Spitzak", "Google"], "ans": "Bill Spitzak"},
    {"q": "SGI company produced what?", "ar": "شركة SGI جانت تصنع شنو؟", "ops": ["Phones", "High-perf workstations", "Software only"], "ans": "High-perf workstations"},
    {"q": "fl_choice() provides how many buttons?", "ar": "دالة fl_choice() تنطينا كم زر؟", "ops": ["One only", "Multiple (up to 3)", "None"], "ans": "Multiple (up to 3)"},
    {"q": "What does 'const char*' represent?", "ar": "النوع 'const char*' يمثل شنو؟", "ops": ["Number", "C-style string", "Decimal"], "ans": "C-style string"},
    {"q": "Enabled = False means widget is:", "ar": "إذا الـ Enabled خطأ، الأداة تكون:", "ops": ["Hidden", "Not clickable", "Red color"], "ans": "Not clickable"},
    {"q": "Caption property changes the:", "ar": "خاصية Caption تغير شنو بالنافذة؟", "ops": ["Background", "Title/Text", "Size"], "ans": "Title/Text"},
    {"q": "The 'fl_' prefix refers to:", "ar": "بادئة 'fl_' تشير لشنو أصلاً؟", "ops": ["Fast Light", "Forms Library", "Florida"], "ans": "Forms Library"},
    {"q": "In callback, data is passed via:", "ar": "بالـ callback، البيانات الإضافية تمر عبر:", "ops": ["Fl_Widget*", "void* data", "int x"], "ans": "void* data"},
    {"q": "What is the return of Fl::run()?", "ar": "شنو ترجع دالة Fl::run()؟", "ops": ["Zero on success", "An object", "A string"], "ans": "Zero on success"},
    {"q": "Visual programming connects logic with:", "ar": "البرمجة المرئية تربط المنطق (logic) ويه شنو؟", "ops": ["Interface", "Database", "Images only"], "ans": "Interface"}
]

# 1. واجهة الدخول
if st.session_state.step == "login":
    st.markdown('<p class="stage-title">🎓 تحدي مريوم الحلوة الشامل</p>', unsafe_allow_html=True)
    gender = st.radio("نورتونا! أنت/أنتِ:", ["ذكر", "أنثى"], index=None)
    if gender:
        st.session_state.gender = gender
        label = "شنو اسمك يا بطل؟" if gender == "ذكر" else "شنو اسمج يا بطلة؟"
        st.session_state.user_name = st.text_input(label)
        if st.button("نبدأ التحدي الرهيب! 🚀"):
            if st.session_state.user_name:
                st.session_state.step = "quiz"
                st.rerun()

# 2. واجهة الاختبار
elif st.session_state.step == "quiz":
    idx = st.session_state.current_q
    total = len(all_questions)
    stage = (idx // 10) + 1
    
    if idx < total:
        st.markdown(f'<p class="stage-title">📍 المرحلة {stage}</p>', unsafe_allow_html=True)
        st.sidebar.markdown(f"## المرحلة {stage}")
        st.sidebar.progress((idx % 10 + 1) * 10)
        
        q_data = all_questions[idx]
        st.markdown(f'<p class="big-font">Q{idx + 1}: {q_data["q"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="ar-font">({q_data["ar"]})</p>', unsafe_allow_html=True)
        
        key = f"q_{idx}"
        is_answered = key + "_done" in st.session_state
        choice = st.radio("اختر الجواب الصح:", q_data['ops'], key=key, index=None, disabled=is_answered)

        if choice and not is_answered:
            st.session_state[key + "_done"] = True
            st.session_state[key + "_choice"] = choice
            st.rerun()

        if is_answered:
            user_choice = st.session_state[key + "_choice"]
            if user_choice == q_data['ans']:
                st.success(f"**عاش! إجابة صح ✅**")
                if key + "_scored" not in st.session_state:
                    st.session_state.score += 1
                    st.session_state.stage_score += 1
                    st.session_state[key + "_scored"] = True
            else:
                st.error(f"**لاا! ركز/ي.. الصح: {q_data['ans']} ❌**")
            
            if st.button("السؤال التالي ➡️"):
                st.session_state.current_q += 1
                if (st.session_state.current_q % 10 == 0):
                    st.session_state.step = "stage_result"
                st.rerun()
    else:
        st.session_state.step = "result"
        st.rerun()

# 3. نتيجة المرحلة
elif st.session_state.step == "stage_result":
    stage_num = (st.session_state.current_q // 10)
    messages = {1: "بداية تجنن، استمر/ي يا وحش! 😍", 
                2: "الأمور بدت تحمى وأنت/ي كدها! 🔥", 
                3: "مابقى شي.. معلوماتك/ج توب! 💎",
                4: "وصلت/ي للنهاية.. أنت/ي مبرمج/ة حقيقي/ة! 👑"}
    
    st.markdown(f'<p class="stage-title">خلصت المرحلة {stage_num}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-text">درجتك بالمرحلة: {st.session_state.stage_score} من 10</p>', unsafe_allow_html=True)
    st.subheader(f"💡 {messages.get(stage_num)}")
    
    if st.button("نروح للي بعدها؟ ➡️"):
        st.session_state.stage_score = 0
        st.session_state.step = "quiz" if st.session_state.current_q < 40 else "result"
        st.rerun()

# 4. النتيجة النهائية
elif st.session_state.step == "result":
    st.balloons()
    st.markdown('<p class="stage-title">🎊 مبرووووك التخرج من التحدي! 🎊</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-text">النتيجة الكلية: {st.session_state.score} من 40</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="big-font" style="color:#FF4B4B; text-align:center;">فدوة لهالتفكير 😂❤️ مبرمج/ة المستقبل اللي راح يشك الشك ويبدع بالامتحان!</p>', unsafe_allow_html=True)
    
    if st.button("نعيد اللعبة؟ 🔄"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()