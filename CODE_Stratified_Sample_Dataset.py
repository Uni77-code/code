import numpy as np

# Load the dataset
df = pd.read_csv('RQ-2_dataset.csv')

# Check the distribution of years
year_dist = df['year'].value_counts(normalize=True)
print("Original Year Distribution:")
print(year_dist.sort_index())

# Calculate total sample size (10%)
sample_size = len(df) // 10

print("\
Original dataset size:", len(df))
print("Target sample size:", sample_size)

# Create stratified systematic sample
def systematic_sample(data, step):
    return data.iloc[::step]

# Initialize empty dataframe for the sample
sampled_df = pd.DataFrame()

# Calculate sampling fraction
sampling_fraction = sample_size / len(df)

# Perform stratified systematic sampling
for year in df['year'].unique():
    # Get stratum
    stratum = df[df['year'] == year]
    
    # Calculate stratum sample size
    stratum_sample_size = int(len(stratum) * sampling_fraction)
    
    # Calculate step size for systematic sampling
    step = max(len(stratum) // stratum_sample_size, 1)
    
    # Take systematic sample from stratum
    stratum_sample = systematic_sample(stratum, step)
    
    # Append to final sample
    sampled_df = pd.concat([sampled_df, stratum_sample])

# Verify the sample size and distribution
print("Sample size:", len(sampled_df))
sample_year_dist = sampled_df['year'].value_counts(normalize=True)
print("\
Sample Year Distribution:")
print(sample_year_dist.sort_index())

# Calculate and display the difference in distributions
print("\
Difference in proportions (Sample - Original):")
diff = (sample_year_dist - year_dist).sort_index()
print(diff)

# Save the sample
sampled_df.to_csv('RQ-2_dataset.csv', index=False)
