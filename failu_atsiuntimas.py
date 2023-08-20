import os
import requests
import pandas as pd
import time

# Funkcija, kuri atlieka HTTP GET užklausą į nurodytą URL adresą su bandymais ir vėlinimais
def bandyti_uzklausa_su_perbandymais(url, maksimalus_perbandymai=20, laiko_miegas=2):
    perbandymai = 0
    while perbandymai < maksimalus_perbandymai:
        try:
            atsakas = requests.get(url)
            if atsakas.status_code == 200:
                return atsakas.json()
            else:
                print(f"Nepavyko gauti duomenų iš {url}, būsena: {atsakas.status_code}")
        except requests.exceptions.Timeout:
            print(f"Pradelstas laikas užklausai {url}, bandome dar kartą...")
        except requests.exceptions.RequestException as e:
            print(f"Klaida užklausai {url}: {e}")

        perbandymai += 1
        time.sleep(laiko_miegas)

    raise Exception(f"Nepavyko gauti duomenų iš {url} po {maksimalus_perbandymai} bandymų.")

# Funkcija, kuri nuskaito meteorologinius duomenis iš API ir juos išsaugo į CSV failus
def nuskaityti_ir_issaugoti_duomenis(pradzios_data, pabaigos_data):
    bazinis_adresas = "https://api.meteo.lt/v1/stations/panevezio-ams/observations/"
    datos_formatas = "%Y-%m-%d"
    menesio_intervalas = pd.DateOffset(months=1)
    vėlinimas_tarp_zingsniu = 2  # Vėlinimas tarp užklausų (sekundėmis)

    # Konvertuojamos pradžios ir pabaigos datos į Pandas datetime formatą
    pradzios_data = pd.to_datetime(pradzios_data, format=datos_formatas)
    pabaigos_data = pd.to_datetime(pabaigos_data, format=datos_formatas)

    esama_data = pradzios_data
    # Ciklas, einantis per kiekvieną mėnesį tarp pradinės datos ir pabaigos datos
    while esama_data <= pabaigos_data:
        pabaigos_menesio_data = esama_data + menesio_intervalas - pd.Timedelta(days=1)
        if pabaigos_menesio_data > pabaigos_data:
            pabaigos_menesio_data = pabaigos_data

        menesio_pavadinimas = esama_data.strftime('%Y-%m')
        menesio_failas = f"data/meteo/miestai/nesujungti/panevezys/meteo_{menesio_pavadinimas}.csv"

        # Patikrinama ar failas jau egzistuoja ir ar reikia jį kurti
        if not os.path.exists(menesio_failas) or (
                esama_data.month == pd.to_datetime('today').month and esama_data.year == pd.to_datetime('today').year):
            # Sukuriamas naujas CSV failas ir jame talpinami meteorologiniai duomenys
            print(
                f"Skaičiuojami duomenys už {esama_data.strftime(datos_formatas)} iki {pabaigos_menesio_data.strftime(datos_formatas)}")

            visi_duomenys = []
            esama_menesio_data = esama_data
            while esama_menesio_data <= pabaigos_menesio_data:
                uzklausos_adresas = f"{bazinis_adresas}{esama_menesio_data.strftime(datos_formatas)}"
                duomenys = bandyti_uzklausa_su_perbandymais(uzklausos_adresas)

                if duomenys is not None:
                    observacijos = duomenys.get("observations")
                    if observacijos:
                        visi_duomenys.extend(observacijos)
                    else:
                        # Jei informacijos nėra, pridedam eilutę su null reikšmėmis
                        visi_duomenys.append({key: None for key in duomenys["station"].keys()})

                esama_menesio_data += pd.Timedelta(days=1)
                time.sleep(vėlinimas_tarp_zingsniu)

            df = pd.DataFrame(visi_duomenys)
            if os.path.exists(menesio_failas):
                # Papildomos naujos datos ir atnaujinami esami duomenys
                senas_df = pd.read_csv(menesio_failas)
                df_esami = pd.DataFrame(senas_df, index=pd.to_datetime(senas_df['observationTimeUtc']))
                # Sukuriam naujų duomenų DataFrame su naujais datos laukais
                df_nauji = pd.DataFrame(index=pd.date_range(start=esama_data, end=pabaigos_menesio_data, freq='H'))
                # Sukonvertuojam datetime indeksą į stulpelį 'observationTimeUtc'
                df_nauji['observationTimeUtc'] = df_nauji.index.strftime(datos_formatas + " %H:%M:%S")
                # Sujungiam naujus ir esamus duomenis
                df_kombinuotas = pd.concat([df_nauji, df_esami], axis=1)
                # Išsaugom DataFrame į CSV failą
                df_kombinuotas.to_csv(menesio_failas, index=False)
                print(f"Duomenys papildyti ir išsaugoti faile {menesio_failas}")
            else:
                # Naujų duomenų DataFrame sukurimas ir išsaugojimas
                df.to_csv(menesio_failas, index=False)
                print(f"Duomenys išsaugoti faile {menesio_failas}")
        else:
            # Jei failas jau egzistuoja ir nereikia jo kurti, pranešama apie tai
            print(f"Failas {menesio_failas} jau egzistuoja, jo nekuriame")

        esama_data += menesio_intervalas

# Pavyzdys, kaip naudoti funkciją:
pradzios_data = "2023-08-01"
pabaigos_data = "2023-08-04"
nuskaityti_ir_issaugoti_duomenis(pradzios_data, pabaigos_data)
