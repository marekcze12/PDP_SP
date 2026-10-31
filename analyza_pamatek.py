import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Vytvoření výstupní složky pro data a grafy
os.makedirs('vystupy', exist_ok=True)

def nacti_a_vycisti(soubor, kraj, pocet_preskocenych_radku):
    # Načtení dat s přeskočením úvodních textových řádků
    df = pd.read_excel(soubor, skiprows=pocet_preskocenych_radku)
    
    # Odstranění řádků bez názvu památky
    df = df.dropna(subset=['Název'])
    
    # Odfiltrování souhrnných řádků za okresy, aby nedošlo k duplikaci dat
    df = df[~df['Název'].str.contains('Celkem Okres|Okres ', case=False, na=False)]
    
    # Nalezení sloupců obsahujících návštěvnost
    roky_sloupce = [col for col in df.columns if 'návštěvnost' in col.lower()]
    
    # Nahrazení chybějících hodnot (tečky, křížky) za NaN a převod na číselný typ
    for col in roky_sloupce:
        df[col] = df[col].replace(['.', 'x'], np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Převod dat ze širokého do dlouhého relačního formátu
    df_long = pd.melt(
        df, 
        id_vars=['Název', 'webové stránky'], 
        value_vars=roky_sloupce, 
        var_name='Rok_str', 
        value_name='Návštěvnost'
    )
    
    # Extrakce roku do samostatného sloupce
    df_long['Rok'] = df_long['Rok_str'].str.extract(r'(\d{4})').astype(int)
    
    # Odstranění dočasného sloupce a záznamů s prázdnou návštěvností
    df_long = df_long.dropna(subset=['Návštěvnost']).drop(columns=['Rok_str'])
    df_long['Kraj'] = kraj
    
    return df_long

# Načtení obou tabulek se správným počtem přeskočených řádků
df_jmk = nacti_a_vycisti('JM_2019-25.xlsx', 'Jihomoravský kraj', 6)
df_pha = nacti_a_vycisti('PR_2019-25.xlsx', 'Praha', 5)

# Sloučení do jednoho centrálního datasetu
df_all = pd.concat([df_jmk, df_pha], ignore_index=True)

# Export vyčištěných dat do CSV s českým kódováním
df_all.to_csv('vystupy/vycistena_data.csv', index=False, encoding='utf-8-sig')

# Výpočet celkové návštěvnosti podle krajů a roků
agregace = df_all.groupby(['Rok', 'Kraj'])['Návštěvnost'].sum().unstack()

# Vykreslení prvního srovnávacího grafu
agregace.plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Vývoj celkové návštěvnosti památek (2019–2025)')
plt.ylabel('Počet návštěvníků')
plt.xlabel('Rok')
plt.grid(True)
plt.tight_layout()

# Uložení grafu na disk
plt.savefig('vystupy/vyvoj_navstevnosti.png')
print("Hotovo. Čistá data a graf jsou uloženy ve složce 'vystupy'.")