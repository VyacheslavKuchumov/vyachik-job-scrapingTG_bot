import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("catigorized_profiles_it.csv")
df = pd.DataFrame(data)






# Группировка данных по 'job_group' и 'entry_date' и подсчет количества вакансий
grouped = df[df["area_name"] == "Приморский край"].groupby(['job_group', 'entry_date']).size().unstack(fill_value=0)

# Рассчитываем процент изменения между датами для каждой группы
percent_change = grouped.pct_change(axis=1) * 100

percent_change.to_excel("primorski_change.xlsx")




# Iterate over each unique job group in the dataframe
# for group in df["job_group"].unique():
#     print(group)
#     group_data = df[df["job_group"] == group]["professional_roles_name"].value_counts()
#     print(group_data)
#     print("\n")

    # # Filter the DataFrame for the current job group
    # group_data = df[df["job_group"] == group]["professional_roles_name"].value_counts()
    #
    # # Plot a pie chart for the current job group
    # plt.figure(figsize=(8, 6))
    # plt.pie(group_data, labels=group_data.index, autopct='%1.1f%%', startangle=140)
    # plt.title(f"Professional Roles Distribution for Job Group: {group}")
    # plt.show()



for group in df["profile"].unique():
    print(group)
    group_data = df[df["profile"] == group]["professional_roles_name"].value_counts()
    print(group_data)
    print("\n")