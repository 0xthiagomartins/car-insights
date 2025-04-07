import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import base64
from data import db_manager

def render():
    st.title("Tabela Realidade")
    st.write("A Tabela Realidade é uma iniciativa da Car Insights, a maior plataforma de avaliação, negociação e gestão de seminovos do Brasil.")
    
    # Initialize session state for steps if not already done
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    if 'selected_brand' not in st.session_state:
        st.session_state.selected_brand = None
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None
    
    if 'selected_year' not in st.session_state:
        st.session_state.selected_year = None
    
    if 'selected_state' not in st.session_state:
        st.session_state.selected_state = None
    
    if 'selected_version' not in st.session_state:
        st.session_state.selected_version = None
    
    # Create a progress bar for the steps
    st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Define the steps
    steps = ["Marca/Modelo", "Ano/Estado/Versão", "Resultados"]
    
    # Create a progress bar
    progress = st.progress(0)
    progress.progress((st.session_state.step - 1) / (len(steps) - 1))
    
    # Display the current step
    st.markdown(f"### Passo {st.session_state.step}: {steps[st.session_state.step - 1]}")
    
    # Render the appropriate step
    if st.session_state.step == 1:
        render_step1()
    elif st.session_state.step == 2:
        render_step2()
    elif st.session_state.step == 3:
        render_step3()
    
    # Add a divider after the steps
    st.markdown("---")
    
    # Add informational sections
    render_info_sections()

def render_step1():
    """Render the first step: Brand/Model selection"""
    
    st.subheader("Escolha a marca e modelo do veículo que quer pesquisar")
    
    # Create columns for brand and model selection
    col1, col2 = st.columns(2)
    
    with col1:
        # Brand selection
        brands = db_manager.get_brands()
        selected_brand = st.selectbox("Marca", brands, key="brand_select")
        
        # Display brand logo if available
        if selected_brand:
            logo_url = db_manager.get_brand_logo_url(selected_brand)
            if logo_url:
                try:
                    st.image(logo_url, width=100)
                except Exception as e:
                    st.error(f"Erro ao carregar logo: {e}")
    
    with col2:
        # Model selection (would be dynamic based on brand in a real app)
        if selected_brand:
            models = db_manager.get_models_by_brand(selected_brand)
            selected_model = st.selectbox("Modelo", models, key="model_select")
            
            # Store selections in session state
            st.session_state.selected_brand = selected_brand
            st.session_state.selected_model = selected_model
    
    # Add a next button below the columns
    if selected_brand and selected_model:
        if st.button("Próximo", key="next_step1"):
            st.session_state.step = 2
            st.experimental_rerun()

def render_step2():
    """Render the second step: Year/State/Version selection"""
    
    st.subheader("Complete os dados abaixo para obter o resultado")
    
    # Create columns for year, state, and version selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Year selection
        years = db_manager.get_years()
        selected_year = st.selectbox("Ano do veículo", years, key="year_select")
    
    with col2:
        # State selection
        states = db_manager.get_states()
        selected_state = st.selectbox("Estado", states, key="state_select")
    
    with col3:
        # Version selection (would be dynamic based on model in a real app)
        if st.session_state.selected_model:
            versions = db_manager.get_versions_by_model(st.session_state.selected_model)
            selected_version = st.selectbox("Versão", versions, key="version_select")
            
            # Store selections in session state
            st.session_state.selected_year = selected_year
            st.session_state.selected_state = selected_state
            st.session_state.selected_version = selected_version
    
    # Add navigation buttons below the columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anterior", key="prev_step2"):
            st.session_state.step = 1
            st.experimental_rerun()
    
    with col2:
        if st.button("Próximo", key="next_step2"):
            st.session_state.step = 3
            st.experimental_rerun()

def render_step3():
    """Render the third step: Results"""
    
    st.subheader("Resultado da Consulta")
    
    # Display the selected options
    st.write(f"**Marca:** {st.session_state.selected_brand}")
    st.write(f"**Modelo:** {st.session_state.selected_model}")
    st.write(f"**Ano:** {st.session_state.selected_year}")
    st.write(f"**Estado:** {st.session_state.selected_state}")
    st.write(f"**Versão:** {st.session_state.selected_version}")
    
    # Create a sample price range
    base_price = 50000 + (2024 - st.session_state.selected_year) * 5000
    min_price = base_price - random.randint(5000, 10000)
    max_price = base_price + random.randint(5000, 10000)
    
    # Calculate purchase and sale values
    purchase_value = base_price - random.randint(5000, 15000)
    sale_value = base_price + random.randint(5000, 15000)
    
    # Display price metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Preço Mínimo", f"R$ {min_price:,.2f}")
    
    with col2:
        st.metric("Preço Médio", f"R$ {base_price:,.2f}")
    
    with col3:
        st.metric("Preço Máximo", f"R$ {max_price:,.2f}")
    
    # Display purchase and sale values side by side
    st.subheader("Valores de Mercado")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Valor que PAGAM por este veículo", f"R$ {purchase_value:,.2f}")
    
    with col2:
        st.metric("Valor que VENDEM este veículo", f"R$ {sale_value:,.2f}")
    
    # Add a chart showing price trend
    st.subheader("Tendência de Preços")
    
    # Sample data for price trend
    months = [datetime.now() - timedelta(days=30*i) for i in range(12)]
    months.reverse()
    prices = [base_price - random.randint(1000, 5000) + i*random.randint(500, 2000) for i in range(12)]
    
    fig = px.line(
        x=months, 
        y=prices,
        title="Tendência de Preços nos Últimos 12 Meses",
        labels={"x": "Mês", "y": "Preço (R$)"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Add a comparison with similar vehicles
    st.subheader("Comparação com Veículos Similares")
    
    # Sample data for similar vehicles
    similar_vehicles = [
        {"Marca": st.session_state.selected_brand, "Modelo": st.session_state.selected_model, "Ano": st.session_state.selected_year, "Preço": base_price},
        {"Marca": "Honda", "Modelo": "Civic", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-5000, 5000)},
        {"Marca": "Volkswagen", "Modelo": "Gol", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-8000, 8000)},
        {"Marca": "Fiat", "Modelo": "Uno", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-10000, 10000)},
        {"Marca": "Chevrolet", "Modelo": "Onix", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-7000, 7000)}
    ]
    
    st.table(pd.DataFrame(similar_vehicles))
    
    # Add navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anterior", key="prev_step3"):
            st.session_state.step = 2
            st.experimental_rerun()
    
    with col2:
        if st.button("Nova Consulta", key="new_search"):
            st.session_state.step = 1
            st.experimental_rerun()

def render_info_sections():
    """Render informational sections about the Table Reality concept"""
    
    # Section 1: Tabela de Referência vs Tabela de Realidade
    st.header("Tabela de Referência? Tabela de Realidade!")
    
    st.write("""
    Você certamente já consultou tabelas de mercado para verificar o valor de um veículo. 
    Você certamente tentou vender um veículo pelo preço indicado. 
    Você certamente se frustrou.
    """)
    
    # Add a visual comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;'>
            <h3>Tabela de Referência</h3>
            <p>Valores teóricos baseados em estimativas</p>
            <p>Não reflete o mercado real</p>
            <p>Desatualizada frequentemente</p>
            <p>Não considera variações regionais</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #e8f5e9;'>
            <h3>Tabela de Realidade</h3>
            <p>Valores reais baseados em transações</p>
            <p>Reflete o mercado atual</p>
            <p>Atualizada mensalmente</p>
            <p>Considera variações regionais</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Section 2: Como chegamos a esse preço?
    st.header("Como chegamos a esse preço?")
    
    st.subheader("Características do Veículo")
    
    st.write("""
    Cada veículo é único, com características distintas que influenciam diretamente o seu valor.
    Para chegar ao preço referencial de mercado, analisamos mensalmente inúmeros parâmetros além das mais de 200 mil avaliações de veículos com base nas seguintes informações:
    """)
    
    # Create a visual representation of vehicle characteristics
    characteristics = {
        "Marca": "Influência da reputação e valor de mercado da marca",
        "Ano": "Desvalorização natural ao longo do tempo",
        "Modelo": "Popularidade e demanda pelo modelo específico",
        "Localização": "Variações de preço por região do país",
        "Versão": "Equipamentos e acabamentos específicos"
    }
    
    for char, desc in characteristics.items():
        st.markdown(f"**{char}**: {desc}")
    
    # Add a visual representation
    st.subheader("Valores do Veículo")
    
    st.write("""
    Depois de encontrarmos veículos com características semelhantes, analisamos o valor das transações para obtermos os preços mínimo, médio e máximo pelos quais o veículo em questão está sendo negociado, tanto para compra quanto para venda.
    """)
    
    # Create a visual representation of the price calculation process
    st.markdown("""
    <div style='text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 5px;'>
        <h4>Processo de Cálculo de Preços</h4>
        <p>1. Coleta de dados de transações reais</p>
        <p>2. Filtragem por características similares</p>
        <p>3. Análise estatística dos valores</p>
        <p>4. Cálculo de preços mínimo, médio e máximo</p>
        <p>5. Validação por especialistas do mercado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a call to action
    st.info("Use nossa Tabela Realidade para obter valores precisos e atualizados para seu veículo, baseados em transações reais do mercado.") 