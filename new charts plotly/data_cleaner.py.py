import pandas as pd

# Read Excel
df = pd.read_excel("email_datatobecleaned.xlsx")

def is_internal_only(recipient_str):
    if pd.isna(recipient_str):
        return False  # Keep empty recipient rows
    recipients = [r.strip().lower() for r in recipient_str.split(",") if r.strip()]
    if not recipients:
        return False
    # Check if all recipients contain @bajajal or @bajajge
    return all(('@bajajal' in r or '@bajajge' in r) for r in recipients)

# Filter out rows that are internal only
filtered_df = df[~df["Recipient"].apply(is_internal_only)]

# Save the result
filtered_df.to_excel("filteredemail_output.xlsx", index=False)

print(f"Original rows: {len(df)}")
print(f"Filtered rows: {len(filtered_df)}")
print("✅ Done! Saved as 'filtered_output.xlsx'")
