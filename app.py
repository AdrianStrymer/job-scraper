import streamlit as st
import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt

st.title("Computing Job Keyword Analyser")

csv_files = [f for f in os.listdir() if f.endswith(".csv")]
if not csv_files:
    st.warning("No CSV files found in the current directory.")
    st.stop()

st.subheader("Available CSV Files")
st.write(csv_files)

selected_file = st.selectbox("Select a CSV file to analyze:", csv_files)

keywords = ['aws', 'python', 'docker', 'kubernetes', 'azure', 'java', 'c#', 'sql', 'javascript', 'linux', 'c++', 'github', 'git', 'shell', 'ai', 'react']

if st.button("Analyse"):
    try:
        df = pd.read_csv(selected_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    if not {"Job Title", "Full Description"}.issubset(df.columns):
        st.error("CSV must contain 'Job Title' and 'Full Description' columns.")
        st.stop()

    counts = Counter()
    for _, row in df.iterrows():
        text = f"{row['Job Title']} {row['Full Description']}".lower()
        for kw in keywords:
            if kw in text:
                counts[kw] += 1

    result_df = pd.DataFrame(counts.items(), columns=["Keyword", "Matches"]).sort_values("Matches", ascending=False)

    st.subheader("Keyword Match Summary")
    st.dataframe(result_df)

    st.subheader("Match Frequency Chart")
    fig, ax = plt.subplots()
    ax.bar(result_df["Keyword"], result_df["Matches"])
    ax.set_ylabel("Number of Listings")
    ax.set_xlabel("Keyword")
    ax.set_title("Job Listings Matching Each Keyword")
    plt.xticks(rotation=75)
    plt.tight_layout()
    st.pyplot(fig)