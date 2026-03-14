import streamlit as st
from backend import scan_ports

st.set_page_config(page_title="CyberShield AI", layout="centered")

st.title("🛡️ CyberShield AI Security Scanner")

st.write("Enter a website or IP address to scan for open ports.")

host = st.text_input("Enter Website or IP Address")

if st.button("Run Scan"):

    if host:
        with st.spinner("Scanning ports... Please wait"):

            result = scan_ports(host)

            st.subheader("Scan Result")

            st.write("Target:", result["host"])
            st.write("Open Ports:", result["open_ports"])
            st.write("Risk Score:", result["risk_score"])
            st.write("Security Grade:", result["grade"])

            if result["grade"] == "High Risk":
                st.error("⚠️ High Vulnerability Detected")

            elif result["grade"] == "Medium Risk":
                st.warning("⚠️ Medium Risk Found")

            elif result["grade"] == "Invalid Host":
                st.error("Invalid website or IP address")

            else:
                st.success("✅ System Appears Secure")

    else:
        st.warning("Please enter a valid host")
