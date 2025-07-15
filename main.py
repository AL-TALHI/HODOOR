
import streamlit as st

# إعداد الواجهة
st.set_page_config(page_title="برنامج حضور الطلاب", layout="centered", page_icon="📝")

st.title("🟢 برنامج حضور الطلاب")

# شاشة الدخول بكلمة مرور
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 تسجيل الدخول")
    password = st.text_input("أدخل كلمة المرور:", type="password")
    if password == "1234":
        st.session_state.authenticated = True
        st.experimental_rerun()
    elif password:
        st.error("كلمة المرور غير صحيحة ❌")
else:
    st.success("مرحبًا بك! ✅")

    # بقية الواجهة هنا
    class_name = st.text_input("📚 اسم الصف الدراسي")
    student_names = st.text_area("👥 أدخل أسماء الطلاب (كل اسم في سطر)", height=150)

    if student_names:
        names = [name.strip() for name in student_names.split("\n") if name.strip()]
        attendance = {}
        st.subheader("📋 سجل الحضور:")

        for name in names:
            attendance[name] = st.checkbox(f"{name}", key=name)

        if st.button("✅ حفظ الحضور"):
            st.success("تم حفظ الحضور بنجاح!")

        if st.button("📤 تصدير إلى Excel / PDF"):
            st.info("ميزة التصدير قيد التطوير حالياً...")
