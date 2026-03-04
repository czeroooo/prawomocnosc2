import datetime
import holidays
import streamlit as st

def data_prawomocnosci(data_doreczenia, typ_orzeczenia):
  data_doreczenia = datetime.date(data_doreczenia.year, data_doreczenia.month, data_doreczenia.day)
  if typ_orzeczenia == 'wyrok':
      okres_prawomocnosci = 30
  elif typ_orzeczenia == 'postanowienie':
      okres_prawomocnosci = 7
  elif typ_orzeczenia == 'decyzja II instancji':
      okres_prawomocnosci = 30
  elif typ_orzeczenia == 'decyzja II instancji - art. 138 § 2':
      okres_prawomocnosci = 14
  elif typ_orzeczenia == 'decyzja I instancji':
      okres_prawomocnosci = 14
  elif typ_orzeczenia == 'wyrok NSA':
      okres_prawomocnosci = -1
  else:
      raise ValueError('Nieznany typ orzeczenia')
  data_prawomocnosci = data_doreczenia + datetime.timedelta(days=okres_prawomocnosci +1)

  # pobranie listy dat świątecznych w Polsce
  polskie_swieto = holidays.Polish()

while True:
# 1. wyliczamy ostatni dzień terminu (nie wliczamy dnia doręczenia)
ostatni_dzien = data_doreczenia + datetime.timedelta(days=okres_prawomocnosci)

polskie_swieto = holidays.Polish()

# 2. jeżeli ostatni dzień wypada w dzień wolny → przesuwamy na roboczy
while ostatni_dzien.weekday() >= 5 or ostatni_dzien in polskie_swieto:
    ostatni_dzien += datetime.timedelta(days=1)

# 3. prawomocność dzień po upływie terminu
data_prawomocnosci = ostatni_dzien + datetime.timedelta(days=1)

return data_prawomocnosci

st.title("Obliczanie prawomocności orzeczeń")
typ_orzeczenia = st.selectbox("Typ orzeczenia", ["wyrok", "postanowienie", "decyzja II instancji", "decyzja II instancji - art. 138 § 2", "decyzja I instancji", "wyrok NSA"])
data_doreczenia = st.date_input("Podaj datę doręczenia", value=datetime.date(2026, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100,12,31))
st.write("Orzeczenie prawomocne od:")
data_prawomocnosci = data_prawomocnosci(data_doreczenia, typ_orzeczenia)

st.markdown(f"<span style='font-size: 20px; color: white;'>Data prawomocności orzeczenia: </span><span style='font-size: 30px; color: green;'>{data_prawomocnosci}</span>", unsafe_allow_html=True)

st.caption('Zaprojektował: Michał Czerniak - Wojewódzki Sąd Administracyjny w Poznaniu')




















