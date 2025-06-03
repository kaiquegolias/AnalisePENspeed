import pandas as pd
import streamlit as st
import plotly.graph_objects as go

SHEET_ID = '1VxX9HudzHmrw9uSe5UJfOeDI51xGD31gJKPT8KH7Kh4'
SHEET_NAME = 'Pagina1'
URL_CSV = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

def carregar_dados(url_csv, coluna_status='status'):
    try:
        df = pd.read_csv(url_csv, encoding='utf-8')
        total_chamados = len(df)
        concluido = df[coluna_status].astype(str).str.contains('OK', case=False, na=False).sum()
        nao_concluido = total_chamados - concluido
        return total_chamados, concluido, nao_concluido
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return 0, 0, 0

def plot_pizza_plotly(concluido, nao_concluido):
    labels = ['Concluídos', 'Não Concluídos']
    values = [concluido, nao_concluido]
    colors = ['#2E86C1', '#D35400']

    fig = go.Figure(data=[go.Pie(
        labels=['Concluídos', 'Não Concluídos'],  # Ou poderia usar só 'Status'
        values=values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
        textinfo='percent',  # Removido 'label' -> Mostra só percentual
        textfont=dict(size=14, family='Arial'),
        hoverinfo='label+value+percent'
    )])

    fig.update_layout(
        title_text='Distribuição Percentual',
        title_font_size=24,
        title_x=0.5,
        font=dict(family='Arial', size=16),
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor='center', font=dict(size=14)),
        margin=dict(t=80, b=20, l=20, r=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=400,
        width=600
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="Painel de Chamados", layout="centered")

    st.title("📊 Estatística de Chamados")

    coluna_status = st.text_input("Nome da coluna de status", value='status')

    total, concluido, nao_concluido = carregar_dados(URL_CSV, coluna_status)

    st.subheader("📌 Resumo dos Chamados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Chamados", total)
    col2.metric("Chamados Concluídos", concluido)
    col3.metric("Chamados Não Concluídos", nao_concluido)

    if total > 0:
        st.subheader("📊 Gráfico de Distribuição")
        plot_pizza_plotly(concluido, nao_concluido)

if __name__ == "__main__":
    main()
