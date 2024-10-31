import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("catigorized_jobs.csv")
df = pd.DataFrame(data)


# Iterate over each unique job group in the dataframe
for group in df["job_group"].unique():
    # Filter the DataFrame for the current job group
    group_data = df[df["job_group"] == group]["professional_roles_name"].value_counts()

    # Plot a pie chart for the current job group
    plt.figure(figsize=(8, 6))
    plt.pie(group_data, labels=group_data.index, autopct='%1.1f%%', startangle=140)
    plt.title(f"Professional Roles Distribution for Job Group: {group}")
    plt.show()