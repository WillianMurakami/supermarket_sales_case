import streamlit as st

# Configuração inicial
st.set_page_config(page_title="Supermarket Dashboard", layout="wide")

# Barra lateral (desenvolvido por...)
st.sidebar.markdown("""
---
Desenvolvido por [Willian Murakami](https://www.linkedin.com/in/willian-murakami/)
""")

# Título e Introdução
st.title("📊 Dashboard Gerencial – Supermarket Sales")
st.markdown("""
Bem-vindo ao painel gerencial de vendas do Supermercado!  
Aqui você encontrará análises detalhadas sobre o faturamento, comportamento dos clientes e performance geral.  

### Sobre o Negócio:
A **Supermarket Sales** é uma empresa fictícia de varejo que atua em três cidades e utiliza este painel para analisar o desempenho de suas vendas. Os dados incluem:
- **Faturamento**: Vendas totais por dia, cidade, e forma de pagamento.
- **Clientes**: Avaliação geral, perfil dos clientes e comportamento de compra.

### Explore as Páginas:
- **Faturamento**: Veja o desempenho financeiro detalhado.
- **Clientes**: Descubra o perfil e comportamento do cliente.
""")
