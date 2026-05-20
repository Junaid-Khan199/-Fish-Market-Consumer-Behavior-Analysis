# ============================
# 📌 Import Libraries
# ============================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, f_oneway

# ============================
# 📌 Load Dataset
# ============================
df = pd.read_excel("D:/Sir Sayab's Project/Fish_Market _Dataset.xlsx")
df.columns = df.columns.str.strip()   # Clean column names

# ============================
# 📌 Group 1: Age Group vs Fish Type
# ============================
bins = [15, 25, 35, 50, 70]
labels = ['15-25', '26-35', '36-50', '51-70']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

age_fish_summary = df.groupby(['age_group', 'fish type']).size().unstack().fillna(0)
print("\n=== Fish Type Preference by Age Group ===")
print(age_fish_summary)

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='age_group', hue='fish type')
plt.title("Fish Type Preference by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Count")
plt.legend(title="Fish Type")
plt.tight_layout()
plt.show()

# ============================
# 📌 Group 2: Education vs Reason for Buying
# ============================
edu_reason_summary = df.groupby(['education', 'reason for buying fish']).size().unstack().fillna(0)
print("\n=== Reason for Buying Fish by Education Level ===")
print(edu_reason_summary)

plt.figure(figsize=(10,5))
sns.countplot(data=df, x='education', hue='reason for buying fish')
plt.title("Reason for Buying Fish by Education Level")
plt.xticks(rotation=45)
plt.xlabel("Education Level")
plt.ylabel("Count")
plt.legend(title="Reason")
plt.tight_layout()
plt.show()

# ============================
# 📌 Group 3: Household Size vs Fish Size
# ============================
house_fish_summary = df.groupby(['house hold size', 'fish size']).size().unstack().fillna(0)
print("\n=== Fish Size Preference by Household Size ===")
print(house_fish_summary)

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='house hold size', hue='fish size')
plt.title("Fish Size Purchased by Household Type")
plt.xlabel("Household Size")
plt.ylabel("Count")
plt.legend(title="Fish Size")
plt.tight_layout()
plt.show()

# ============================
# 📌 ANOVA: Age vs Fish Size
# ============================
df_anova = df.dropna(subset=['age', 'fish size'])
groups = [group['age'].values for _, group in df_anova.groupby('fish size')]
f_stat, p_val = f_oneway(*groups)

print("\n=== ANOVA: Age vs Fish Size ===")
print("F-statistic:", round(f_stat, 2))
print("p-value:", round(p_val, 4))
print("Conclusion:", "✅ Significant difference" if p_val < 0.05 else "❌ No significant difference")

# ============================
# 📌 Chi-Square Tests
# ============================

# 1. Age Group vs Fish Type
df_chi = df.dropna(subset=['age_group', 'fish type'])
contingency_table = pd.crosstab(df_chi['age_group'], df_chi['fish type'])
chi2, p, dof, _ = chi2_contingency(contingency_table)
print("\n=== Chi-Square Test: Age Group vs Fish Type ===")
print("Chi-square:", round(chi2, 2), "| p-value:", round(p, 4), "| dof:", dof)
print("Conclusion:", "✅ Significant association" if p < 0.05 else "❌ No significant association")

# 2. Education vs Reason
df_clean = df.dropna(subset=['education', 'reason for buying fish'])
table = pd.crosstab(df_clean['education'], df_clean['reason for buying fish'])
chi2, p, dof, _ = chi2_contingency(table)
print("\n=== Chi-Square Test: Education vs Reason ===")
print("Chi-square:", round(chi2, 2), "| p-value:", round(p, 4), "| dof:", dof)
print("Conclusion:", "✅ Significant association" if p < 0.05 else "❌ No significant association")

# 3. Household Size vs Fish Size
df_clean = df.dropna(subset=['house hold size', 'fish size'])
table = pd.crosstab(df_clean['house hold size'], df_clean['fish size'])
chi2, p, dof, _ = chi2_contingency(table)
print("\n=== Chi-Square Test: Household Size vs Fish Size ===")
print("Chi-square:", round(chi2, 2), "| p-value:", round(p, 4), "| dof:", dof)
print("Conclusion:", "✅ Significant association" if p < 0.05 else "❌ No significant association")

# 4. SES vs Fish Size
df_clean = df.dropna(subset=['socioeconomic status', 'fish size'])
table = pd.crosstab(df_clean['socioeconomic status'], df_clean['fish size'])
chi2, p, _, _ = chi2_contingency(table)
print("\n=== Chi-Square Test: SES vs Fish Size ===")
print("Chi-square:", round(chi2, 2), "| p-value:", round(p, 4))
print("Conclusion:", "✅ SES affects fish size preference" if p < 0.05 else "❌ No significant association")

# 5. SES vs Buying Frequency
df_clean2 = df.dropna(subset=['socioeconomic status', 'frequency'])
table2 = pd.crosstab(df_clean2['socioeconomic status'], df_clean2['frequency'])
chi2, p, _, _ = chi2_contingency(table2)
print("\n=== Chi-Square Test: SES vs Buying Frequency ===")
print("Chi-square:", round(chi2, 2), "| p-value:", round(p, 4))
print("Conclusion:", "✅ SES affects buying frequency" if p < 0.05 else "❌ No significant association")



# ============================
# 📌  Results Snapshot Table
# ============================
results = {
    "ANOVA: Age vs Fish Size": ["F=3.34", "p=0.0375", "✅ Significant"],
    "Chi-Square: Age Group vs Fish Type": ["χ²=19.97", "p=0.1731", "❌ Not Significant"],
    "Chi-Square: Education vs Reason": ["χ²=27.7", "p=0.0061", "✅ Significant"],
    "Chi-Square: Household vs Fish Size": ["χ²=44.16", "p=0.000", "✅ Significant"],
    "Chi-Square: SES vs Fish Size": ["χ²=78.28", "p=0.000", "✅ Significant"],
    "Chi-Square: SES vs Frequency": ["χ²=23.67", "p=0.0026", "✅ Significant"],
}

results_df = pd.DataFrame(results).T
results_df.columns = ["Statistic", "p-value", "Conclusion"]
print("\n=== Results Snapshot ===")
print(results_df)

