import streamlit as st
import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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

    st.subheader("Top Job Locations")
    df["Location"] = df["Location"].apply(
    lambda x: "Dublin" if "dublin" in str(x).lower() else x.strip()
    )
    location_counts = df["Location"].value_counts().head(10)

    fig1, ax1 = plt.subplots()
    ax1.bar(location_counts.index, location_counts.values, color="skyblue")
    ax1.set_xlabel("Location")
    ax1.set_ylabel("Number of Jobs")
    ax1.set_title("Job Locations")
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig1)


    st.subheader("Top Hiring Companies")
    company_counts = df["Company"].value_counts().head(10)

    fig2, ax2 = plt.subplots()
    ax2.bar(company_counts.index, company_counts.values, color="salmon")
    ax2.set_xlabel("Company")
    ax2.set_ylabel("Number of Jobs")
    ax2.set_title("Hiring Companies")
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig2)