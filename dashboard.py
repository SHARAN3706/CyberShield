import streamlit as st
from backend import scan_ports, PORT_LABELS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberShield AI Security Scanner",
    page_icon="🛡️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Dark cyber background */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a1628 100%);
        color: #e0e6f0;
    }

    /* Title styling */
    h1 {
        font-family: 'Courier New', monospace !important;
        color: #00d4ff !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        letter-spacing: 2px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #7a9db8;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        margin-top: -10px;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* Result card */
    .result-card {
        background: rgba(0, 20, 40, 0.8);
        border: 1px solid #00d4ff33;
        border-radius: 10px;
        padding: 20px 28px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 24px rgba(0, 212, 255, 0.08);
    }

    .result-label {
        color: #7a9db8;
        font-size: 0.78rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .result-value {
        color: #e0e6f0;
        font-size: 1.15rem;
        font-weight: bold;
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.4rem;
    }

    /* Port pill */
    .port-pill {
        display: inline-block;
        background: rgba(0, 212, 255, 0.12);
        border: 1px solid #00d4ff55;
        color: #00d4ff;
        border-radius: 6px;
        padding: 3px 10px;
        margin: 3px 4px;
        font-size: 0.85rem;
        font-family: 'Courier New', monospace;
    }

    .port-pill-none {
        color: #4a8a6a;
        font-style: italic;
    }

    /* Divider */
    .cyber-divider {
        border: none;
        border-top: 1px solid #00d4ff22;
        margin: 20px 0;
    }

    /* Input label */
    label {
        color: #7a9db8 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🛡️ CyberShield AI Security Scanner")
st.markdown(
    '<p class="subtitle">▸ NETWORK VULNERABILITY ASSESSMENT TOOL ◂</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="cyber-divider">', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
target = st.text_input(
    "TARGET HOST",
    placeholder="e.g. example.com  or  192.168.1.1",
    help="Enter a domain name or IP address to scan",
)

col_btn, col_spacer = st.columns([1, 3])
with col_btn:
    run_scan = st.button("⚡ Run Scan", use_container_width=True)

# ── Scan logic ────────────────────────────────────────────────────────────────
if run_scan:
    if not target.strip():
        st.warning("⚠️  Please enter a website or IP address before scanning.")
    else:
        with st.spinner("🔍  Scanning target — please wait..."):
            try:
                result = scan_ports(target.strip())
            except ValueError as exc:
                st.error(f"❌  {exc}")
                st.stop()
            except Exception as exc:
                st.error(f"❌  Unexpected error: {exc}")
                st.stop()

        # ── Results dashboard ────────────────────────────────────────────────
        st.markdown('<hr class="cyber-divider">', unsafe_allow_html=True)
        st.markdown("### 📊 Scan Results")

        # Row 1 – Target / Resolved IP
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">Target</div>
                    <div class="result-value">{target.strip()}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">Resolved IP</div>
                    <div class="result-value">{result["host"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Row 2 – Risk Score / Grade
        grade = result["grade"]
        score = result["risk_score"]

        grade_color = {
            "High Risk":   "#ff4b4b",
            "Medium Risk": "#ffa500",
            "Low Risk":    "#21c97a",
        }.get(grade, "#e0e6f0")

        c3, c4 = st.columns(2)
        with c3:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">Risk Score</div>
                    <div class="result-value" style="color:{grade_color};font-size:2rem;">
                        {score} / 96
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">Security Grade</div>
                    <div class="result-value" style="color:{grade_color};font-size:1.5rem;">
                        {grade}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Open ports
        open_ports = result["open_ports"]
        if open_ports:
            pills_html = " ".join(
                f'<span class="port-pill">{p} <span style="opacity:.6;font-size:.75rem;">({PORT_LABELS.get(p, "?")})</span></span>'
                for p in open_ports
            )
        else:
            pills_html = '<span class="port-pill-none">No open ports detected</span>'

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Open Ports ({len(open_ports)} found)</div>
                <div style="margin-top:8px;">{pills_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Visual alert ─────────────────────────────────────────────────────
        st.markdown("")
        if grade == "High Risk":
            st.error(
                f"🚨 **HIGH RISK** — {len(open_ports)} open port(s) detected.  "
                "Immediate hardening is strongly recommended. "
                "Close unused ports and review firewall rules."
            )
        elif grade == "Medium Risk":
            st.warning(
                f"⚠️ **MEDIUM RISK** — {len(open_ports)} open port(s) detected.  "
                "Review exposed services and apply security patches."
            )
        else:
            st.success(
                f"✅ **LOW RISK** — Only {len(open_ports)} open port(s) detected.  "
                "The host appears well-secured. Continue monitoring regularly."
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="cyber-divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#3a5a7a;font-family:\'Courier New\',monospace;'
    'font-size:0.75rem;">CyberShield AI • For authorized security assessments only</p>',
    unsafe_allow_html=True,
)
