import pandas as pd
import ast

# Load the dataset
df = pd.read_csv('RQ-2_dataset.csv')

# Clean and explode the Tags column
df['Tags'] = df['Tags'].str.strip('[]').str.replace("'", "").str.split(', ')
df_exploded = df.explode('Tags')

# Calculate the top ten tags by question volume
top_tags = df_exploded['Tags'].value_counts().head(10).reset_index()
top_tags.columns = ['Tag', 'Question Volume']

# Display the top ten tags
top_tags

# Get temporal data for top tags
top_10_tags = top_filtered_tags['Tag'].tolist()

# Group by year and tag, count questions
temporal_data = (df_exploded[df_exploded['Tags'].isin(top_10_tags)]
                .groupby(['year', 'Tags'])
                .size()
                .reset_index(name='count'))

# Create temporal visualisation
plt.figure(figsize=(15, 8))

# Plot each tag's trend
for tag in top_10_tags:
    tag_data = temporal_data[temporal_data['Tags'] == tag]
    plt.plot(tag_data['year'], tag_data['count'], marker='o', label=tag, linewidth=2)

plt.title('Evolution of Top Python Tags Over Time (2008-2016)', pad=20)
plt.xlabel('Year')
plt.ylabel('Number of Questions')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('temporal_tags_trends.png', bbox_inches='tight')
plt.show()

# Print growth rates for each tag
print("\
Growth Rates (2008 to 2016):")
for tag in top_10_tags:
    tag_data = temporal_data[temporal_data['Tags'] == tag]
    if len(tag_data) >= 2:
        first_year = tag_data.iloc[0]['count']
        last_year = tag_data.iloc[-1]['count']
        if first_year > 0:  # Avoid division by zero
            growth = ((last_year - first_year) / first_year) * 100
            print(f"{tag}: {growth:.1f}%")