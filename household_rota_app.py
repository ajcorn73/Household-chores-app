
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Household Rota Generator", layout="centered")

st.title("🏡 Household Rota Generator")

with st.sidebar:
    st.header("Settings")
    people = st.text_input("Enter household members (comma separated)", "Dad,Oliver,Bella")
    tasks = st.text_input("Enter daily tasks (comma separated)", "Empty Dishwasher,Fill Dishwasher,Lay the Table,Wipe Down Sides,Clear the Table")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    generate_button = st.button("Generate New Rota")

people = [p.strip() for p in people.split(",") if p.strip()]
tasks = [t.strip() for t in tasks.split(",") if t.strip()]

if generate_button:
    total_tasks = len(days) * len(tasks)
    base_jobs = total_tasks // len(people)
    extra_jobs = total_tasks % len(people)

    # Prepare the job distribution
    job_distribution = []
    for i, person in enumerate(people):
        count = base_jobs + (1 if i < extra_jobs else 0)
        job_distribution += [person] * count
    random.shuffle(job_distribution)

    # Build the rota
    rota = {}
    for day in days:
        day_assignments = []
        for _ in tasks:
            if job_distribution:
                day_assignments.append(job_distribution.pop())
            else:
                day_assignments.append(random.choice(people))
        rota[day] = day_assignments

    df_rota = pd.DataFrame(rota, index=tasks).T
    st.subheader("📅 7-Day Rota")
    st.dataframe(df_rota)

    csv = df_rota.to_csv().encode('utf-8')
    st.download_button("📥 Download CSV", csv, "rota.csv", "text/csv")
