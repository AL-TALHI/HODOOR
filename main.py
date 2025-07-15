
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="برنامج حضور الطلاب", layout="centered")
st.title("📘 برنامج حضور الطلاب")
st.markdown("### سجل حضور وغياب الطلاب بسهولة")

# إنشاء مجلد لتخزين البيانات
if not os.path.exists("data"):
    os.makedirs("data")

# اختيار الصف
grade = st.text_input("📚 أدخل اسم الصف:", "الصف الأول")

# إدخال أسماء الطلاب
st.markdown("### 👥 أسماء الطلاب")
student_names = st.text_area("أدخل أسماء الطلاب (كل اسم في سطر)", height=200)

if student_names:
    students = [name.strip() for name in student_names.strip().split("\n") if name.strip()]

    # عرض جدول الحضور
    st.markdown("### 🗓️ جدول الحضور والغياب")
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
        st.success(f"تم حفظ الحضور في الملف: {filename}")

        # إحصائيات
        st.markdown("### 📊 الإحصائيات")
        total = len(df)
        hadir = (df["الحالة"] == "حاضر").sum()
        ghaib = (df["الحالة"] == "غائب").sum()
        percent = round(hadir / total * 100, 2)
        st.info(f"📌 عدد الطلاب: {total} | ✅ حاضر: {hadir} | ❌ غائب: {ghaib} | نسبة الحضور: {percent}%")

else:
    st.warning("يرجى إدخال أسماء الطلاب أولاً.")
