import streamlit as st
import plotly.express as px
import datetime as dt
import datetime
import pandas as pd
import pytz
import calendar

# Leer los datos para cada año
df_2020 =pd.read_csv("./src/proyecto_calidad_del_aire.csv")
df_2021 =pd.read_csv("./src/datos_calidad_2021.csv")
df_2023 =pd.read_csv("./src/datos_calidad_2.csv")

# Crear un diccionario para almacenar los DataFrames de cada año
dataframes = {"2020": df_2020, "2021": df_2021, "2023": df_2023}

# Título principal
st.title("Calidad del aire en Medellín")

# Menú desplegable para seleccionar el año
selected_year = st.selectbox("Seleccionar año", list(dataframes.keys()))

def aggregate_columns(df):
  df["pm25"]= df[df["parameter"]=="pm25"]["value"]
  df["pm10"]= df[df["parameter"]=="pm10"]["value"]
  df["o3"]= df[df["parameter"]=="o3"]["value"]
  df["no2"]= df[df["parameter"]=="no2"]["value"]
  df["co"]= df[df["parameter"]=="co"]["value"]
  df["so2"]= df[df["parameter"]=="so2"]["value"]

  return df



# Obtener el DataFrame correspondiente al año seleccionado
selected_df = dataframes[selected_year]
#df= selected_df.copy()
# # Convertir a datetime
if selected_year=="2023":
  selected_df= aggregate_columns(selected_df)

selected_df["date.utc"] = pd.to_datetime(selected_df["date.utc"])
selected_df.reset_index(drop=True, inplace=True)

# # Eliminar valores que no tienen sentido
selected_df.drop(selected_df[selected_df["value"]==-9999.0].index, inplace=True)

# # Group by para graficar 
# grouped_df = df.groupby(["location", "date.utc"])[["pm10", "pm25", "o3", "no2", "co", "so2"]].sum()


# Mostrar un desplegable para seleccionar el parámetro
parameter = st.selectbox("Seleccionar parámetro", ["pm25", "pm10", "no2", "o3", "co"])


import datetime as dt
# Gráfica de barras por mes
dk = selected_df[["location", parameter, "date.utc"]]
dk_ = dk.groupby([dk["date.utc"].dt.month, pd.Grouper(key="location")]).mean().dropna()
# Convertir los números de mes a nombres de mes
#dk_.reset_index(inplace= True)
#dk_["date.utc"] = dk_["date.utc"].apply(lambda x: calendar.month_abbr[int(x)])

# Crear la gráfica de barras con Plotly Express
fig = px.bar(dk_, x='date.utc', y=parameter, color='location', barmode='group',
             labels={"date.utc": "Mes", parameter: f" Concentración  {parameter}  (&mu;g/m<sup>3</sup>)"},
             width=1100,  # Ancho de la gráfica en píxeles
             height=600   # Altura de la gráfica en píxeles
             )
# Mostrar la gráfica de barras en Streamlit
# Agregar el código LaTeX al eje y de la gráfica
#fig.update_yaxes(title_text=f"Concentración {parameter} (&mu;g/m<sup>3</sup>)")


st.plotly_chart(fig)

# Convertir la columna 'date.utc' a la zona horaria de Bogotá
bogota_tz = pytz.timezone('America/Bogota')
selected_df['date.utc'] = selected_df['date.utc'].apply(lambda x: x.tz_convert(tz=bogota_tz))

# Calcular el promedio del parámetro seleccionado por hora y por ubicación
l = selected_df.groupby([selected_df["date.utc"].dt.hour, pd.Grouper(key="location")])[parameter].mean().dropna()

# Crear la gráfica de línea con Plotly Express
fig2 = px.line(l.reset_index(), x='date.utc', y=parameter, color='location',
               labels={"date.utc": "Horas del día", parameter: f"Concentración {parameter}($\mu g/m^3$)"},
               width=1100,  # Ancho de la gráfica en píxeles
               height=600   # Altura de la gráfica en píxeles
               )

# Mostrar la gráfica de línea en Streamlit
st.plotly_chart(fig2)

# Filtrar el DataFrame según el parámetro seleccionado
filtered_df = selected_df[selected_df["parameter"] == parameter]

# Obtener las ubicaciones únicas de las estaciones de monitoreo para el parámetro seleccionado
unique_locations = filtered_df[["location", "coordinates.latitude", "coordinates.longitude"]].drop_duplicates()

# Añadir un título HTML para el mapa
st.markdown(f"<h2>Ubicaciones de las estaciones de monitoreo para el parámetro {parameter}</h2>", unsafe_allow_html=True)

# Mapa con las ubicaciones de las estaciones de monitoreo para el parámetro seleccionado
fig_map = px.scatter_mapbox(unique_locations, lat="coordinates.latitude", lon="coordinates.longitude", 
                             hover_name="location", zoom=10, size_max=1000)
fig_map.update_traces(marker=dict(color="blue", opacity=1.0))
fig_map.update_layout(mapbox_style="carto-positron")
st.plotly_chart(fig_map)
# import streamlit as st
# import plotly.express as px
# import pandas as pd
# import pytz
# import calendar

# # Crear datos de ejemplo
# data = {
#     "location": ["A", "B", "C", "A", "B", "C"],
#     "pm25": [10, 20, 30, 15, 25, 35],
#     "date.utc": pd.date_range(start="2022-01-01", periods=6)
# }

# df = pd.read_csv("../../Downloads/datos_calidad_2021.csv")

# # Convertir a datetime
# df["date.utc"] = pd.to_datetime(df["date.utc"])
# df.reset_index(drop=True, inplace=True)

# # Eliminar valores que no tienen sentido
# df.drop(df[df["value"]==-9999.0].index, inplace=True)

# # Group by para graficar 
# grouped_df = df.groupby(["location", "date.utc"])[["pm10", "pm25", "o3", "no2", "co", "so2"]].sum()

# # Título principal
# st.title("Calidad del aire en Medellín")

# # Menú desplegable para seleccionar el parámetro
# parameter = st.selectbox("Seleccionar parámetro", ["pm25", "pm10", "no2", "o3", "co"])

# # Gráfica de barras por mes
# dk = df[["location", parameter, "date.utc"]]  # Cambiar aquí para usar el parámetro seleccionado
# dk_ = dk.groupby([dk["date.utc"].dt.month, pd.Grouper(key="location")]).mean().dropna()

# # Convertir los números de mes a nombres de mes
# dk_.reset_index(inplace=True)
# dk_["date.utc"] = dk_["date.utc"].apply(lambda x: calendar.month_abbr[int(x)])

# # Crear la gráfica de barras con Plotly Express
# fig = px.bar(dk_, x='date.utc', y=parameter, color='location', barmode='group',
#              labels={"date.utc": "Mes", parameter: f"{parameter} ($\mu g/m^3$)"},
#              width=1000,  # Ancho de la gráfica en píxeles
#              height=600   # Altura de la gráfica en píxeles
#              )

# # Mostrar la gráfica de barras en Streamlit
# st.plotly_chart(fig)

# # Convertir la columna 'date.utc' a la zona horaria de Bogotá
# bogota_tz = pytz.timezone('America/Bogota')
# df['date.utc'] = df['date.utc'].apply(lambda x: x.tz_convert(tz=bogota_tz))

# # Calcular el promedio del parámetro seleccionado por hora y por ubicación
# l = df.groupby([df["date.utc"].dt.hour, pd.Grouper(key="location")])[parameter].mean().dropna()

# # Crear la gráfica de línea con Plotly Express
# fig2 = px.line(l.reset_index(), x='date.utc', y=parameter, color='location',
#                labels={"date.utc": "Horas del día", parameter: f"{parameter} ($\mu g/m^3$)"},
#                width=1000,  # Ancho de la gráfica en píxeles
#                height=600   # Altura de la gráfica en píxeles
#                )

# # Mostrar la gráfica de línea en Streamlit
# st.plotly_chart(fig2)
