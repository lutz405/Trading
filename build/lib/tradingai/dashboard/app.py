from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from tradingai.paper.broker import PaperBroker


def load_broker(state_path: str = "data/paper_state.json") -> PaperBroker:
    return PaperBroker.load(state_path)


def equity_dataframe(broker: PaperBroker) -> pd.DataFrame:
    if not broker.trades:
        return pd.DataFrame(columns=["timestamp", "equity"])
    rows = []
    cap = broker.capital
    for t in broker.trades:
        rows.append({"pnl": t["pnl"]})
    df = pd.DataFrame(rows)
    df["cumulative"] = df["pnl"].cumsum()
    return df


def candlestick_figure(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"], open=df["open"], high=df["high"], low=df["low"], close=df["close"]
    )])
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
    return fig


def main() -> None:
    st.set_page_config(page_title="TradingAI_BTC", layout="wide")
    st.title("TradingAI_BTC - Paper Trading")
    broker = load_broker()
    st.sidebar.header("Navegación")
    page = st.sidebar.radio("Sección", ["Overview", "Market", "Paper Trading", "Risk", "Backtesting", "Logs"])

    if page == "Overview":
        st.metric("Capital virtual", f"{broker.capital:.2f}")
        st.metric("Posiciones abiertas", len(broker.positions))
        st.metric("Operaciones", len(broker.trades))
    elif page == "Market":
        st.write("Carga datos históricos con scripts/download_data.py")
    elif page == "Paper Trading":
        st.dataframe(pd.DataFrame(broker.trades) if broker.trades else pd.DataFrame())
        st.dataframe(pd.DataFrame([{"side": p.side, "entry": p.entry_price, "qty": p.qty} for p in broker.positions]))
    elif page == "Risk":
        st.write("Límites configurados en config/risk.yaml")
    elif page == "Backtesting":
        st.write("Ejecuta backtesting desde scripts (Stage 6).")
    elif page == "Logs":
        st.write("Logs en monitoring/ (si existen).")


if __name__ == "__main__":
    main()
