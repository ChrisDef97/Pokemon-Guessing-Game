import pandas as pd

# Load your CSV file
df = pd.read_csv('Pokedex_Ver_SV2.csv')

# Drop the columns you want to remove (replace 'column_name' with actual column names)
df = df.drop(columns=['Branch_Code','Original_Name','Height','Weight','Ability1','Ability2','Ability_Hidden','Color','Gender_Male','Gender_Female','Gender_Unknown','Egg_Steps','Egg_Group1','Egg_Group2','Get_Rate','Base_Experience','Experience_Type','Mega_Evolution_Flag','Region_Form','HP','Attack','Defense','SP_Attack','SP_Defense','Speed','Total','E_HP','E_Attack','E_Defense','E_SP_Attack','E_SP_Defense','E_Speed'])

# Save the updated CSV
df.to_csv('Pokedex_Database.csv', index=False)
