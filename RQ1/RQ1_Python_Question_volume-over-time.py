# Plot the trends in question volume over the years
# import dataset
data = pd.read_csv('RQ-2_dataset.csv')

# Group by year and count the number of questions per year
questions_per_year = data.groupby('Year').size().reset_index(name='QuestionCount')

# Question creation dates format
data['CreationDate_question'] = pd.to_datetime(data['CreationDate_question'])
data['Year'] = data['CreationDate_question'].dt.year

# Plot the trends in Python-related questions over time
plt.figure(figsize=(10, 6))
sns.lineplot(data=questions_per_year, x='Year', y='QuestionCount', marker='o')
plt.title('Trends in Python-Related Questions Over Time', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Questions', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.savefig('python_trends_over_time.png')
plt.show()

