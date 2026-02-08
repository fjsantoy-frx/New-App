import requests
import json
import random

class NetSentryAgent:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"
        self.mock_mode = True  # Default to True for sandbox environment

    def set_mock_mode(self, enabled: bool):
        self.mock_mode = enabled

    def _generate_mock_response(self, prompt):
        """Generates a realistic sounding AI response based on keywords in the prompt."""
        prompt_lower = prompt.lower()

        if ("syn" in prompt_lower and "flood" in prompt_lower) or ("syn" in prompt_lower and "high volume" in prompt_lower):
            return (
                "**ALERT: SYN Flood Attack Detected**\n\n"
                "I have analyzed the traffic patterns and detected an abnormally high volume of TCP SYN packets "
                "originating from a single external IP address. This indicates a **SYN Flood Denial-of-Service (DoS)** attack.\n\n"
                "**Recommendations:**\n"
                "1. Block the offending source IP immediately at the firewall.\n"
                "2. Enable SYN cookies on the server to mitigate half-open connection exhaustion.\n"
                "3. Monitor bandwidth usage for further spikes."
            )
        elif "port scan" in prompt_lower:
             return (
                "**ALERT: Port Scan Activity Detected**\n\n"
                "My analysis shows a sequential series of connection attempts to multiple ports on your target machine. "
                "This is a classic **Port Scan**, likely a reconnaissance phase preceding a targeted attack.\n\n"
                "**Recommendations:**\n"
                "1. Identify the source IP and add it to the blocklist.\n"
                "2. Ensure all unnecessary ports are closed.\n"
                "3. Review system logs for any successful login attempts during this timeframe."
            )
        elif "udp" in prompt_lower:
            return (
                "**Observation: UDP Traffic Spike**\n\n"
                "I noticed a significant amount of UDP traffic. While often used for streaming or DNS, sudden spikes "
                "can indicate UDP Floods or amplification attacks. Please verify the source."
            )
        else:
            return (
                "**Status: Normal**\n\n"
                "I have reviewed the recent traffic logs. The patterns appear consistent with normal network activity. "
                "No anomalies or known attack signatures were detected at this time."
            )

    def analyze_traffic(self, traffic_data_summary):
        """
        Sends traffic summary to the LLM for analysis.
        """
        prompt = f"""
        You are a Cybersecurity Analyst AI named NetSentry.
        Analyze the following network traffic summary and identify any potential threats.
        Be concise and professional.

        Traffic Summary:
        {traffic_data_summary}
        """

        if self.mock_mode:
            return self._generate_mock_response(traffic_data_summary)

        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.ollama_url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json().get("response", "Error: No response from model.")

        except requests.exceptions.RequestException as e:
            # Fallback if local LLM is down
            return f"**Connection Error:** Could not connect to Local LLM at {self.ollama_url}. \n\n(Ensure Ollama is running or switch to Mock Mode.)"

    def chat(self, user_question, context_data=""):
        """
        Allows the user to ask questions about the traffic.
        """
        prompt = f"""
        Context: The user is asking about network traffic. Here is the recent data: {context_data}

        User Question: {user_question}

        Answer as a helpful security analyst.
        """

        if self.mock_mode:
            # Simple keyword matching for chat in mock mode
            if "danger" in user_question.lower() or "threat" in user_question.lower():
                return "Based on current logs, the highest threat level was detected during the recent SYN Flood. No active threats right now."
            elif "ip" in user_question.lower():
                return "I track IPs from both internal (192.168.x.x) and external sources. Check the 'Top Source IP' metric for the most active one."
            else:
                return "I am monitoring the network. You can ask me about specific threats, IPs, or protocols."

        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(self.ollama_url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json().get("response", "Error: No response from model.")
        except:
             return "I'm having trouble connecting to my brain (Ollama). Please check the connection."
