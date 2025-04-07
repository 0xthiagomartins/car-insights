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
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1.5rem;
    }
    .step-header {
        font-size: 1.8rem;
        color: #1E88E5;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1E88E5;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #757575;
    }
    .btn-primary {
        background-color: #1E88E5;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }
    .btn-secondary {
        background-color: #9E9E9E;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }
    .progress-container {
        margin-bottom: 2rem;
    }
    .progress-step {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #E0E0E0;
        color: #757575;
        text-align: center;
        line-height: 30px;
        margin: 0 10px;
        position: relative;
    }
    .progress-step.active {
        background-color: #1E88E5;
        color: white;
    }
    .progress-step.completed {
        background-color: #4CAF50;
        color: white;
    }
    .progress-line {
        display: inline-block;
        height: 3px;
        width: 100px;
        background-color: #E0E0E0;
        position: relative;
        top: -15px;
    }
    .progress-line.active {
        background-color: #1E88E5;
    }
    .progress-line.completed {
        background-color: #4CAF50;
    }
    .brand-logo {
        max-width: 150px;
        margin: 1rem auto;
        display: block;
    }
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
    }
    .comparison-table th, .comparison-table td {
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid #E0E0E0;
    }
    .comparison-table th {
        background-color: #F5F5F5;
        font-weight: bold;
    }
    .comparison-table tr:hover {
        background-color: #F5F5F5;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    # Create a custom progress indicator
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    
    # Define the steps
    steps = ["Marca/Modelo", "Ano/Estado/Versão", "Resultados"]
    
    # Create a custom progress indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        for i, step in enumerate(steps):
            if i < st.session_state.step - 1:
                st.markdown(f'<div class="progress-step completed">{i+1}</div>', unsafe_allow_html=True)
            elif i == st.session_state.step - 1:
                st.markdown(f'<div class="progress-step active">{i+1}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="progress-step">{i+1}</div>', unsafe_allow_html=True)
            
            if i < len(steps) - 1:
                if i < st.session_state.step - 1:
                    st.markdown('<div class="progress-line completed"></div>', unsafe_allow_html=True)
                elif i == st.session_state.step - 1:
                    st.markdown('<div class="progress-line active"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="progress-line"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<h2 class="step-header">Passo {st.session_state.step}: {steps[st.session_state.step - 1]}</h2>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        for i, step in enumerate(steps):
            st.markdown(f'<div style="margin-bottom: 10px;">{step}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    st.markdown('<h3 class="sub-header">Escolha a marca e modelo do veículo que quer pesquisar</h3>', unsafe_allow_html=True)
    
    # Create columns for brand and model selection
    col1, col2 = st.columns(2)
    
    with col1:
        # Brand selection
        st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown('<label style="font-weight: bold; margin-bottom: 0.5rem;">Marca</label>', unsafe_allow_html=True)
        brands = db_manager.get_brands()
        selected_brand = st.selectbox("", brands, key="brand_select")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display brand logo if available
        if selected_brand:
            logo_url = db_manager.get_brand_logo_url(selected_brand)
            if logo_url:
                try:
                    st.markdown(f'<img src="{logo_url}" class="brand-logo" alt="{selected_brand} logo">', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao carregar logo: {e}")
    
    with col2:
        # Model selection (would be dynamic based on brand in a real app)
        if selected_brand:
            st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
            st.markdown('<label style="font-weight: bold; margin-bottom: 0.5rem;">Modelo</label>', unsafe_allow_html=True)
            models = db_manager.get_models_by_brand(selected_brand)
            selected_model = st.selectbox("", models, key="model_select")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Store selections in session state
            st.session_state.selected_brand = selected_brand
            st.session_state.selected_model = selected_model
    
    # Add a next button below the columns
    if selected_brand and selected_model:
        st.markdown('<div style="text-align: center; margin-top: 2rem;">', unsafe_allow_html=True)
        if st.button("Próximo", key="next_step1", use_container_width=True):
            st.session_state.step = 2
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_step2():
    """Render the second step: Year/State/Version selection"""
    
    st.markdown('<h3 class="sub-header">Complete os dados abaixo para obter o resultado</h3>', unsafe_allow_html=True)
    
    # Create columns for year, state, and version selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Year selection
        st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown('<label style="font-weight: bold; margin-bottom: 0.5rem;">Ano do veículo</label>', unsafe_allow_html=True)
        years = db_manager.get_years()
        selected_year = st.selectbox("", years, key="year_select")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # State selection
        st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
        st.markdown('<label style="font-weight: bold; margin-bottom: 0.5rem;">Estado</label>', unsafe_allow_html=True)
        states = db_manager.get_states()
        selected_state = st.selectbox("", states, key="state_select")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        # Version selection (would be dynamic based on model in a real app)
        if st.session_state.selected_model:
            st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
            st.markdown('<label style="font-weight: bold; margin-bottom: 0.5rem;">Versão</label>', unsafe_allow_html=True)
            versions = db_manager.get_versions_by_model(st.session_state.selected_model)
            selected_version = st.selectbox("", versions, key="version_select")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Store selections in session state
            st.session_state.selected_year = selected_year
            st.session_state.selected_state = selected_state
            st.session_state.selected_version = selected_version
    
    # Add navigation buttons below the columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anterior", key="prev_step2", use_container_width=True):
            st.session_state.step = 1
            st.experimental_rerun()
    
    with col2:
        if st.button("Próximo", key="next_step2", use_container_width=True):
            st.session_state.step = 3
            st.experimental_rerun()

def render_step3():
    """Render the third step: Results"""
    
    st.markdown('<h3 class="sub-header">Resultado da Consulta</h3>', unsafe_allow_html=True)
    
    # Display the selected options in a nice card
    st.markdown('<div style="background-color: #F5F5F5; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-bottom: 1rem;">Detalhes do Veículo</h4>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<p><strong>Marca:</strong> {st.session_state.selected_brand}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Modelo:</strong> {st.session_state.selected_model}</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<p><strong>Ano:</strong> {st.session_state.selected_year}</p>', unsafe_allow_html=True)
        st.markdown(f'<p><strong>Estado:</strong> {st.session_state.selected_state}</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<p><strong>Versão:</strong> {st.session_state.selected_version}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create a sample price range
    base_price = 50000 + (2024 - st.session_state.selected_year) * 5000
    min_price = base_price - random.randint(5000, 10000)
    max_price = base_price + random.randint(5000, 10000)
    
    # Calculate purchase and sale values
    purchase_value = base_price - random.randint(5000, 15000)
    sale_value = base_price + random.randint(5000, 15000)
    
    # Display price metrics in a more visually appealing way
    st.markdown('<h4 style="margin: 2rem 0 1rem 0;">Faixa de Preços</h4>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">R$ {min_price:,.2f}</div>
            <div class="metric-label">Preço Mínimo</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">R$ {base_price:,.2f}</div>
            <div class="metric-label">Preço Médio</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">R$ {max_price:,.2f}</div>
            <div class="metric-label">Preço Máximo</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Display purchase and sale values side by side
    st.markdown('<h4 style="margin: 2rem 0 1rem 0;">Valores de Mercado</h4>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card" style="background-color: #E8F5E9;">
            <div class="metric-value" style="color: #4CAF50;">R$ {purchase_value:,.2f}</div>
            <div class="metric-label">Valor que PAGAM por este veículo</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card" style="background-color: #FFEBEE;">
            <div class="metric-value" style="color: #F44336;">R$ {sale_value:,.2f}</div>
            <div class="metric-label">Valor que VENDEM este veículo</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Add a chart showing price trend
    st.markdown('<h4 style="margin: 2rem 0 1rem 0;">Tendência de Preços</h4>', unsafe_allow_html=True)
    
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
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    fig.update_traces(line=dict(color='#1E88E5', width=3))
    st.plotly_chart(fig, use_container_width=True)
    
    # Add a comparison with similar vehicles
    st.markdown('<h4 style="margin: 2rem 0 1rem 0;">Comparação com Veículos Similares</h4>', unsafe_allow_html=True)
    
    # Sample data for similar vehicles
    similar_vehicles = [
        {"Marca": st.session_state.selected_brand, "Modelo": st.session_state.selected_model, "Ano": st.session_state.selected_year, "Preço": base_price},
        {"Marca": "Honda", "Modelo": "Civic", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-5000, 5000)},
        {"Marca": "Volkswagen", "Modelo": "Gol", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-8000, 8000)},
        {"Marca": "Fiat", "Modelo": "Uno", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-10000, 10000)},
        {"Marca": "Chevrolet", "Modelo": "Onix", "Ano": st.session_state.selected_year, "Preço": base_price + random.randint(-7000, 7000)}
    ]
    
    # Create a styled table
    st.markdown('''
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Marca</th>
                <th>Modelo</th>
                <th>Ano</th>
                <th>Preço</th>
            </tr>
        </thead>
        <tbody>
    ''', unsafe_allow_html=True)
    
    for vehicle in similar_vehicles:
        st.markdown(f'''
            <tr>
                <td>{vehicle["Marca"]}</td>
                <td>{vehicle["Modelo"]}</td>
                <td>{vehicle["Ano"]}</td>
                <td>R$ {vehicle["Preço"]:,.2f}</td>
            </tr>
        ''', unsafe_allow_html=True)
    
    st.markdown('</tbody></table>', unsafe_allow_html=True)
    
    # Add navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Anterior", key="prev_step3", use_container_width=True):
            st.session_state.step = 2
            st.experimental_rerun()
    
    with col2:
        if st.button("Nova Consulta", key="new_search", use_container_width=True):
            st.session_state.step = 1
            st.experimental_rerun()

def render_info_sections():
    """Render informational sections about the Table Reality concept"""
    
    # Section 1: Tabela de Referência vs Tabela de Realidade
    st.markdown('<h2 class="sub-header">Tabela de Referência? Tabela de Realidade!</h2>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="info-box">
        Você certamente já consultou tabelas de mercado para verificar o valor de um veículo. 
        Você certamente tentou vender um veículo pelo preço indicado. 
        Você certamente se frustrou.
    </div>
    ''', unsafe_allow_html=True)
    
    # Add a visual comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div style='text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;'>
            <h3 style="color: #757575;">Tabela de Referência</h3>
            <p>Valores teóricos baseados em estimativas</p>
            <p>Não reflete o mercado real</p>
            <p>Desatualizada frequentemente</p>
            <p>Não considera variações regionais</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style='text-align: center; padding: 20px; border: 1px solid #4CAF50; border-radius: 10px; background-color: #e8f5e9;'>
            <h3 style="color: #4CAF50;">Tabela de Realidade</h3>
            <p>Valores reais baseados em transações</p>
            <p>Reflete o mercado atual</p>
            <p>Atualizada mensalmente</p>
            <p>Considera variações regionais</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Section 2: Como chegamos a esse preço?
    st.markdown('<h2 class="sub-header">Como chegamos a esse preço?</h2>', unsafe_allow_html=True)
    
    st.markdown('<h4>Características do Veículo</h4>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="info-box">
        Cada veículo é único, com características distintas que influenciam diretamente o seu valor.
        Para chegar ao preço referencial de mercado, analisamos mensalmente inúmeros parâmetros além das mais de 200 mil avaliações de veículos com base nas seguintes informações:
    </div>
    ''', unsafe_allow_html=True)
    
    # Create a visual representation of vehicle characteristics
    characteristics = {
        "Marca": "Influência da reputação e valor de mercado da marca",
        "Ano": "Desvalorização natural ao longo do tempo",
        "Modelo": "Popularidade e demanda pelo modelo específico",
        "Localização": "Variações de preço por região do país",
        "Versão": "Equipamentos e acabamentos específicos"
    }
    
    for char, desc in characteristics.items():
        st.markdown(f'<p><strong>{char}</strong>: {desc}</p>', unsafe_allow_html=True)
    
    # Add a visual representation
    st.markdown('<h4>Valores do Veículo</h4>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="info-box">
        Depois de encontrarmos veículos com características semelhantes, analisamos o valor das transações para obtermos os preços mínimo, médio e máximo pelos quais o veículo em questão está sendo negociado, tanto para compra quanto para venda.
    </div>
    ''', unsafe_allow_html=True)
    
    # Create a visual representation of the price calculation process
    st.markdown('''
    <div style='text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;'>
        <h4 style="color: #1E88E5;">Processo de Cálculo de Preços</h4>
        <p>1. Coleta de dados de transações reais</p>
        <p>2. Filtragem por características similares</p>
        <p>3. Análise estatística dos valores</p>
        <p>4. Cálculo de preços mínimo, médio e máximo</p>
        <p>5. Validação por especialistas do mercado</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Add a call to action
    st.markdown('''
    <div style="background-color: #E3F2FD; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1E88E5; margin-top: 2rem; text-align: center;">
        <h3 style="color: #1E88E5;">Use nossa Tabela Realidade</h3>
        <p>Obtenha valores precisos e atualizados para seu veículo, baseados em transações reais do mercado.</p>
    </div>
    ''', unsafe_allow_html=True) 