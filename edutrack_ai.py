import streamlit as st
import pandas as pd

# App title
st.title("📘 EduTrack AI – Institutional Document Analyzer")
st.write("Upload institutional documents (text or CSV) to check completeness and calculate performance score.")

# List of required documents
required_docs = [
    "Affiliation Certificate",
    "Faculty List",
    "Infrastructure Report",
    "Accreditation Certificate",
    "Fee Structure",
    "Student Enrollment Data"
]

# File uploader
uploaded_files = st.file_uploader(
    "Upload Documents (.txt or .csv)", 
    type=["txt", "csv"], 
    accept_multiple_files=True
)

if uploaded_files:
    extracted_docs = []

    st.subheader("📄 Extracted Text from Documents")
    for file in uploaded_files:
        st.write(f"**Document:** {file.name}")
        # Read text
        if file.name.endswith(".txt"):
            text = file.read().decode("utf-8")
        elif file.name.endswith(".csv"):
            df_csv = pd.read_csv(file)
            text = " ".join(df_csv.astype(str).values.flatten())
        else:
            text = ""
        st.text_area("Extracted Text", text, height=150)
        extracted_docs.append(text)

    # Combine all text and check required documents
    all_text = " ".join(extracted_docs).lower()
    count_present = sum(1 for req in required_docs if req.lower() in all_text)

    # Document sufficiency
    sufficiency = (count_present / len(required_docs)) * 100
    st.subheader("📊 Document Sufficiency")
    st.metric("Sufficiency Score", f"{sufficiency:.2f}%")

    # Simple performance score
    performance_score = min(100, sufficiency + 10)
    st.subheader("📈 Institution Performance Indicator (IPI)")
    st.metric("IPI Score", f"{performance_score:.2f}")

    # Document checklist table
    st.subheader("📋 Document Checklist")
    df = pd.DataFrame({
        "Document": required_docs,
        "Status": ["Present" if req.lower() in all_text else "Missing" for req in required_docs]
    })
    st.table(df)
