import pandas as pd
import matplotlib.pyplot as plt

# Načtení vyčištěných dat
df = pd.read_csv('vystupy/vycistena_data.csv')

# 1. Srovnání období (Před pandemií 2019, Pandemie 2020-2021, Zotavení 2022-2025)
def prirad_obdobi(rok):
    if rok == 2019: return 'Před pandemií (2019)'
    elif rok in [2020, 2021]: return 'Pandemie (2020-2021)'
    else: return 'Zotavení (2022-2025)'

df['Období'] = df['Rok'].apply(prirad_obdobi)
# Průměrná návštěvnost všech památek v daném kraji a období
prumery_obdobi = df.groupby(['Období', 'Kraj'])['Návštěvnost'].mean().unstack()
prumery_obdobi = prumery_obdobi.reindex(['Před pandemií (2019)', 'Pandemie (2020-2021)', 'Zotavení (2022-2025)'])

fig, ax = plt.subplots(figsize=(10, 6))
prumery_obdobi.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'])
plt.title('Průměrná návštěvnost jedné památky v různých obdobích')
plt.ylabel('Průměrný počet návštěvníků')
plt.xlabel('Období')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('vystupy/srovnani_obdobi.png')
plt.close()

# 2. Koncentrace návštěvníků (Kumulativní podíl) za rok 2025
df_2025 = df[df['Rok'] == 2025].copy()
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for i, kraj in enumerate(['Jihomoravský kraj', 'Praha']):
    kraj_data = df_2025[df_2025['Kraj'] == kraj].sort_values('Návštěvnost', ascending=False)
    celkem_kraj = kraj_data['Návštěvnost'].sum()
    kraj_data['Kumulativní_podíl'] = kraj_data['Návštěvnost'].cumsum() / celkem_kraj * 100
    
    axes[i].plot(range(1, len(kraj_data) + 1), kraj_data['Kumulativní_podíl'], marker='o')
    axes[i].set_title(f'Koncentrace návštěvníků - {kraj} (2025)')
    axes[i].set_xlabel('Pořadí památky (od nejnavštěvovanější)')
    axes[i].set_ylabel('Kumulativní podíl návštěvnosti (%)')
    axes[i].grid(True)
    axes[i].axhline(80, color='r', linestyle='--', label='80 % celkové návštěvnosti')
    axes[i].legend()

plt.tight_layout()
plt.savefig('vystupy/koncentrace_navstevniku.png')
plt.close()

print("Zbývající grafy byly úspěšně vygenerovány.")