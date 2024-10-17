import pandas              as pd
import numpy               as np
import matplotlib.pyplot   as plt
import seaborn as sns
from matplotlib.lines import Line2D
import streamlit as st

df = pd.read_csv('Train.csv')
tabla = pd.set_option('display.max_columns', None)
df.head(5)



df[['Height (cm)',
 'Weight (kg)',
 'Cholesterol Level (mg/dL)',
 'BMI',
 'Blood Glucose Level (mg/dL)',
 'Hearing Ability (dB)',
 'Cognitive Function',
 'Stress Levels',
 'Pollution Exposure',
 'Sun Exposure',
 'Age (years)']] = df[['Height (cm)',
 'Weight (kg)',
 'Cholesterol Level (mg/dL)',
 'BMI',
 'Blood Glucose Level (mg/dL)',
 'Hearing Ability (dB)',
 'Cognitive Function',
 'Stress Levels',
 'Pollution Exposure',
 'Sun Exposure',
 'Age (years)']].round(0)

df[['Height (cm)',
 'Weight (kg)',
 'Cholesterol Level (mg/dL)',
 'BMI',
 'Blood Glucose Level (mg/dL)',
 'Hearing Ability (dB)',
 'Cognitive Function',
 'Stress Levels',
 'Pollution Exposure',
 'Sun Exposure',
 'Age (years)']].astype(int)  

column_list = list(df.columns)
titulos_columnas = pd.DataFrame(df.columns, columns=['Data'])

df['Rango edad'] = df['Age (years)'].apply(lambda valor: '18-20' if valor <= 20 else
                                                         '21-29' if 21 <= valor <= 29 else
                                                         '30-39' if 30 <= valor <= 39 else
                                                         '40-49' if 40 <= valor <= 49 else
                                                         '50-59' if 50 <= valor < 60 else 'mayor a 60')


def figura_distr (grupo, nom_grupo, valor, color_graf, color_borde):
  df_graf = df.groupby(grupo).count().reset_index()
  categorias = df_graf[grupo]
  valores = df_graf[valor]
  x = np.arange(len(categorias))
  plt.bar(x, valores, color = color_graf, edgecolor=color_borde, alpha=0.75)
  plt.title(f'distribución de datos por {nom_grupo}', fontsize=12, fontweight='bold', pad=20)
  plt.xlabel(f'{grupo}', fontsize=10)
  plt.ylabel('Cantidad', fontsize=10)
  for i in range(len(categorias)):
      plt.text(x[i], valores[i]+0.5, str(valores[i]),  rotation=90, ha='center', va='bottom', fontsize=10, color='black')
  plt.xticks(x, categorias, ha='center')
  plt.grid(axis='y', linestyle='--', alpha=0.7)



def main():
    
    APP_TITLE = "Data analysis based on various health and lifestyle factors"
    st.title(APP_TITLE)

    st.write(df.head(5))      

    st.write("----")

    # Subir archivo
    st.sidebar.title("⚙️ Opciones")
   

    # Crear dos columnas
    col1, col2 = st.columns(2)
    with col1:
        # Mostrar los datos
        st.header("📊 Datos:")
        st.write(titulos_columnas)

    with col2:
        # Mostrar estadísticas descriptivas
        st.header("📈 Estadísticas descriptivas:")
        st.write(df.describe())

    st.write("----")

    # Crear barra lateral para seleccionar el tipo de gráfico y filtrar datos
    chart_type = st.sidebar.selectbox(
        "Selecciona los datos de la distribucion:",
        ["Por genero", "Por rango de edad"],
    )


    # Crear dos columnas
    col1, col2 = st.columns(2)

    # Mostrar el gráfico seleccionado en la primera columna
    with col1:
        if chart_type == "Por genero":
            st.header("distribución de datos por genero:")
            fig = figura_distr ('Gender','el genero','Height (cm)', '#87ceeb','black')
            sns.scatterplot(fig)
            st.pyplot(fig)

        elif chart_type == "Por rango de edad":
            st.header("distribución de datos por rango de edad")
            fig2 = figura_distr ('Rango edad','el rango de edades','Height (cm)', '#ffff00','black')
            sns.scatterplot(fig2)
            st.pyplot(fig2)
        


if __name__ == "__main__":
    #  Esto se usa para ejecutar la función main() directamente desde este archivo
    main()
