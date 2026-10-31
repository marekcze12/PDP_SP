import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Načtení vyčištěných dat
df = pd.read_csv('vystupy/vycistena_data.csv')

# 1. Výpočet základních statistik podle krajů
stats = df.groupby('Kraj')['Návštěvnost'].describe()
stats['medián'] = df.groupby('Kraj')['Návštěvnost'].median()
stats.to_csv('vystupy/zakladni_statistiky.csv')

# 2. Meziroční procentuální změny návštěvnosti
agregace = df.groupby(['Rok', 'Kraj'])['Návštěvnost'].sum().unstack()
pct_zmeny = agregace.pct_change() * 100

plt.figure(figsize=(10, 6))
pct_zmeny.plot(kind='bar', color=['#1f77b4', '#ff7f0e'])
plt.title('Meziroční procentuální změna návštěvnosti (2019–2025)')
plt.ylabel('Změna v %')
plt.xlabel('Rok')
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('vystupy/mezirocni_zmeny.png')
plt.close()

# 3. Top 10 nejnavštěvovanějších památek za rok 2025
df_2025 = df[df['Rok'] == 2025]

for kraj in df['Kraj'].unique():
    top10 = df_2025[df_2025['Kraj'] == kraj].nlargest(10, 'Návštěvnost')
    
    plt.figure(figsize=(10, 6))
    plt.barh(top10['Název'], top10['Návštěvnost'], color='skyblue')
    plt.gca().invert_yaxis()  # Nejnavštěvovanější nahoře
    plt.title(f'Top 10 památek v roce 2025 - {kraj}')
    plt.xlabel('Počet návštěvníků')
    plt.tight_layout()
    plt.savefig(f'vystupy/top10_{kraj}.png')
    plt.close()

print("Analýza dokončena. Nové tabulky a grafy najdeš ve složce 'vystupy'.")