# Notas de Desenvolvimento — Superstore Analytics

## Stack Técnico
- Python 3.11+
- Streamlit (multipage: app.py + pages/)
- Pandas para processamento (sem supabase-py — usar REST API via requests)
- Plotly Express para todos os gráficos
- python-dotenv para .env

## Variáveis de Ambiente Necessárias
Configure no arquivo `.env` (nunca commitar):
```
SUPABASE_URL=<url do projeto no painel Supabase>
SUPABASE_KEY=<chave anon do painel Supabase → Settings → API>
TABLE_NAME=STREAMLIT
```

## Colunas da Tabela STREAMLIT (9.994 linhas)
| Coluna         | Tipo original | Observação                              |
|----------------|---------------|-----------------------------------------|
| Row ID         | int           |                                         |
| Order ID       | str           | ex: 'CA-2016-152156'                    |
| Order Date     | str           | formato DD/MM/YYYY                      |
| Ship Date      | str           | formato DD/MM/YYYY                      |
| Ship Mode      | str           |                                         |
| Customer ID    | str           |                                         |
| Customer Name  | str           |                                         |
| Segment        | str           | Consumer / Corporate / Home Office      |
| Country        | str           | United States                           |
| City           | str           |                                         |
| State          | str           |                                         |
| Postal Code    | int           |                                         |
| Region         | str           | South / West / Central / East           |
| Product ID     | str           |                                         |
| Category       | str           | Furniture / Office Supplies / Technology|
| Sub-Category   | str           | hífen no nome!                          |
| Product Name   | str           |                                         |
| Sales          | str           | vírgula como decimal → .replace(',','.').astype(float) |
| Quantity       | int           |                                         |
| Discount       | str           | vírgula como decimal → mesmo tratamento |
| Profit         | str           | vírgula como decimal → mesmo tratamento |

## Conversões Críticas em processing.py
```python
for col in ['Sales', 'Discount', 'Profit']:
    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
```

## Estratégia de Carga dos Dados
- Usar REST API do Supabase diretamente com `requests`
- Carregar tudo com paginação (limit=1000, offset incremental) até esgotar
- Aplicar filtros no Pandas (não no Supabase) para simplicidade
- `@st.cache_data(ttl=3600)` em `load_data()`

## Padrões do Projeto
1. Credenciais sempre via `os.environ` — nunca hardcodadas
2. `@st.cache_data` em toda função de carga
3. Todos os gráficos via Plotly Express (interativo)
4. Interface em Português BR
5. Cada pergunta: resultado numérico/tabela + gráfico + insight textual
6. Filtros do sidebar filtram todas as perguntas via `session_state`

## Restrições
- Não ler CSV local no app final
- Não commitar `.env`
- Não misturar lógica de query com visualização
