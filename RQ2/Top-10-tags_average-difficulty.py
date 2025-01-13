import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load the tag mapping dataset
df_tag_mapping = pd.read_csv('df_tag_mapping_cleaned.csv')

# Exclude the 'python' tag
df_tag_mapping = df_tag_mapping[df_tag_mapping['tag'] != 'python']

# Calculate tag frequency
tag_frequency = df_tag_mapping['tag'].value_counts()

# Calculate average score per tag
avg_score_per_tag = df_tag_mapping.groupby('tag')['score'].mean().sort_values(ascending=False)

# Calculate difficulty score
df_tag_mapping['difficulty_score'] = (1 - df_tag_mapping['score'].rank(pct=True)) + \
                                     df_tag_mapping['tag'].map(tag_frequency).rank(pct=True)

# Normalise difficulty score
df_tag_mapping['difficulty_score'] = (df_tag_mapping['difficulty_score'] - df_tag_mapping['difficulty_score'].min()) / \
                                     (df_tag_mapping['difficulty_score'].max() - df_tag_mapping['difficulty_score'].min())

# Calculate average difficulty score per tag
avg_difficulty_per_tag = df_tag_mapping.groupby('tag')['difficulty_score'].mean().sort_values(ascending=False)

# Display top 10 most difficult tags

print(avg_difficulty_per_tag.head(10))

# Visualize top 10 tags by average difficulty
top_10_tags = avg_difficulty_per_tag.head(10)
fig = px.bar(x=top_10_tags.index, y=top_10_tags.values,
             title='Top 10 Tags by Average Difficulty',
             labels={'x': 'Tag', 'y': 'Average Difficulty Score'},
             color=top_10_tags.index,  # Use tag names for colors
             color_discrete_sequence=px.colors.qualitative.Set3)  
fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', font_color='#333333')
fig.update_xaxes(tickangle=45)
fig.show()