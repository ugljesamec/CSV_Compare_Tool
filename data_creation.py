import pandas as pd
import random

# Number of rows
rows = 100

names = ["John Smith", "Jane Doe", "Bob Stone", "Alice Green", "Tom Brown", "Emma White",
         "Oliver Black", "Sophia Gray", "Liam Blue", "Mia Silver", "Noah Gold", "Ava Rose",
         "Ethan Wood", "Isabella Hill", "Lucas Fox", "Amelia Reed", "Mason Lee", "Harper King",
         "Logan Hall", "Ella Adams"]

statuses = ["active", "inactive", "pending"]

# Generate base data
data_old = []
for i in range(1, rows + 1):
    name = random.choice(names)
    email = f"{name.split()[0].lower()}{i}@example.com"
    balance = round(random.uniform(50, 1000), 2)
    status = random.choice(statuses)
    data_old.append([i, name, email, balance, status])

# Copy and create new version with ~33 differences
data_new = [row.copy() for row in data_old]
indices_to_change = random.sample(range(rows), 33)

for idx in indices_to_change:
    field_to_change = random.choice([1, 3, 4])  # name, balance, or status
    if field_to_change == 1:
        data_new[idx][1] = random.choice(names)
    elif field_to_change == 3:
        data_new[idx][3] = round(random.uniform(50, 1000), 2)
    elif field_to_change == 4:
        data_new[idx][4] = random.choice(statuses)

# Save to CSV
df_old = pd.DataFrame(data_old, columns=["id", "name", "email", "balance", "status"])
df_new = pd.DataFrame(data_new, columns=["id", "name", "email", "balance", "status"])

df_old.to_csv("data_old.csv", index=False)
df_new.to_csv("data_new.csv", index=False)

print("✅ Created: data_old.csv and data_new.csv (100 rows, ~33 differences)")
