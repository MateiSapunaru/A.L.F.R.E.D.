import requests
import streamlit as st

API_URL = "http://localhost:8000"


def api_get(path: str) -> dict:
    try:
        r = requests.get(f"{API_URL}{path}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def api_post(path: str, payload: dict | None = None, timeout: int = 60) -> dict:
    try:
        r = requests.post(f"{API_URL}{path}", json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


st.set_page_config(page_title="A.L.F.R.E.D.", page_icon="🎩", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Status")
    health = api_get("/")
    if "error" in health:
        st.error(f"Backend unreachable — is `uvicorn alfred.main:app` running?\n\n{health['error']}")
    else:
        st.success(health.get("status", "online"))

    st.divider()
    st.header("Preferences")
    prefs = api_get("/preferences")
    if isinstance(prefs, dict) and "error" not in prefs:
        if prefs:
            for k, v in prefs.items():
                st.caption(f"**{k}**: {v}")
        else:
            st.caption("None saved yet.")
    with st.form("pref_form", clear_on_submit=True):
        pk = st.text_input("Key")
        pv = st.text_input("Value")
        if st.form_submit_button("Save preference") and pk and pv:
            api_post("/preference", {"key": pk, "value": pv})
            st.rerun()

    st.divider()
    st.header("Memories")
    mems = api_get("/memories")
    if isinstance(mems, dict) and "memories" in mems:
        for m in mems["memories"]:
            st.caption(f"- {m.get('content', '')}")
    with st.form("mem_form", clear_on_submit=True):
        mem_text = st.text_input("Teach Alfred something")
        if st.form_submit_button("Save memory") and mem_text:
            api_post("/memory", {"text": mem_text})
            st.rerun()

st.title("🎩 A.L.F.R.E.D.")
st.caption("Text chat talks to the FastAPI backend directly. Voice mode records/speaks on whatever machine is running that backend.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Say something to Alfred...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = api_post("/chat", {"text": prompt}, timeout=180)
        reply = result.get("response") or result.get("error", "Something went wrong.")
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
if st.button("🎤 Talk (records 5s on the server)"):
    with st.spinner("Listening..."):
        result = api_post("/listen", timeout=30)
    if "you" in result:
        st.session_state.messages.append({"role": "user", "content": result["you"]})
        st.session_state.messages.append({"role": "assistant", "content": result["alfred"]})
        st.rerun()
    else:
        st.warning(result.get("status", result.get("error", "No input detected.")))
