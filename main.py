
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# --- شاشة دخول ---
def check_login():
    st.title("🔐 تسجيل الدخول")
    password = st.text_input("أدخل كلمة المرور", type="password")
    if password == "1234":
        st.session_state["authenticated"] = True
        st.success("تم تسجيل الدخول بنجاح")
    elif password:
        st.error("كلمة المرور غير صحيحة")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    check_login()
    st.stop()

# --- التطبيق بعد تسجيل الدخول ---
st.set_page_config(page_title="برنامج حضور الطلاب", layout="centered")
st.title("📘 برنامج حضور الطلاب")

# إنشاء مجلد البيانات
if not os.path.exists("data"):
    os.makedirs("data")

# اختيار الصف
grade = st.text_input("📚 اسم الصف:", "الصف الأول")

# إدخال الطلاب
st.markdown("### 👥 أسماء الطلاب")
student_names = st.text_area("أدخل أسماء الطلاب (كل اسم في سطر)", height=200)

if student_names:
    students = [name.strip() for name in student_names.strip().split("\n") if name.strip()]
    st.markdown("### 🗓️ جدول الحضور")
    status = {}
    for student in students:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{student}**")
        with col2:
            status[student] = st.radio("", ["حاضر", "غائب"], horizontal=True, key=student)

    if st.button("✅ حفظ الحضور"):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"data/{grade}_{date_str}.csv"
        df = pd.DataFrame([{"الاسم": k, "الحالة": v} for k, v in status.items()])
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        st.success(f"📁 تم الحفظ في: {filename}")

        # إحصائيات
        hadir = (df["الحالة"] == "حاضر").sum()
        ghaib = (df["الحالة"] == "غائب").sum()
        percent = round(hadir / len(df) * 100, 2)
        st.info(f"✅ الحضور: {hadir} | ❌ الغياب: {ghaib} | النسبة: {percent}%")

        # --- تصدير PDF وExcel ---
        st.markdown("### 📤 تصدير البيانات")
        colx1, colx2 = st.columns(2)
        with colx1:
            st.download_button("⬇️ تحميل Excel", df.to_csv(index=False).encode('utf-8-sig'), file_name=f"{grade}_{date_str}.csv", mime="text/csv")
        with colx2:
            pdf_text = df.to_string(index=False)
            pdf_bytes = BytesIO()
            pdf_bytes.write(pdf_text.encode('utf-8'))
            st.download_button("⬇️ تحميل PDF (نص)", pdf_bytes.getvalue(), file_name=f"{grade}_{date_str}.pdf", mime="application/pdf")

else:
    st.warning("يرجى إدخال أسماء الطلاب.")
