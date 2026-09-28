import pandas as pd
import plotly.express as px
import streamlit as st

from price_tracker.storage.mongo_store import MongoStore

st.set_page_config(page_title="Price Tracker", layout="wide")
st.title("Price Tracker Dashboard")


@st.cache_resource
def get_store() -> MongoStore:
    return MongoStore()


store = get_store()

symbols = sorted(store.prices.distinct("symbol"))
if not symbols:
    st.info("No data yet. Start the poller first: "
            "`python -m price_tracker.cli run --symbols bitcoin`")
    st.stop()

# --- sidebar controls ---
symbol = st.sidebar.selectbox("Symbol", symbols)
limit = st.sidebar.slider("Data points", 50, 1000, 200, step=50)
st.sidebar.button("Refresh")  # any click reruns the script, re-reading Atlas

# --- price history ---
history = store.get_price_history(symbol, limit=limit)
df = pd.DataFrame([p.model_dump() for p in history]).sort_values("fetched_at")

latest, first = df.iloc[-1], df.iloc[0]
change_pct = (latest.price - first.price) / first.price * 100

c1, c2, c3 = st.columns(3)
c1.metric("Latest price", f"{latest.price:,.2f} {latest.currency}", f"{change_pct:+.2f}% over window")
c2.metric("Data points", len(df))
c3.metric("Last updated (UTC)", f"{latest.fetched_at:%Y-%m-%d %H:%M:%S}")

fig = px.line(df, x="fetched_at", y="price", color="source", markers=True,
              labels={"fetched_at": "Time (UTC)", "price": "Price"})
st.plotly_chart(fig)

# --- alert log ---
st.subheader("Alert log")
alerts = store.get_alert_log(limit=100)
if alerts:
    st.dataframe(
        pd.DataFrame([{
            "time": a.triggered_at,
            "symbol": a.symbol,
            "condition": a.rule.condition,
            "threshold": a.rule.threshold,
            "price": a.triggered_price,
            "message": a.message,
        } for a in alerts]),
        hide_index=True,
    )
else:
    st.caption("No alerts have fired yet.")