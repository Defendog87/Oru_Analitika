import os
import pandas as pd
import glob
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# Nuskaityti duomenis iš failo su nurodytu kodavimu ir priskirti stulpelių pavadinimus
visi_miestai = 'data/meteo/miestai/sujungti/visi_miestai.csv'
stulpeliu_pavadinimai = ['Miestas', 'Stebėjimų laikas', 'Oro temp.', 'Junt. temp', 'Vėjo greitis', 'Vėjo gūsis', 'Vėjo kryptis', 'Debesuotumas', 'Slėgis', 'Santykinis oro drėgnis', 'Kritulių kiekis', 'Orų sąlygos']
df = pd.read_csv(visi_miestai, encoding='utf-8', names=stulpeliu_pavadinimai, header=0)

# Konvertuoti 'Stebėjimų laikas' stulpelį į datetimo tipą su tinkamu formatu
df['Stebėjimų laikas'] = pd.to_datetime(df['Stebėjimų laikas'], format='%Y-%m-%d %H:%M:%S', errors='coerce')


# Funkcija, kuri nustato, ar tai diena, ar naktis pagal stebėjimo laiką
def day_or_night(row):
    if pd.notna(row['Stebėjimų laikas']):  # Patikrinti, ar 'Stebėjimų laikas' nėra NaT (Ne laikas)
        hour = row['Stebėjimų laikas'].hour
        if 6 <= hour < 18:
            return 'Diena'
    return 'Naktis'


df.dropna(inplace=True)
# Sukurti naują stulpelį 'Paros laikas'
df['Paros laikas'] = df.apply(day_or_night, axis=1)

# Prideda naujus stulpelius ir konvertuoti stulpelius į int tipą
df['Metai'] = df['Stebėjimų laikas'].dt.year.astype(int)
df['Ketvirtis'] = df['Stebėjimų laikas'].dt.quarter.astype(int)
df['Mėnesis'] = df['Stebėjimų laikas'].dt.month.astype(int)
df['Diena'] = df['Stebėjimų laikas'].dt.month.astype(int)

# data_rugpjucio_2022 = df[(df['Metai'] == 2022) & (df['Mėnesis'] == 8)]
# print(data_rugpjucio_2022[['Stebėjimų laikas', 'Oro temp.']])

while True:
    print('Sveiki atvykę į meteorologinių duomenų stebėjimo programą: ')
    print('pasirinkite norima operacija _>')
    print("1. Lietuvos didmiesčių klimato kaitos ypatybės: ")
    print("2. Vidutinės metinės temperatūros kaitos grafikas: ")
    print("3. Vidutinės metinės temperatūros kaitos grafikas (Miestai): ")
    print("4. Kritulių kiekis per stebėjimo laikotarpį: ")
    print("5. Vidutinė oro temperatūra Lietuvoje: ")
    print("6. Ketvirčių nuokrypiai nuo standartinės klimato normos: ")
    print("7. Užbaigti operacijas: ")
    operacija = int(input('Iveskite operacijos numeri_>'))
    if operacija == 1:

        # Grupuojame duomenis pagal 'Miestas' ir skaičiuojame vidutinę metinę temperatūrą
        vidurkis_metu_temperatura = df.groupby(['Miestas'])['Oro temp.'].mean().reset_index()
        # Suapvalinam vidurkį iki 2 skaičių po kablelio
        vidurkis_metu_temperatura = round(vidurkis_metu_temperatura, 2)
        # Konvertuojame vidurkio stulpelį į tekstą ir pridedame °C simbolį
        vidurkis_metu_temperatura['Oro temp.'] = vidurkis_metu_temperatura['Oro temp.'].astype(str) + ' °C'
        # Pervadiname stulpelį į 'Vidutinė metų temperatūra'
        vidurkis_metu_temperatura.rename(columns={'Oro temp.': 'Vidutinė metų temperatūra'}, inplace=True)

        vidutinis_vejo_greitis = df.groupby(['Miestas'])['Vėjo greitis'].mean().reset_index()
        vidutinis_vejo_greitis = round(vidutinis_vejo_greitis, 2)
        vidutinis_vejo_greitis['Vėjo greitis'] = vidutinis_vejo_greitis['Vėjo greitis'].astype(str) + ' m/s'
        vidutinis_vejo_greitis.rename(columns={'Vėjo greitis': 'Vidutinis vėjo greitis'}, inplace=True)

        vidutinis_vejo_gusis = df.groupby(['Miestas'])['Vėjo gūsis'].mean().reset_index()
        vidutinis_vejo_gusis = round(vidutinis_vejo_gusis, 2)
        vidutinis_vejo_gusis['Vėjo gūsis'] = vidutinis_vejo_gusis['Vėjo gūsis'].astype(str) + ' m/s'
        vidutinis_vejo_gusis.rename(columns={'Vėjo gūsis': 'Vidutiniai vėjo gūsiai'}, inplace=True)

        didziausia_temperatura = df.groupby(['Miestas'])['Oro temp.'].idxmax()
        didziausia_temperatura = df.loc[didziausia_temperatura, ['Miestas', 'Oro temp.']]
        didziausia_temperatura['Oro temp.'] = didziausia_temperatura['Oro temp.'].astype(str) + '°C'
        didziausia_temperatura.rename(columns={'Oro temp.': 'Aukščiausia temperatūra'}, inplace=True)

        maziausia_temperatura = df.groupby(['Miestas'])['Oro temp.'].idxmin()
        maziausia_temperatura = df.loc[maziausia_temperatura, ['Miestas', 'Oro temp.']]
        maziausia_temperatura['Oro temp.'] = maziausia_temperatura['Oro temp.'].astype(str) + '°C'
        maziausia_temperatura.rename(columns={'Oro temp.': 'Žemiausia temperatūra'}, inplace=True)

        didziausias_vejo_gusis = df.groupby(['Miestas'])['Vėjo gūsis'].idxmax()
        didziausias_vejo_gusis = df.loc[didziausias_vejo_gusis, ['Miestas', 'Vėjo gūsis']]
        didziausias_vejo_gusis['Vėjo gūsis'] = didziausias_vejo_gusis['Vėjo gūsis'].astype(str) + ' m/s'
        didziausias_vejo_gusis.rename(columns={'Vėjo gūsis': 'Didžiausias vėjo gūsis'}, inplace=True)

        didziausias_vejo_greitis = df.groupby(['Miestas'])['Vėjo greitis'].idxmax()
        didziausias_vejo_greitis = df.loc[didziausias_vejo_greitis, ['Miestas', 'Vėjo greitis']]
        didziausias_vejo_greitis['Vėjo greitis'] = didziausias_vejo_greitis['Vėjo greitis'].astype(str) + ' m/s'
        didziausias_vejo_greitis.rename(columns={'Vėjo greitis': 'Didžiausias vėjo greitis'}, inplace=True)

        krituliu_kiekis_per_metus = df.groupby(['Metai', 'Miestas'])['Kritulių kiekis'].sum().reset_index()
        krituliu_kiekis_per_metus = krituliu_kiekis_per_metus.groupby('Miestas')['Kritulių kiekis'].mean().reset_index()
        krituliu_kiekis_per_metus['Kritulių kiekis'] = krituliu_kiekis_per_metus['Kritulių kiekis'].round(2).astype(str) + ' mm'
        krituliu_kiekis_per_metus.rename(columns={'Kritulių kiekis': 'Vidutinis kritulių kiekis per metus'},inplace=True)

        sauletos_dienos = df.loc[(df['Debesuotumas'] < 20) & (df['Paros laikas'] == 'Diena')]
        sauletos_dienos = sauletos_dienos.groupby(['Metai', 'Miestas'])['Miestas'].count()
        sauletos_dienos = sauletos_dienos.reset_index(name='Saulėtos dienos')
        sauletos_dienos = sauletos_dienos.groupby('Miestas')['Saulėtos dienos'].mean()
        sauletos_dienos = sauletos_dienos.astype(int).astype(str) + ' valandos'
        sauletos_dienos = sauletos_dienos.to_frame().rename(columns={'Saulėtos dienos': 'Saulėtos valandos'})

        # Apjungiam skirtingus duomenis į bendrą lentelę pagal 'Miestas'
        statistiniai_duomenys = pd.merge(vidurkis_metu_temperatura, maziausia_temperatura, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, didziausia_temperatura, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, didziausias_vejo_gusis, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, didziausias_vejo_greitis, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, vidutinis_vejo_greitis, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, vidutinis_vejo_gusis, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, krituliu_kiekis_per_metus, on='Miestas')
        statistiniai_duomenys = pd.merge(statistiniai_duomenys, sauletos_dienos, on='Miestas')

        # Susikuriame lentelę 'statistiniai_duomenys_lentele' iš 'statistiniai_duomenys' duomenų naudodami pivot_table metodą
        statistiniai_duomenys_lentele = statistiniai_duomenys.pivot_table(index=None, columns='Miestas', aggfunc='first')
        # Naudojame 'tabulate' biblioteką, kad konvertuotume 'statistiniai_duomenys_lentele' į tekstinį formatą su stulpelių antraštėmis 'keys' ir lentelės formatu 'pipe'
        lenteles_formatas = tabulate(statistiniai_duomenys_lentele, headers='keys', tablefmt='pipe')

        print(lenteles_formatas)
        print('''
        ''')

    elif operacija == 2:
        # Apskaičiuojame Vidutinę metinę temperatūrą kiekvienais metais
        vidutine_temperatura_per_metai = df.groupby(['Metai'])['Oro temp.'].mean()

        # Apskaičiuojame tiesės koeficientus ir atitinkamus reikšmes trendo linijai
        koeficientai = np.polyfit(vidutine_temperatura_per_metai.index, vidutine_temperatura_per_metai.values, 1)
        trendo_linija = np.polyval(koeficientai, vidutine_temperatura_per_metai.index)

        # Nubraižome diagramą su trendo linija
        plt.figure(figsize=(10, 6))
        plt.plot(vidutine_temperatura_per_metai.index, vidutine_temperatura_per_metai.values, marker='o', linestyle='-',color='b', label='Vidutinė temperatūra')
        plt.plot(vidutine_temperatura_per_metai.index, trendo_linija, linestyle='--', color='r', label='Trendo linija')
        plt.xlabel('Metai')
        plt.ylabel('Vidutinė temperatūra (°C)')
        plt.title('Vidutinės metinės temperatūros kaita nuo 2014 iki 2022')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif operacija == 3:
        # Filtruojame duomenis pagal miestus
        df_kaunas = df[df['Miestas'] == 'Kaunas']
        df_vilnius = df[df['Miestas'] == 'Vilnius']
        df_klaipeda = df[df['Miestas'] == 'Klaipeda']
        df_panevezys = df[df['Miestas'] == 'Panevezys']

        # Apskaičiuojame Vidutinę metinę temperatūrą kiekvienais metais miestams
        vidutine_temperatura_kaunas = df_kaunas.groupby(['Metai'])['Oro temp.'].mean()
        vidutine_temperatura_vilnius = df_vilnius.groupby(['Metai'])['Oro temp.'].mean()
        vidutine_temperatura_klaipeda = df_klaipeda.groupby(['Metai'])['Oro temp.'].mean()
        vidutine_temperatura_panevezys = df_panevezys.groupby(['Metai'])['Oro temp.'].mean()

        # Skaičiuojame tendencijų linijas (trendo linijas) naudodami polinominę aproksimaciją
        koeficientai_kaunas = np.polyfit(vidutine_temperatura_kaunas.index, vidutine_temperatura_kaunas.values, 1)
        koeficientai_vilnius = np.polyfit(vidutine_temperatura_vilnius.index, vidutine_temperatura_vilnius.values, 1)
        koeficientai_klaipeda = np.polyfit(vidutine_temperatura_klaipeda.index, vidutine_temperatura_klaipeda.values, 1)
        koeficientai_panevezys = np.polyfit(vidutine_temperatura_panevezys.index, vidutine_temperatura_panevezys.values, 1)

        # Kadangi norime tiesinės tendencijos linijos, naudojame np.polyfit funkciją su laipsniu 1 (t.y. tiesinė polinominė funkcija)
        trendo_linija_kaunas = np.polyval(koeficientai_kaunas, vidutine_temperatura_kaunas.index)
        trendo_linija_vilnius = np.polyval(koeficientai_vilnius, vidutine_temperatura_vilnius.index)
        trendo_linija_klaipeda = np.polyval(koeficientai_klaipeda, vidutine_temperatura_klaipeda.index)
        trendo_linija_panevezys = np.polyval(koeficientai_panevezys, vidutine_temperatura_panevezys.index)

        # Sukuriame 2x2 dydžio vaizdo langą, kad matytume 4 skirtingus grafikus
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        # Pavaizduojame vidutinės metinės temperatūros tendenciją kiekvienam miestui
        # Kaunas
        axs[0, 0].plot(vidutine_temperatura_kaunas.index, vidutine_temperatura_kaunas.values, marker='o', linestyle='-',color='#4a4e4d', label='Kaunas')
        axs[0, 0].plot(vidutine_temperatura_kaunas.index, trendo_linija_kaunas, linestyle='--', color='r', label='Trendo linija')
        axs[0, 0].set_xlabel('Metai')
        axs[0, 0].set_ylabel('Vidutinė temperatūra (°C)')
        axs[0, 0].set_title('Kaunas')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # Vilnius
        axs[0, 1].plot(vidutine_temperatura_vilnius.index, vidutine_temperatura_vilnius.values, marker='o', linestyle='-', color='#ff6f69', label='Vilnius')
        axs[0, 1].plot(vidutine_temperatura_vilnius.index, trendo_linija_vilnius, linestyle='--', color='r', label='Trendo linija')
        axs[0, 1].set_xlabel('Metai')
        axs[0, 1].set_ylabel('Vidutinė temperatūra (°C)')
        axs[0, 1].set_title('Vilnius')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        # Klaipeda
        axs[1, 0].plot(vidutine_temperatura_klaipeda.index, vidutine_temperatura_klaipeda.values, marker='o', linestyle='-', color='#009688', label='Klaipėda')
        axs[1, 0].plot(vidutine_temperatura_klaipeda.index, trendo_linija_klaipeda, linestyle='--', color='r', label='Trendo linija')
        axs[1, 0].set_xlabel('Metai')
        axs[1, 0].set_ylabel('Vidutinė temperatūra (°C)')
        axs[1, 0].set_title('Klaipėda')
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        # Panevezys
        axs[1, 1].plot(vidutine_temperatura_panevezys.index, vidutine_temperatura_panevezys.values, marker='o', linestyle='-', color='purple', label='Panevežys')
        axs[1, 1].plot(vidutine_temperatura_panevezys.index, trendo_linija_panevezys, linestyle='--', color='r', label='Trendo linija')
        axs[1, 1].set_xlabel('Metai')
        axs[1, 1].set_ylabel('Vidutinė temperatūra (°C)')
        axs[1, 1].set_title('Panevežys')
        axs[1, 1].legend()
        axs[1, 1].grid(True)

        # Sureguliuojame vaizdo langą, kad pavadinimai neatkristų
        plt.tight_layout()
        # Pridedame pavadinimą virš vaizdo lango
        plt.subplots_adjust(top=0.88)  # Sureguliuojame viršutinę kraštinę, kad atsirastų vietos pavadinimui
        fig.suptitle('Vidutinės metinės temperatūros kaita skirtinguose miestuose nuo 2014 iki 2022', fontsize=16)


        plt.show()

    elif operacija == 4:

        # Grupuojame duomenis pagal metus ir skaičiuojame bendrą kritulių kiekį ir miestų skaičių kiekvienais metais
        krituliu_kiekis_pagal_metus = df.groupby('Metai')['Kritulių kiekis'].sum()
        miestu_skaicius_pagal_metus = df.groupby('Metai')['Miestas'].nunique()

        # Skaičiuojame vidutinį kritulių kiekį
        vidutinis_krituliu_kiekis = krituliu_kiekis_pagal_metus / miestu_skaicius_pagal_metus

        # Sukuriame DataFrame su stulpeliais 'Metai' ir 'Vidutinis kritulių kiekis'
        krituliu_df = pd.DataFrame({'Metai': vidutinis_krituliu_kiekis.index, 'Vidutinis kritulių kiekis': vidutinis_krituliu_kiekis.values})

        # Atliekame linijinę regresiją, kad gautume trendo liniją
        X = sm.add_constant(krituliu_df['Metai'])  # Pridedame konstantos reikšmę interceptui
        y = krituliu_df['Vidutinis kritulių kiekis']

        modelis = sm.OLS(y, X).fit()
        trendo_linija = modelis.predict(X)

        # Braižome stulpelinę diagramą su trendo linija
        plt.figure(figsize=(10, 6))
        plt.bar(krituliu_df['Metai'], krituliu_df['Vidutinis kritulių kiekis'], label='Vidutinis kritulių kiekis (mm)', color='#4b86b4')
        plt.plot(krituliu_df['Metai'], trendo_linija, color='red', label='Trendo linija')
        plt.xlabel('Metai')
        plt.ylabel('Vidutinis kritulių kiekis')
        plt.title('Vidutinis kritulių kiekis per metus su trendo linija (vidutiniškai per miestus)')
        plt.legend()
        plt.xticks(krituliu_df['Metai'])
        plt.show()
    elif operacija == 5:

        # Sukuriame sąrašą su standartine klimato norma mėnesiams
        standartine_klimato_norma_menesis = [-2.9, -2.5, 0.9, 7.2, 12.5, 15.9, 18.3, 17.6, 12.8, 7.3, 2.6, -1.1]

        # Filtruojame duomenis nuo 2022 01 01 iki gruodžio 2022 12 31
        start_date_2022 = '2022-01-01'
        end_date_2022 = '2022-12-31'
        df_2022 = df[(df['Stebėjimų laikas'] >= start_date_2022) & (df['Stebėjimų laikas'] <= end_date_2022)]

        # Skaičiuojame vidutines mėnesines temperatūras 2022 metais
        vidutine_temperatura_2022 = df_2022.groupby(['Mėnesis'])['Oro temp.'].mean()

        # Filtruojame duomenis nuo sausio 2023 iki liepos 31, 2023
        start_date = '2023-01-01'
        end_date = '2023-07-31'
        df_2023 = df[(df['Stebėjimų laikas'] >= start_date) & (df['Stebėjimų laikas'] <= end_date)]

        # Skaičiuojame vidutines mėnesines temperatūras 2023 metais
        vidutine_temperatura_2023 = df_2023.groupby(['Mėnesis'])['Oro temp.'].mean()

        # Braižome diagramą
        plt.figure(figsize=(10, 6))

        # Įtraukiame vidutines temperatūras 2022 metais į diagramą
        plt.plot(vidutine_temperatura_2022.index, vidutine_temperatura_2022.values, marker='o', linestyle='-', color='purple', label='Vidutinė temperatūra (2022)')

        # Įtraukiame standartinę klimato normą į diagramą
        plt.plot(range(1, 13), standartine_klimato_norma_menesis, marker='.', linestyle='-', color='#fec8c1', label='Standartinė klimato norma')

        # Įtraukiame vidutines temperatūras 2023 metais į diagramą
        plt.plot(vidutine_temperatura_2023.index, vidutine_temperatura_2023.values, marker='o', linestyle='-', color='g', label='Vidutinė temperatūra (2023.01 - 2023.07)')
        plt.xlabel('Mėnesis')
        plt.ylabel('Temperatūra (°C)')
        plt.title('Vidutinė oro temperatūra Lietuvoje')
        plt.xticks(range(1, 13), ['Sausis', 'Vasaris', 'Kovas', 'Balandis', 'Gegužė', 'Birželis', 'Liepa', 'Rugpjūtis', 'Rugsėjis', 'Spalis', 'Lapkritis', 'Gruodis'], rotation=45)
        plt.grid(True)
        plt.legend()
        plt.show()
    elif operacija == 6:
        # Standartinės klimato normos kiekvienam ketvirtį
        standartine_klimato_norma_ketvirtis = [-1.50, 11.87, 16.23, 2.93]

        # Su grupavimu pagal metus ir ketvirtį suskaičiuojame vidutinę temperatūrą kiekvienam ketvirtį
        ketvircio_vidurkiai = df.groupby(['Metai', 'Ketvirtis'])['Oro temp.'].mean()

        # Sukuriame Seriją 'standard_climate_series' su 'Ketvirtis' indeksu, naudodami ketvirčių normas kaip reikšmes
        standartinė_klimato_norma_serija = pd.Series(standartine_klimato_norma_ketvirtis, index=range(1, 5))

        # Skaičiuojame ketvirčių nuokrypius nuo standartinių klimato normų
        ketvirčių_nuokrypiai = ketvircio_vidurkiai - standartinė_klimato_norma_serija.loc[ketvircio_vidurkiai.index.get_level_values('Ketvirtis')].values

        # Sukuriame stulpelinę diagramą su metais x ašyje ir nuokrypiais y ašyje
        # Stulpelinės diagramos stulpeliai atspindi ketvirčių nuokrypius, o spalvos atitinka ketvirčius
        ketvirčių_spalvos = ['#4B86B4', '#65C3BA', '#F9CAA7', '#FF6F69']

        # Braižome stulpelinę diagramą su ketvirčių nuokrypiais, naudodami skirtingas spalvas kiekvienam ketvirčiui
        plt.figure(figsize=(10, 6))
        ax = ketvirčių_nuokrypiai.plot(kind='bar', ax=plt.gca(), width=0.8, color=ketvirčių_spalvos)
        plt.xlabel('Metai')
        plt.ylabel('Ketvirčio nuokrypis nuo standartinės normos')
        plt.title('Ketvirčio oro temperatūros nuokrypiai nuo standartinės klimato normos')
        plt.grid(True)

        # Sukuriame legendos etiketes su ketvirčių informacija
        legend_labels = ['I ketvirtis', 'II ketvirtis', 'III ketvirtis', 'IV ketvirtis']

        # Sukuriame individualią legendą kiekvienam ketvirčiui
        legend_handles = []
        for i, quarter in enumerate(ketvirčių_nuokrypiai.index.get_level_values('Ketvirtis').unique()):
            legend_handles.append(plt.bar(0, 0, color=ketvirčių_spalvos[i], label=legend_labels[i]))

        # Pridedame individualią legendą į diagramą
        plt.legend(handles=legend_handles, title='Ketvirtis', bbox_to_anchor=(1.02, 1), loc='upper left')

        # Nustatome x ašies žymeklius, kiekvieną 4-ą metus, ir pritaikome x ašies žymeklių pavadinimus
        plt.xticks(range(0, len(ketvirčių_nuokrypiai), 4), ketvirčių_nuokrypiai.index.get_level_values('Metai')[::4])
        plt.tight_layout()
        plt.xticks(rotation=0)
        plt.show()

    elif operacija == 7:
        print('Operacijos pabaiga')
        break
    else:
        print('neteisingas pasirinkimas, bandykite dar karta')




