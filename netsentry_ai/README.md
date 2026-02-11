# NetSentry AI 🛡️

NetSentry AI is a real-time network threat detection dashboard powered by AI. It simulates network traffic, detects anomalies (like SYN Floods and Port Scans), and uses an AI Agent to explain the threats in plain English.

## 🚀 How to Run (Step-by-Step)

Follow these exact steps to get the application running on your machine.

### 1. Open your Terminal
Open your command prompt (cmd.exe), PowerShell, or Terminal.

### 2. Navigate to the project folder
Type the following command and press **Enter**:
```bash
cd netsentry_ai
```

### 3. Install Dependencies
Type the following command and press **Enter**:
```bash
pip install -r requirements.txt
```
*(Wait for the installation to finish. You should see "Successfully installed..." at the end.)*

### 4. Run the Dashboard
Type the following command and press **Enter**:
```bash
streamlit run app.py
```

### 5. Open in Browser
After running the command, you will see a URL like `http://localhost:8501`.
*   Copy and paste this URL into your web browser (Chrome, Firefox, etc.).
*   OR hold **Ctrl** (or **Cmd**) and click the link in the terminal.

---

## 🎮 How to Use the Dashboard

Once the dashboard is open:

1.  **Start Simulation:** Look at the left sidebar. Click the button that says **"Start/Stop Simulation"**. You will see the charts start moving!
2.  **Trigger an Attack:** In the sidebar, click the yellow **"⚠️ Trigger SYN Flood"** button.
    *   Watch the "Packets per Second" chart spike.
    *   Look at the "AI Analyst Insight" panel on the right to see the AI explain the attack.
3.  **Chat with AI:** Scroll down to the "Chat with NetSentry" box. Type "Is my network safe?" and press **Enter**.

---

## 🔧 AI Configuration (Optional)
By default, the app runs in **Mock Mode** (simulated AI) so it works instantly without setup.
If you have **Ollama** installed locally:
1.  Run `ollama run llama3` in a separate terminal.
2.  In the NetSentry dashboard sidebar, change "LLM Model" to **Llama3 (Local)**.
