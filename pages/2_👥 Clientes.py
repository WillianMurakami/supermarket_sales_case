import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👥 Clientes")

# Carregar os dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df["Day of Week"] = df["Date"].dt.day_name()

# Barra lateral (desenvolvido por...)
st.sidebar.markdown("""
---
Desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
""")

# Card de Avaliações
st.metric(label="Avaliação Média", value=f"{df['Rating'].mean():.2f} / 10.0")

# Gráficos em colunas (linha 1)
col1, col2 = st.columns(2)

# Gráfico: Gênero dos clientes
fig_gender = px.pie(df, names="Gender", title="Gênero dos Clientes", hole=0.4)
col1.plotly_chart(fig_gender, use_container_width=True)

# Contagem e Percentual por Tipo de Cliente
customer_counts = df["Customer type"].value_counts().reset_index()
customer_counts.columns = ["Customer type", "Count"]
customer_counts["Percentual"] = (customer_counts["Count"] / customer_counts["Count"].sum()) * 100

# Gráfico com Rótulos
fig_customer_type = px.bar(customer_counts, x="Customer type", y="Count", color="Customer type",
                           title="Tipo de Clientes",
                           text=customer_counts.apply(lambda row: f"{row['Count']} ({row['Percentual']:.1f}%)", axis=1))
fig_customer_type.update_traces(textposition="inside")  # Rótulos dentro das barras
col2.plotly_chart(fig_customer_type, use_container_width=True)

# Corrigir formato da coluna "Time"
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour

# Preparar os dados
df["Day of Week"] = pd.Categorical(df["Day of Week"], 
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                   ordered=True)
hourly_counts = df.groupby(["Day of Week", "Hour"]).size().reset_index(name="Count")

# Preparar os dados
hourly_avg = df.groupby(["Day of Week", "Hour"]).size().reset_index(name="Count")

# Contagem por Dia e Hora
heatmap_data = df.groupby(["Day of Week", "Hour"]).size().reset_index(name="Count")
heatmap_pivot = heatmap_data.pivot(index="Hour", columns="Day of Week", values="Count")

# Preparar os dados: Total de vendas por dia da semana e hora
df["Day of Week"] = pd.Categorical(df["Day of Week"], 
                                   categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                   ordered=True)
hourly_sales = df.groupby(["Day of Week", "Hour"])["Total"].sum().reset_index()

# Preparar os dados: Total de vendas por dia da semana e hora
heatmap_sales = df.groupby(["Day of Week", "Hour"])["Total"].sum().reset_index()
heatmap_pivot = heatmap_sales.pivot(index="Hour", columns="Day of Week", values="Total")

# Gráfico Heatmap com Anotações
import plotly.graph_objects as go
fig_annotated = go.Figure(data=go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale="Viridis",
    hoverongaps=False,
    colorbar=dict(title="Faturamento (R$)")
))

# Adicionar anotações com valores
for i, row in enumerate(heatmap_pivot.values):
    for j, val in enumerate(row):
        fig_annotated.add_annotation(
            x=heatmap_pivot.columns[j],  # Dia da semana
            y=heatmap_pivot.index[i],  # Hora
            text=f"R${val:,.2f}" if not pd.isna(val) else "",
            showarrow=False,
            font=dict(size=10, color="white")
        )

# Layout do gráfico
fig_annotated.update_layout(
    title="Faturamento por Dia e Hora (com valores)",
    xaxis_title="Dia da Semana",
    yaxis_title="Hora",
    yaxis_nticks=24
)
st.plotly_chart(fig_annotated, use_container_width=True)
