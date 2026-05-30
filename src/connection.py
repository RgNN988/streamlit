import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
TABLE_NAME = os.environ.get("TABLE_NAME", "STREAMLIT")


def _get_headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


def _fetch_page(offset: int, limit: int = 1000) -> list:
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    params = {"select": "*", "limit": limit, "offset": offset}
    resp = requests.get(url, headers=_get_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=3600, show_spinner="Carregando dados do Supabase...")
def load_raw_data() -> pd.DataFrame:
    all_rows = []
    offset = 0
    limit = 1000
    while True:
        page = _fetch_page(offset, limit)
        if not page:
            break
        all_rows.extend(page)
        if len(page) < limit:
            break
        offset += limit
    return pd.DataFrame(all_rows)
