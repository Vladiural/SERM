import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Аналитика Подача66", layout="wide")

# Заголовок
st.title("📊 Дашборд эффективности бизнеса")

# Функция для загрузки данных (здесь можно подключить твой парсер для Ozon/WB)
@st.cache_data
def load_data():
    # Создадим фиктивные данные для примера
    data = {
        'Дата': pd.date_range(start='2026-05-01', periods=30),
        'Выручка': [25000 + i*500 for i in range(30)],
        'Заказы': [5, 6, 4, 8, 7, 10, 12, 11, 9, 13] * 3,
        'Техника': ['Манипулятор 3/5', 'Манипулятор 5/7', 'Экскаватор MST544'] * 10
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR (Фильтры) ---
st.sidebar.header("Фильтры")
tech_filter = st.sidebar.multiselect("Выберите технику:", 
                                     options=df['Техника'].unique(), 
                                     default=df['Техника'].unique())

filtered_df = df[df['Техника'].isin(tech_filter)]

# --- ВЕРХНИЙ РЯД (KPI) ---
col1, col2, col3 = st.columns(3)
total_rev = filtered_df['Выручка'].sum()
total_orders = filtered_df['Заказы'].sum()
avg_check = total_rev / total_orders if total_orders > 0 else 0

col1.metric("Общая выручка", f"{total_rev:,} ₽")
col2.metric("Всего заказов", total_orders)
col3.metric("Средний чек", f"{avg_check:,.0f} ₽")

st.divider()

# --- ГРАФИКИ ---
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📈 Динамика выручки по дням")
    fig_line = px.line(filtered_df, x='Дата', y='Выручка', color='Техника',
                       template='plotly_white', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with right_col:
    st.subheader("🏗️ Доля заказов по технике")
    fig_pie = px.pie(filtered_df, values='Заказы', names='Техника', 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- ТАБЛИЦА С ДАННЫМИ ---
with st.expander("Посмотреть детализированную таблицу"):
    st.dataframe(filtered_df.sort_values(by='Дата', ascending=False), use_container_width=True)