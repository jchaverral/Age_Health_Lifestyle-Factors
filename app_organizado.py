#  poetry run streamlit run app_organizado.py

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# Usar st.cache para cargar los datos
@st.cache_data
def load_data():
    """
    Carga los datos de ejemplo usando seaborn.
    Se usa st.cache para que los datos se carguen solo una vez y se mantengan en memoria.
    Esto es útil para evitar cargar los datos en cada interacción con la aplicación.
    """
    return sns.load_dataset("tips")


def main():
    
    APP_TITLE = "Análisis Avanzado de Datos con Streamlit"
    st.set_page_config(
        page_title=APP_TITLE, layout="wide", page_icon=":chart_with_upwards_trend:"
    )
    st.image(image="images/logo.webp", use_column_width=False, width=400)
    st.title(APP_TITLE)

    # Subir archivo
    st.sidebar.title("⚙️ Opciones")
    df = load_data()  # Cargar datos usando la función cacheada

    # Crear dos columnas
    col1, col2 = st.columns(2)
    with col1:
        # Mostrar los datos
        st.header("📊 Datos de ejemplo:")
        st.dataframe(df)

    with col2:
        # Mostrar estadísticas descriptivas
        st.header("📈 Estadísticas descriptivas:")
        st.write(df.describe())

    st.write("----")

    # Crear barra lateral para seleccionar el tipo de gráfico y filtrar datos
    chart_type = st.sidebar.selectbox(
        "Selecciona el tipo de gráfico:",
        ["Dispersión", "Barras", "Histograma", "Boxplot"],
    )

    # Filtrar datos por múltiples columnas
    st.sidebar.subheader("Filtros")
    days = st.sidebar.multiselect(
        "📅 Selecciona los días:", df["day"].unique(), default=df["day"].unique()
    )
    times = st.sidebar.multiselect(
        "⏰ Selecciona los tiempos:", df["time"].unique(), default=df["time"].unique()
    )
    smokers = st.sidebar.multiselect(
        "🚬 Selecciona si son fumadores:",
        df["smoker"].unique(),
        default=df["smoker"].unique(),
    )
    sexes = st.sidebar.multiselect(
        "👤 Selecciona el sexo:", df["sex"].unique(), default=df["sex"].unique()
    )

    # Aplicar filtros
    filtered_df = df[
        (df["day"].isin(days))
        & (df["time"].isin(times))
        & (df["smoker"].isin(smokers))
        & (df["sex"].isin(sexes))
    ]

    # Crear dos columnas
    col1, col2 = st.columns(2)

    # Mostrar el gráfico seleccionado en la primera columna
    with col1:
        if chart_type == "Dispersión":
            st.header("Gráfico de dispersión entre total_bill y tip:")
            fig, ax = plt.subplots()
            sns.scatterplot(
                data=filtered_df, x="total_bill", y="tip", ax=ax, color="blue"
            )
            st.pyplot(fig)
        elif chart_type == "Barras":
            st.header("Gráfico de barras del total de cuentas por día:")
            fig, ax = plt.subplots()
            sns.barplot(
                data=filtered_df,
                x="day",
                y="total_bill",
                ax=ax,
                ci=None,
                color="lightblue",
            )
            st.pyplot(fig)
        elif chart_type == "Histograma":
            st.header("Histograma del total de cuentas:")
            fig, ax = plt.subplots()
            sns.histplot(
                data=filtered_df, x="total_bill", bins=10, ax=ax, color="skyblue"
            )
            st.pyplot(fig)
        elif chart_type == "Boxplot":
            st.header("Boxplot del total de cuentas por día:")
            fig, ax = plt.subplots()
            sns.boxplot(
                data=filtered_df, x="day", y="total_bill", ax=ax, color="lightgreen"
            )
            st.pyplot(fig)

    # Interactividad adicional
    with col2:
        st.header("Interactividad adicional:")
        show_data = st.checkbox("Mostrar datos filtrados")
        if show_data:
            st.dataframe(filtered_df)

        st.subheader("Control deslizante para filtrar por total_bill:")
        total_bill_min = st.slider(
            "Total Bill mínimo",
            float(df["total_bill"].min()),
            float(df["total_bill"].max()),
            float(df["total_bill"].min()),
        )
        filtered_df = filtered_df[filtered_df["total_bill"] >= total_bill_min]
        st.dataframe(filtered_df)


if __name__ == "__main__":
    #  Esto se usa para ejecutar la función main() directamente desde este archivo
    main()
