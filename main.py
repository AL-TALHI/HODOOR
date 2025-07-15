
import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="برنامج حضور الطلاب", layout="centered", page_icon="📝")
st.title("🟢 برنامج حضور الطلاب")

# تخزين حالة تسجيل الدخول في الجلسة
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# شاشة تسجيل الدخول
if not st.session_state["authenticated"]:
    st.subheader("🔐 تسجيل الدخول")
    password = st.text_input("أدخل كلمة المرور:", type="password")
    login_btn = st.button("دخول")
    if login_btn:
        if password == "1234":
            st.session_state["authenticated"] = True
            st.success("تم تسجيل الدخول بنجاح ✅")
        else:
            st.error("كلمة المرور غير صحيحة ❌")
else:
    # بعد تسجيل الدخول
    st.success("✅ تم تسجيل الدخول!")

    st.subheader("📌 معلومات الحصة:")
    class_options = ["الصف الأول", "الصف الثاني", "الصف الثالث"]
    subject_options = ["رياضيات", "علوم", "لغة عربية", "تاريخ"]

    selected_class = st.selectbox("📚 اختر الصف الدراسي:", class_options)
    selected_subject = st.selectbox("📘 اختر المادة:", subject_options)

    uploaded_file = st.file_uploader("📥 رفع ملف Excel يحتوي على عمود 'الاسم':", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            if "الاسم" not in df.columns:
                st.error("⚠️ الملف لا يحتوي على عمود اسمه 'الاسم'")
            else:
                names = df["الاسم"].dropna().tolist()
                attendance = {}
                st.subheader("📋 سجل الحضور:")

                for name in names:
                    attendance[name] = st.checkbox(f"{name}", key=name)

                if st.button("✅ حفظ الحضور"):
                    st.success("تم حفظ الحضور بنجاح!")

                if st.button("📤 تصدير إلى Excel / PDF"):
                    st.info("ميزة التصدير قيد التطوير حالياً...")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
