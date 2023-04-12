import datetime
import holidays
import streamlit as st

def data_prawomocnosci(dzien_doreczenia, miesiac_doreczenia, rok_doreczenia, okres_odwolawczy, typ_orzeczenia):
  data_doreczenia = datetime.date(rok_doreczenia, miesiac_doreczenia, dzien_doreczenia)
  if typ_orzeczenia == 'wyrok':
      okres_prawomocnosci = 30
  elif typ_orzeczenia == 'postanowienie':
      okres_prawomocnosci = 7
  elif typ_orzeczenia == 'decyzja':
      okres_prawomocnosci = 14
  else:
      raise ValueError('Nieznany typ orzeczenia')
  data_prawomocnosci = data_doreczenia + datetime.timedelta(days=okres_odwolawczy + okres_prawomocnosci)

  # pobranie listy dat świątecznych w Polsce
  polskie_swieto = holidays.Polish()

  while True:
      # sprawdzenie, czy data prawomocności przypada na dzień świąteczny lub dzień wolny od pracy
      if data_prawomocnosci.weekday() >= 5 or data_prawomocnosci in polskie_swieto:
          data_prawomocnosci += datetime.timedelta(days=1)
      else:
          break

  return data_prawomocnosci

st.title("Obliczanie daty prawomocności orzeczenia")

dzien_doreczenia = st.number_input("Podaj dzień doręczenia", value=1, min_value=1, max_value=31)
miesiac_doreczenia = st.number_input("Podaj miesiąc doręczenia", value=1, min_value=1, max_value=12)
rok_doreczenia = st.number_input("Podaj rok doręczenia", value=2022, min_value=1900, max_value=2100)

typ_orzeczenia = st.selectbox("Typ orzeczenia", ["wyrok", "postanowienie", "decyzja"])

data_prawomocnosci = data_prawomocnosci(dzien_doreczenia, miesiac_doreczenia, rok_doreczenia)

st.write("Data prawomocności orzeczenia: ", data_prawomocnosci)
