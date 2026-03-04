import datetime
import holidays
import streamlit as st


def data_prawomocnosci(data_doreczenia: datetime.date, typ_orzeczenia: str) -> datetime.date:

    OKRESY = {
        "wyrok": 30,
        "postanowienie": 7,
        "decyzja II instancji": 30,
        "decyzja II instancji - art. 138 § 2": 14,
        "decyzja I instancji": 14,
    }

    # Wyrok NSA – prawomocny w dniu wydania
    if typ_orzeczenia == "wyrok NSA":
        return data_doreczenia

    okres = OKRESY.get(typ_orzeczenia)
    if okres is None:
        raise ValueError("Nieznany typ orzeczenia")

    # 1️⃣ Ostatni dzień terminu (nie wliczamy dnia doręczenia)
    ostatni_dzien = data_doreczenia + datetime.timedelta(days=okres)

    polskie_swieto = holidays.Polish()

    # 2️⃣ Jeżeli ostatni dzień przypada w sobotę, niedzielę lub święto → przesuwamy na dzień roboczy
    while ostatni_dzien.weekday() >= 5 or ostatni_dzien in polskie_swieto:
        ostatni_dzien += datetime.timedelta(days=1)

    # 3️⃣ Prawomocność = dzień po upływie terminu
    data_prawomocnosci = ostatni_dzien + datetime.timedelta(days=1)

    return data_prawomocnosci


# ------------------ STREAMLIT UI ------------------

st.title("Obliczanie prawomocności orzeczeń")

typ_orzeczenia = st.selectbox(
    "Typ orzeczenia",
    [
        "wyrok",
        "postanowienie",
        "decyzja II instancji",
        "decyzja II instancji - art. 138 § 2",
        "decyzja I instancji",
        "wyrok NSA",
    ],
)

data_doreczenia = st.date_input(
    "Podaj datę doręczenia / wydania (dla wyroku NSA)",
    value=datetime.date(2026, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date(2100, 12, 31),
)

st.subheader("Orzeczenie prawomocne od:")

data_wynik = data_prawomocnosci(data_doreczenia, typ_orzeczenia)

st.markdown(
    f"<span style='font-size: 20px;'>Data prawomocności orzeczenia: </span>"
    f"<span style='font-size: 30px; color: green; font-weight: bold;'>{data_wynik}</span>",
    unsafe_allow_html=True,
)

st.caption("Zaprojektował: Michał Czerniak - Wojewódzki Sąd Administracyjny w Poznaniu")
