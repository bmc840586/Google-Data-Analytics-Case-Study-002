import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load daily activity dataset
df_act = pd.read_csv('dailyActivity_merged.csv')

# Clean date column
df_act['ActivityDate'] = pd.to_datetime(df_act['ActivityDate'])
df_act['DayOfWeek'] = df_act['ActivityDate'].dt.day_name()

# Order days of week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_act['DayOfWeek'] = pd.Categorical(df_act['DayOfWeek'], categories=day_order, ordered=True)

# Remove 0 step days (non-wear days)
df_clean = df_act[df_act['TotalSteps'] > 0].copy()

# Summary by Day of Week
weekly_summary = df_clean.groupby('DayOfWeek', observed=False).agg(
    AvgSteps=('TotalSteps', 'mean'),
    AvgCalories=('Calories', 'mean'),
    AvgSedentaryMins=('SedentaryMinutes', 'mean'),
    AvgVeryActiveMins=('VeryActiveMinutes', 'mean'),
    AvgLightlyActiveMins=('LightlyActiveMinutes', 'mean')
).reset_index()

print("Weekly Summary Statistics:")
print(weekly_summary)

# Plotting Daily Steps and Sedentary Minutes
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Average Steps by Day of Week
sns.barplot(data=weekly_summary, x='DayOfWeek', y='AvgSteps', ax=axes[0], palette='viridis')
axes[0].set_title('Average Daily Steps by Day of Week', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Day of the Week', fontsize=12)
axes[0].set_ylabel('Average Steps', fontsize=12)
axes[0].axhline(10000, color='red', linestyle='--', label='10,000 Steps Goal')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=45)

# Plot 2: Breakdown of Active vs Sedentary Minutes
sns.barplot(data=weekly_summary, x='DayOfWeek', y='AvgSedentaryMins', ax=axes[1], palette='magma')
axes[1].set_title('Average Sedentary Minutes by Day of Week', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Day of the Week', fontsize=12)
axes[1].set_ylabel('Average Sedentary Minutes', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('bellabeat_weekly_trends.png')
plt.show()