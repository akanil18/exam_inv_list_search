# st.py
import streamlit as st
import pandas as pd
from extract import extract_records

st.set_page_config(page_title="Invigilation Duty Search", layout="centered")
st.title("📄 Invigilation Duty Search System")

# Upload PDF file
uploaded_file = st.file_uploader("📤 Upload Invigilation Duty PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")

    # Extract records from the uploaded file
    records = extract_records(uploaded_file)

    # Optional: Show preview of extracted records
    if st.checkbox("Show extracted data table"):
        st.subheader("📋 Extracted Records Preview")
        st.dataframe(records)

    # Search section
    st.subheader("🔎 Search Records")
    search_type = st.radio("Search By", ("Teacher Name", "Room No"))

    if search_type == "Teacher Name":
        teacher_query = st.text_input("Enter Teacher Name")
        if teacher_query:
            results = [r for r in records if teacher_query.lower() in r['Teacher'].lower()]
            st.markdown(f"### 🎓 Results for: `{teacher_query}`")
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)

                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                filename = f"Results_for_{teacher_query.replace(' ', '_')}.csv"
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv,
                    file_name=filename,
                    mime='text/csv'
                )
            else:
                st.warning("No matching records found.")

    elif search_type == "Room No":
        room_query = st.text_input("Enter Room (e.g., A Block, C-101, Lab 2)")
        if room_query:
            results = [r for r in records if room_query.lower() in r['Room'].lower()]
            st.markdown(f"### 🏫 Results for: `{room_query}`")
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)

                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                filename = f"Results_for_{room_query.replace(' ', '_')}.csv"
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv,
                    file_name=filename,
                    mime='text/csv'
                )
            else:
                st.warning("No matching records found.")

else:
    st.info("Please upload a PDF file to begin.")
