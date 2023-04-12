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
  else:
      raise ValueError('Nieznany typ orzeczenia')
  data_prawomocnosci = data_doreczenia + datetime.timedelta(days=okres_prawomocnosci +1)

  # pobranie listy dat świątecznych w Polsce
  polskie_swieto = holidays.Polish()

  while True:
      # sprawdzenie, czy data prawomocności przypada na dzień świąteczny lub dzień wolny od pracy
      if data_prawomocnosci.weekday() >= 5 or data_prawomocnosci in polskie_swieto:
          data_prawomocnosci += datetime.timedelta(days=1)
      else:
          break
  return data_prawomocnosci

st.title("Obliczanie daty prawomocności orzeczeń")
data_doreczenia = st.date_input("Podaj datę doręczenia", value=datetime.date(2023, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100,12,31))
typ_orzeczenia = st.selectbox("Typ orzeczenia", ["wyrok", "postanowienie", "decyzja II instancji", "decyzja II instancji - art. 138 § 2", "decyzja I instancji"])

data_prawomocnosci = data_prawomocnosci(data_doreczenia, typ_orzeczenia)

st.write("Data prawomocności orzeczenia: ", data_prawomocnosci)
