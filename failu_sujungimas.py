import os
import pandas as pd
import glob

def sujungti_failus_ir_issaugoti(vardas_sablonas, bendras_failas, miesto_pavadinimas):
    # Nustatome kelią iki failų skaitymo vietos
    skaitymo_kelias = "data/meteo/miestai/nesujungti/vilnius"
    # Nustatome kelią, kurioje išsaugosime sujungtą failą
    issaugojimo_kelias = "data/meteo/miestai/sujungti"
    # Gauname visus failus, atitinkančius nurodytą šabloną
    visi_failai = glob.glob(os.path.join(skaitymo_kelias, vardas_sablonas))
    duomenu_rameles = []
    antraste_prideta = False

    for failas in visi_failai:
        # Nuskaitome duomenis iš CSV failo
        duomenys = pd.read_csv(failas)

        # Pasirenkame tik reikiamus stulpelius
        duomenys = duomenys[['observationTimeUtc', 'airTemperature', 'feelsLikeTemperature', 'windSpeed', 'windGust', 'windDirection', 'cloudCover', 'seaLevelPressure', 'relativeHumidity', 'precipitation', 'conditionCode']]

        # Pridedame stulpelį 'Miestas' su pasirinktu pavadinimu į pradžią
        duomenys.insert(0, 'Miestas', miesto_pavadinimas)

        if not antraste_prideta:
            duomenu_rameles.append(duomenys)
            antraste_prideta = True
        else:
            duomenu_rameles.append(duomenys[1:])

    # Sujungiame duomenų rėmelius
    bendra_ramele = pd.concat(duomenu_rameles, ignore_index=True)

    # Užpildome trūkstamas reikšmes "null" reikšmėmis
    bendra_ramele = bendra_ramele.fillna("null")

    if not os.path.exists(issaugojimo_kelias):
        os.makedirs(issaugojimo_kelias)

    # Išsaugome duomenų rėmelį į CSV failą
    bendra_ramele.to_csv(os.path.join(issaugojimo_kelias, bendras_failas), index=False)
    print(f"Bendra duomenų rėmelė sujungta ir išsaugota {os.path.join(issaugojimo_kelias, bendras_failas)}")


while True:
    print('pasirinkite norima operacija _>')
    print("1. Sukurti miesto failą ")
    print("2. Sukurti bendra failą ")
    print("3. Užbaigti operacijas: ")
    operacija = int(input('Iveskite operacijos numeri_>'))
    if operacija == 1:

        # Pavyzdys, kaip naudoti funkciją:
        vardas_sablonas = "meteo_*.csv"
        bendras_failas = "vilnius_meteo.csv"
        miesto_pavadinimas = "Vilnius"
        sujungti_failus_ir_issaugoti(vardas_sablonas, bendras_failas, miesto_pavadinimas)

    elif operacija == 2:

        # Nustatome direktoriją, kurioje yra miestų meteo failai
        data_directory = "data/meteo/miestai/sujungti"

        # Sudarome sąrašą su visais failais, kuriuos norime sujungti
        file_list = [file for file in os.listdir(data_directory) if file.endswith("_meteo.csv")]

        # Sukuriame tuščią DataFrame, į kurį sujungsime duomenis
        sujungti_df = pd.DataFrame()

        # Sujungiame duomenis iš visų failų į vieną DataFrame
        for file in file_list:
            failo_kelias = os.path.join(data_directory, file)
            df = pd.read_csv(failo_kelias)
            sujungti_df = pd.concat([sujungti_df, df], ignore_index=True)

        # Saugome sujungtus duomenis į naują CSV failą
        isvesties_failas = os.path.join(data_directory, "visi_miestai.csv")
        sujungti_df.to_csv(isvesties_failas, index=False)

        print("Duomenys buvo sėkmingai sujungti į 'visi_miestai.csv' failą.")

    elif operacija == 3:
        print('Operacijos pabaiga')
        break
    else:
        print('neteisingas pasirinkimas, bandykite dar karta')