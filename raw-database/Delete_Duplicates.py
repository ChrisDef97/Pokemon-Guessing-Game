import pandas as pd

# Load your CSV file
df = pd.read_csv('Pokedex_Database.csv')

# Drop duplicates based on 'Pokedex_Number' column, keeping only the first occurrence
df = df.drop_duplicates(subset='No', keep='first')

# Save the updated CSV without duplicates
df.to_csv('Pokedex_Database_NoDuplicates.csv', index=False)
