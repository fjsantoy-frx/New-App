import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from traffic_generator import TrafficGenerator
from ai_agent import NetSentryAgent

# Page Config
st.set_page_config(
    page_title="NetSentry AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = pd.DataFrame({
        "Timestamp": pd.Series(dtype='datetime64[ns]'),
        "Source": pd.Series(dtype='str'),
        "Destination": pd.Series(dtype='str'),
        "Protocol": pd.Series(dtype='str'),
        "Length": pd.Series(dtype='int'),
        "Flags": pd.Series(dtype='str'),
        "Info": pd.Series(dtype='str')
    })

if 'generator' not in st.session_state:
    st.session_state.generator = TrafficGenerator()

if 'agent' not in st.session_state:
    st.session_state.agent = NetSentryAgent()

if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False

if 'ai_analysis' not in st.session_state:
    st.session_state.ai_analysis = "System initialized. Monitoring network traffic..."

def update_data():
    """Generates new traffic and appends to session state."""
    new_packets = st.session_state.generator.generate_batch(random.randint(5, 15))
    df_new = pd.DataFrame(new_packets)
    st.session_state.traffic_data = pd.concat([st.session_state.traffic_data, df_new], ignore_index=True).tail(1000) # Keep last 1000

def trigger_attack(attack_type):
    """Injects attack traffic."""
    if attack_type == "SYN Flood":
        packets = st.session_state.generator.generate_dos_attack("192.168.1.100")
        analysis = st.session_state.agent.analyze_traffic("High volume of SYN packets detected (Potential SYN Flood).")
    elif attack_type == "Port Scan":
        packets = st.session_state.generator.generate_port_scan("192.168.1.50")
        analysis = st.session_state.agent.analyze_traffic("Sequential port connection attempts detected (Potential Port Scan).")

    df_attack = pd.DataFrame(packets)
    st.session_state.traffic_data = pd.concat([st.session_state.traffic_data, df_attack], ignore_index=True).tail(1000)
    st.session_state.ai_analysis = analysis

# --- UI Layout ---

# Sidebar
st.sidebar.title("🛡️ NetSentry Control")
st.sidebar.markdown("---")

# Simulation Controls
st.sidebar.subheader("Simulation Status")
if st.sidebar.button("Start/Stop Simulation"):
    st.session_state.simulation_running = not st.session_state.simulation_running

status_text = "🟢 Running" if st.session_state.simulation_running else "🔴 Stopped"
st.sidebar.markdown(f"**Status:** {status_text}")

st.sidebar.markdown("---")
st.sidebar.subheader("Attack Simulation")
if st.sidebar.button("⚠️ Trigger SYN Flood"):
    trigger_attack("SYN Flood")
if st.sidebar.button("⚠️ Trigger Port Scan"):
    trigger_attack("Port Scan")

st.sidebar.markdown("---")
st.sidebar.subheader("AI Configuration")
model_option = st.sidebar.selectbox("LLM Model", ["Mock Mode (Sandbox)", "Llama3 (Local)", "Mistral (Local)"])
if model_option == "Mock Mode (Sandbox)":
    st.session_state.agent.set_mock_mode(True)
else:
    st.session_state.agent.set_mock_mode(False)
    st.session_state.agent.model_name = model_option.split(" ")[0].lower()


# Main Dashboard
st.title("🛡️ NetSentry AI Analyst")
st.markdown("### Real-time Network Threat Detection System")

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

# Calculate Metrics
df = st.session_state.traffic_data
total_packets = len(df)
unique_ips = df['Source'].nunique()
# Simple heuristic for "threats"
threat_count = df[df['Info'].str.contains("ALERT", na=False)].shape[0]
avg_packet_size = df['Length'].mean() if not df.empty else 0

col1.metric("Total Packets Captured", f"{total_packets}")
col2.metric("Active Source IPs", f"{unique_ips}")
col3.metric("Threats Detected", f"{threat_count}", delta_color="inverse")
col4.metric("Avg Packet Size", f"{avg_packet_size:.0f} bytes")

# Charts and Data
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Traffic Volume (Real-time)")
    if not df.empty:
        # Resample by second to show volume
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df_chart = df.set_index('Timestamp').resample('1S').count()
        fig = px.area(df_chart, y='Source', title="Packets per Second", labels={'Source': 'Packet Count'})
        fig.update_layout(xaxis_title="Time", yaxis_title="Packets", template="plotly_dark", height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Waiting for data...")

with col_chart2:
    st.subheader("Protocol Distribution")
    if not df.empty:
        fig_pie = px.pie(df, names='Protocol', title="Protocol Breakdown", hole=0.4)
        fig_pie.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Waiting for data...")

st.markdown("---")

col_details, col_ai = st.columns([2, 1])

with col_details:
    st.subheader("Recent Packet Logs")
    st.dataframe(
        df.tail(20)[["Timestamp", "Source", "Destination", "Protocol", "Length", "Info"]],
        use_container_width=True,
        hide_index=True
    )

with col_ai:
    st.subheader("🤖 AI Analyst Insight")
    st.info(st.session_state.ai_analysis)

    st.markdown("---")
    st.subheader("Chat with NetSentry")
    user_input = st.text_input("Ask about the network status:", placeholder="Is there any danger?")
    if user_input:
        response = st.session_state.agent.chat(user_input, context_data=df.tail(20).to_string())
        st.write(f"**AI:** {response}")

# Auto-refresh logic
if st.session_state.simulation_running:
    update_data()
    time.sleep(1)
    st.rerun()
