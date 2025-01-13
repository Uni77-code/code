# DIFFICULTY_SCORING_SYSTEM

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load and prepare data
df = pd.read_csv('RQ-2_dataset.csv')

# 1. Question Reception (40%)
scaler = MinMaxScaler()
df['normalized_question_score'] = scaler.fit_transform(df[['Score_question']])

# 2. Response Characteristics (35%)
# Handle dates and response time
df['CreationDate_question'] = pd.to_datetime(df['CreationDate_question'])
df['CreationDate_answer'] = pd.to_datetime(df['CreationDate_answer'].replace('No data', pd.NA), errors='coerce')

# Calculate response time and handle missing values
df['response_time'] = (df['CreationDate_answer'] - df['CreationDate_question']).dt.total_seconds() / 3600
# Fill missing response times with a high value (168 hours / 1 week)
df['response_time'] = df['response_time'].fillna(168)  # One week for missing responses

df['normalized_response_time'] = scaler.fit_transform(df[['response_time']])
df['answer_presence'] = df['Score_answer'].notna().astype(float)
df['normalized_answer_presence'] = scaler.fit_transform(df[['answer_presence']])

# 3. Question Complexity (25%)
df['content_length'] = df['Title'].str.len() + df['Body_question'].str.len()
df['normalized_content_length'] = scaler.fit_transform(df[['content_length']])
df['tag_count'] = df['Tags'].str.count(',') + 1
df['normalized_tag_count'] = scaler.fit_transform(df[['tag_count']])

# Calculate final difficulty score
df['difficulty_score'] = (
    0.40 * df['normalized_question_score'] +
    0.35 * (df['normalized_response_time'] + df['normalized_answer_presence']) / 2 +
    0.25 * (df['normalized_content_length'] + df['normalized_tag_count']) / 2
)

# Print basic scoring statistics 
print("Difficulty Score Statistics:")
print(df['difficulty_score'].describe())

# Calculate thresholds for difficulty categories
thresholds = df['difficulty_score'].quantile([0.33, 0.66])
print("\
Difficulty Thresholds:")
print(f"Easy-Medium Threshold (33rd percentile): {thresholds[0.33]:.3f}")
print(f"Medium-Hard Threshold (66th percentile): {thresholds[0.66]:.3f}")

# Categorise questions
df['difficulty_category'] = pd.cut(
    df['difficulty_score'],
    bins=[-np.inf, thresholds[0.33], thresholds[0.66], np.inf],
    labels=['Easy', 'Medium', 'Hard']
)

# Show distribution
print("\
Difficulty Category Distribution:")
print(df['difficulty_category'].value_counts())