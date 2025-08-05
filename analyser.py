import csv
from collections import Counter

keywords = ['aws', 'python', 'docker', 'kubernetes', 'azure', 'java', 'c#', 'sql', 'javascript', 'linux', 'c++', 'github', 'git', 'shell', 'ai', 'react']

filename = input("Enter the CSV filename (e.g., devops_jobs.csv): ").strip()

keyword_counts = Counter()

with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        text = (row["Job Title"] + " " + row["Full Description"]).lower()
        for keyword in keywords:
            if keyword in text:
                keyword_counts[keyword] += 1

print("\nKeyword frequency in job listings:\n")
for keyword, count in keyword_counts.most_common():
    print(f"{keyword.upper():<12}: {count}")