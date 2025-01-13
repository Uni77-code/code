# Load and clean data, remove 'python' tag
import pandas as pd
import numpy as np
from collections import defaultdict

# Load the dataset
df = pd.read_csv('RQ-2_dataset.csv')

# Clean the Tags column and remove 'python' tag
df['Tags'] = df['Tags'].str.strip('[]').str.replace("'", "").str.split(', ')
df['Tags'] = df['Tags'].apply(lambda x: [tag for tag in x if tag != 'python'])

# Create tag co-occurrence matrix without python
tag_pairs = []
for tags in df['Tags']:
    pairs = [(t1, t2) for i, t1 in enumerate(tags) for t2 in tags[i+1:]]
    tag_pairs.extend(pairs)

# Count co-occurrences
cooccurrence = defaultdict(int)
for t1, t2 in tag_pairs:
    if t1 < t2:
        cooccurrence[(t1, t2)] += 1
    else:
        cooccurrence[(t2, t1)] += 1

# Convert to DataFrame and filter significant relationships
cooccur_df = pd.DataFrame([(t1, t2, count) for (t1, t2), count in cooccurrence.items()],
                         columns=['tag1', 'tag2', 'count'])
significant_cooccur = cooccur_df[cooccur_df['count'] >= 25].sort_values('count', ascending=False)

print("Top 20 Most Common Tag Pairs (without 'python'):")
print(significant_cooccur.head(20))

# Find hierarchical relationships
def find_parent_child_relationships(cooccur_df, min_count=25):
    relationships = defaultdict(list)
    for tag in set(cooccur_df['tag1'].unique()) | set(cooccur_df['tag2'].unique()):
        tag_cooccur = cooccur_df[
            ((cooccur_df['tag1'] == tag) | (cooccur_df['tag2'] == tag)) &
            (cooccur_df['count'] >= min_count)
        ]
        
        if len(tag_cooccur) > 0:
            related_tags = []
            for _, row in tag_cooccur.iterrows():
                other_tag = row['tag2'] if row['tag1'] == tag else row['tag1']
                related_tags.append((other_tag, row['count']))
            related_tags.sort(key=lambda x: x[1], reverse=True)
            relationships[tag] = related_tags
    
    return relationships

hierarchical_relationships = find_parent_child_relationships(cooccur_df)

print("\
Example Tag Hierarchies without 'python' (showing top 5 related tags for each):")
for tag, related in sorted(hierarchical_relationships.items(), 
                         key=lambda x: sum(count for _, count in x[1]), 
                         reverse=True)[:10]:
    print(f"\
{tag}:")
    for related_tag, count in related[:5]:
        print(f"  - {related_tag} ({count} co-occurrences)")