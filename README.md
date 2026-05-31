# 📊 Superstore Analytics — ITAJR 2026

Painel analítico interativo construído com **Streamlit**, conectado ao **Supabase** (PostgreSQL),
respondendo 10 perguntas de negócio sobre o dataset Superstore com visualizações Plotly e insights textuais.

---

## Funcionalidades

- Conexão segura ao Supabase via variáveis de ambiente
- 10 análises de negócio com gráficos interativos (Plotly)
- Filtros globais: período, região/estado/cidade, segmento, categoria/subcategoria
- Insights textuais em cada pergunta
- Download CSV em cada análise
- Simulador avançado de desconto com sliders interativos
- Relatório de qualidade dos dados
- KPIs na página inicial (Total de Vendas, Pedidos, Lucro, Ticket Médio)

---

## Pré-requisitos

- Python 3.11+
- pip

---

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/superstore-analytics.git
cd superstore-analytics
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env`:

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-publica
TABLE_NAME=STREAMLIT
```

> As credenciais estão disponíveis no painel do Supabase em **Settings → API**.

### 4. Execute o app

```bash
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## Estrutura do Projeto

```
├── app.py                    # Página inicial: KPIs e visão geral
├── pages/
│   ├── 1_Perguntas_1_5.py   # Perguntas 1 a 5
│   └── 2_Perguntas_6_10.py  # Perguntas 6 a 10 + simulador de desconto
├── src/
│   ├── connection.py         # Carga de dados via REST API do Supabase
│   ├── processing.py         # Limpeza e transformações Pandas (Q1–Q10)
│   └── visualizations.py    # Funções de gráficos Plotly
├── .env.example              # Modelo de variáveis de ambiente (sem valores reais)
├── requirements.txt          # Dependências Python
└── docs/project-notes.md    # Notas internas de desenvolvimento
```

### Como os dados fluem

```
Supabase (REST API)
      ↓
connection.py → load_raw_data() [cache 1h]
      ↓
processing.py → clean_data() → apply_filters()
      ↓
processing.py → q1_*() ... q10_*()
      ↓
visualizations.py → bar_chart / pie_chart / line_chart
      ↓
Streamlit (app.py + pages/)
```

---

## Perguntas Respondidas

| # | Pergunta | Tipo de Visualização |
|---|----------|----------------------|
| 1 | Cidade com maior venda em Office Supplies | Tabela + Bar Chart |
| 2 | Total de vendas por data de pedido | Bar Chart |
| 3 | Total de vendas por estado | Bar Chart horizontal |
| 4 | Top N cidades por total de vendas | Bar Chart |
| 5 | Segmento com maior total de vendas | Pie Chart |
| 6 | Total de vendas por segmento e ano | Tabela pivot + Bar Chart agrupado |
| 7 | Simulação: quantas vendas recebem 15% de desconto? | Métrica + Pie Chart |
| 8 | Média de vendas antes e após desconto | Métricas + Bar Chart comparativo |
| 9 | Média de vendas por segmento, ano e mês | Line Chart |
| 10 | Vendas por categoria e top 12 subcategorias | Bar Chart agrupado |

---

## Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Streamlit | Interface web interativa |
| Pandas | Processamento e transformação de dados |
| Plotly Express | Visualizações interativas |
| Supabase | Banco de dados PostgreSQL na nuvem |
| python-dotenv | Gerenciamento seguro de credenciais |

---

## Segurança

- Credenciais **nunca** são commitadas no repositório
- `.env` está no `.gitignore`
- Apenas `.env.example` (sem valores reais) é versionado
