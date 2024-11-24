import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Faturamento")

# Carregar os dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
df["Day of Week"] = df["Date"].dt.day_name()

# Filtro por Mês
months = [0] + sorted(df["Date"].dt.month.unique())  # 0 representa "Todos"
month = st.sidebar.select_slider("Selecione o mês:", options=months, value=0)

# Filtro por Tipo de Cliente
customer_types = ["Todos"] + list(df["Customer type"].unique())
customer_type = st.sidebar.selectbox("Selecione o tipo de cliente:", customer_types)

# Aplicar Filtros
df_filtered = df.copy()
if month != 0:  # 0 significa "Todos"
    df_filtered = df_filtered[df_filtered["Date"].dt.month == month]

if customer_type != "Todos":
    df_filtered = df_filtered[df_filtered["Customer type"] == customer_type]

# Barra lateral (desenvolvido por...)
st.sidebar.markdown("""
---
Desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
""")


# Card de Faturamento Total
st.metric(label="Faturamento Total", value=f"R$ {df_filtered['Total'].sum():,.2f}")

# Faturamento diário somado
daily_sales = df_filtered.groupby("Date")[["Total"]].sum().reset_index().sort_values("Date")
fig_date = px.line(daily_sales, x="Date", y="Total", title="Faturamento Diário (Somado por Dia)")
st.plotly_chart(fig_date, use_container_width=True)

# Gráficos em colunas (linha 2)
col1, col2 = st.columns(2)

# Gráfico: Contribuição por cidade
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.pie(city_total, values="Total", names="City", title="Contribuição por Cidade", 
                  hole=0.4)
col1.plotly_chart(fig_city, use_container_width=True)

# Ticket Médio e Percentual do Total
df_filtered["Ticket Médio"] = df_filtered["Total"] / df_filtered["Quantity"]
city_avg = df_filtered.groupby("City")[["Ticket Médio"]].mean().reset_index()
city_avg["Percentual"] = (city_avg["Ticket Médio"] / city_avg["Ticket Médio"].sum()) * 100

# Gráfico com rótulos
fig_avg = px.bar(city_avg, x="City", y="Ticket Médio", title="Ticket Médio por Cidade",
                 text=city_avg.apply(lambda row: f"R${row['Ticket Médio']:.2f} ({row['Percentual']:.1f}%)", axis=1))
fig_avg.update_traces(textposition="inside")  # Rótulos dentro das barras
col2.plotly_chart(fig_avg, use_container_width=True)


# Gráficos em colunas (linha 3)
col3, col4 = st.columns(2)

# Percentual no Treemap
product_totals = df_filtered.groupby("Product line")[["Total"]].sum()
product_totals["Percentual"] = (product_totals["Total"] / product_totals["Total"].sum()) * 100

fig_prod = px.treemap(df_filtered, path=["Product line"], values="Total",
                      title="Total de Vendas por Linha de Produto",
                      custom_data=["Total"])

# Adicionando rótulos com valor total e percentual
fig_prod.data[0].texttemplate = "<b>%{label}</b><br>R$%{value:,.2f}<br>(%{percentParent:.1%})"
col3.plotly_chart(fig_prod, use_container_width=True)


# Vendas por tipo de pagamento e percentuais
payment_totals = df_filtered.groupby("Payment")[["Total"]].sum().reset_index()
payment_totals["Percentual"] = (payment_totals["Total"] / payment_totals["Total"].sum()) * 100

# Gráfico com rótulos
fig_payment = px.bar(payment_totals, x="Payment", y="Total", color="Payment",
                     title="Vendas por Forma de Pagamento",
                     text=payment_totals.apply(lambda row: f"R${row['Total']:.2f} ({row['Percentual']:.1f}%)", axis=1))
fig_payment.update_traces(textposition="inside")  # Rótulos dentro das barras
col4.plotly_chart(fig_payment, use_container_width=True)

