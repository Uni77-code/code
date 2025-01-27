import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
tag_df = pd.read_csv('df_tag_mapping.csv')

# Top 15 libraries from previous analysis
top_15_libraries = ['django', 'numpy', 'pandas', 'matplotlib', 'tkinter', 
                   'flask', 'scipy', 'beautifulsoup', 'sqlalchemy', 'selenium',
                   'pygame', 'pyqt', 'opencv', 'pillow', 'requests']

# Convert creation_date to datetime
tag_df['creation_date'] = pd.to_datetime(tag_df['creation_date'])
tag_df['year'] = tag_df['creation_date'].dt.year

# Calculate yearly counts for each library
yearly_counts = []
for lib in top_15_libraries:
    lib_data = tag_df[tag_df['tag'] == lib].groupby('year').size().reset_index()
    lib_data.columns = ['year', 'count']
    lib_data['library'] = lib
    yearly_counts.append(lib_data)

yearly_df = pd.concat(yearly_counts)

# Create the temporal trend plot
plt.figure(figsize=(15, 8))
for lib in top_15_libraries:
    lib_data = yearly_df[yearly_df['library'] == lib]
    plt.plot(lib_data['year'], lib_data['count'], marker='o', label=lib)

plt.title('Python Library Popularity Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Questions')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Calculate and print summary statistics
print("\
Summary Statistics for Top 15 Libraries:")
summary_stats = []
for lib in top_15_libraries:
    stats = tag_df[tag_df['tag'] == lib]['score'].describe()
    stats['library'] = lib
    summary_stats.append(stats)

summary_df = pd.DataFrame(summary_stats)
print(summary_df)