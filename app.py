import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CropGuard AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7faf7;
    }

    section[data-testid="stSidebar"] {
        background-color: #102a1b;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #163a24;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 17px;
        color: #66736b;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e1e8e2;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .metric-label {
        color: #6b756e;
        font-size: 14px;
    }

    .metric-value {
        color: #173b24;
        font-size: 28px;
        font-weight: 750;
        margin-top: 5px;
    }

    .urgent-card {
        background: #fff5f3;
        border-left: 5px solid #d64545;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 12px;
    }

    .warning-card {
        background: #fff9eb;
        border-left: 5px solid #e4a72c;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 12px;
    }

    .safe-card {
        background: #effaf2;
        border-left: 5px solid #3c9b57;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 12px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #173b24;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h1 style="font-size:28px;">🌱 CropGuard AI</h1>
        <p style="color:#b8c9bd;">
        Severity-Triaged Crop Disease Advisory
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔬 Disease Detection",
            "🚜 Farm Fields",
            "📋 Treatment Plan",
            "📊 Analytics",
        ],
    )

    st.divider()

    st.markdown("### Farm Settings")

    budget = st.number_input(
        "Treatment Budget (₹)",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=500,
    )

    farm_area = st.number_input(
        "Total Farm Area (acres)",
        min_value=0.1,
        value=10.0,
        step=0.5,
    )

    st.divider()

    st.caption("HTH-CV-06 • AgriTech MVP")


# ============================================================
# SAMPLE DATA
# ============================================================

fields = pd.DataFrame(
    [
        {
            "Field": "F-01",
            "Crop": "Tomato",
            "Disease": "Early Blight",
            "Severity": "High",
            "Loss": 14700,
            "Treatment": 2200,
            "Spread": "High",
            "Action": "TREAT NOW",
        },
        {
            "Field": "F-02",
            "Crop": "Potato",
            "Disease": "Late Blight",
            "Severity": "Critical",
            "Loss": 18300,
            "Treatment": 2800,
            "Spread": "Critical",
            "Action": "TREAT NOW",
        },
        {
            "Field": "F-03",
            "Crop": "Tomato",
            "Disease": "Leaf Mold",
            "Severity": "Medium",
            "Loss": 6300,
            "Treatment": 1100,
            "Spread": "Medium",
            "Action": "TREAT",
        },
        {
            "Field": "F-04",
            "Crop": "Pepper",
            "Disease": "Bacterial Spot",
            "Severity": "Low",
            "Loss": 2100,
            "Treatment": 900,
            "Spread": "Low",
            "Action": "MONITOR",
        },
        {
            "Field": "F-05",
            "Crop": "Tomato",
            "Disease": "Early Blight",
            "Severity": "Medium",
            "Loss": 8200,
            "Treatment": 1700,
            "Spread": "Medium",
            "Action": "TREAT",
        },
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">Good morning, Farmer 👋</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Monitor crop health and prioritize treatment based on "
        "potential economic loss."
        "</div>",
        unsafe_allow_html=True,
    )

    # Metrics
    total_loss = fields["Loss"].sum()
    treatment_cost = fields["Treatment"].sum()

    critical_fields = len(
        fields[
            fields["Severity"].isin(["High", "Critical"])
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Fields Monitored</div>
                <div class="metric-value">{len(fields)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Fields Requiring Action</div>
                <div class="metric-value">{critical_fields}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Potential Loss</div>
                <div class="metric-value">₹{total_loss:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Treatment Budget</div>
                <div class="metric-value">₹{budget:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Priority alerts
    st.markdown(
        '<div class="section-title">🚨 Priority Alerts</div>',
        unsafe_allow_html=True,
    )

    alert1, alert2 = st.columns(2)

    with alert1:
        st.markdown(
            """
            <div class="urgent-card">
                <b>🔴 Critical: Field F-02</b><br><br>
                Potato Late Blight detected.<br>
                Estimated untreated loss: <b>₹18,300</b>.<br>
                Recommended action: <b>Treat today.</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with alert2:
        st.markdown(
            """
            <div class="warning-card">
                <b>🟠 High Risk: Field F-01</b><br><br>
                Tomato Early Blight detected.<br>
                Estimated untreated loss: <b>₹14,700</b>.<br>
                Recommended action: <b>Treat within 24 hours.</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Treatment queue
    st.markdown(
        '<div class="section-title">📋 Today\'s Treatment Queue</div>',
        unsafe_allow_html=True,
    )

    display = fields[
        [
            "Field",
            "Crop",
            "Disease",
            "Severity",
            "Loss",
            "Treatment",
            "Spread",
            "Action",
        ]
    ].copy()

    display["Loss"] = display["Loss"].apply(
        lambda x: f"₹{x:,.0f}"
    )

    display["Treatment"] = display["Treatment"].apply(
        lambda x: f"₹{x:,.0f}"
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DISEASE DETECTION
# ============================================================

elif page == "🔬 Disease Detection":

    st.markdown(
        '<div class="main-title">🔬 Disease Detection</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Upload a leaf image to detect disease and estimate severity."
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1])

    with left:

        uploaded_file = st.file_uploader(
            "Upload leaf image",
            type=["jpg", "jpeg", "png"],
        )

        if uploaded_file is not None:

            st.image(
                uploaded_file,
                caption="Uploaded leaf",
                use_container_width=True,
            )

    with right:

        if uploaded_file is not None:

            st.markdown(
                """
                <div class="metric-card">

                <h3>AI Diagnosis</h3>

                <p>
                <b>Crop</b><br>
                Tomato
                </p>

                <p>
                <b>Disease</b><br>
                Early Blight
                </p>

                <p>
                <b>Confidence</b><br>
                94.2%
                </p>

                <p>
                <b>Severity</b><br>
                🔴 High
                </p>

                <p>
                <b>Affected Area</b><br>
                38%
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.warning(
                "⚠️ AI prediction is currently using demo data. "
                "The trained disease model will be connected here next."
            )

        else:

            st.info(
                "Upload a leaf image to begin analysis."
            )

    # Economic impact
    st.markdown(
        '<div class="section-title">💰 Estimated Impact</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Yield at Risk",
            "1,620 kg",
        )

    with b:
        st.metric(
            "Potential Loss",
            "₹14,700",
        )

    with c:
        st.metric(
            "Treatment Cost",
            "₹2,200",
        )

    # Cost of delay
    st.markdown(
        '<div class="section-title">⏱ Cost of Delay</div>',
        unsafe_allow_html=True,
    )

    delay = pd.DataFrame(
        {
            "Delay": [
                "Today",
                "+1 Day",
                "+2 Days",
                "+3 Days",
            ],
            "Estimated Loss": [
                14700,
                16905,
                19440,
                22356,
            ],
        }
    )

    st.line_chart(
        delay.set_index("Delay")
    )


# ============================================================
# FARM FIELDS
# ============================================================

elif page == "🚜 Farm Fields":

    st.markdown(
        '<div class="main-title">🚜 Farm Fields</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Overview of disease status across all monitored fields."
        "</div>",
        unsafe_allow_html=True,
    )

    st.dataframe(
        fields,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        '<div class="section-title">Disease Distribution</div>',
        unsafe_allow_html=True,
    )

    disease_counts = fields["Disease"].value_counts()

    st.bar_chart(
        disease_counts
    )


# ============================================================
# TREATMENT PLAN
# ============================================================

elif page == "📋 Treatment Plan":

    st.markdown(
        '<div class="main-title">📋 Treatment Plan</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Budget-aware treatment prioritization."
        "</div>",
        unsafe_allow_html=True,
    )

    sorted_fields = fields.sort_values(
        "Loss",
        ascending=False,
    )

    for _, row in sorted_fields.iterrows():

        if row["Action"] == "TREAT NOW":

            st.markdown(
                f"""
                <div class="urgent-card">
                    <h4>🔴 {row["Field"]} — {row["Crop"]}</h4>

                    <b>Disease:</b> {row["Disease"]}<br>
                    <b>Severity:</b> {row["Severity"]}<br>
                    <b>Potential Loss:</b> ₹{row["Loss"]:,.0f}<br>
                    <b>Treatment Cost:</b> ₹{row["Treatment"]:,.0f}<br>
                    <b>Spread Risk:</b> {row["Spread"]}<br><br>

                    <b>Recommendation: TREAT NOW</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif row["Action"] == "TREAT":

            st.markdown(
                f"""
                <div class="warning-card">
                    <h4>🟠 {row["Field"]} — {row["Crop"]}</h4>

                    <b>Disease:</b> {row["Disease"]}<br>
                    <b>Severity:</b> {row["Severity"]}<br>
                    <b>Potential Loss:</b> ₹{row["Loss"]:,.0f}<br>
                    <b>Treatment Cost:</b> ₹{row["Treatment"]:,.0f}<br>
                    <b>Spread Risk:</b> {row["Spread"]}<br><br>

                    <b>Recommendation: TREAT SOON</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
                <div class="safe-card">
                    <h4>🟢 {row["Field"]} — {row["Crop"]}</h4>

                    <b>Disease:</b> {row["Disease"]}<br>
                    <b>Severity:</b> {row["Severity"]}<br>
                    <b>Potential Loss:</b> ₹{row["Loss"]:,.0f}<br><br>

                    <b>Recommendation: MONITOR</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">📊 Farm Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Economic impact and disease severity overview."
        "</div>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Potential Loss by Field")

        loss_chart = fields.set_index("Field")["Loss"]

        st.bar_chart(
            loss_chart
        )

    with c2:

        st.subheader("Severity Distribution")

        severity_chart = fields["Severity"].value_counts()

        st.bar_chart(
            severity_chart
        )

    st.subheader("Farm Summary")

    total_loss = fields["Loss"].sum()
    total_treatment = fields["Treatment"].sum()

    st.write(
        f"**Total estimated untreated loss:** ₹{total_loss:,.0f}"
    )

    st.write(
        f"**Total treatment requirement:** ₹{total_treatment:,.0f}"
    )

    st.write(
        f"**Available budget:** ₹{budget:,.0f}"
    )

    if total_treatment <= budget:

        st.success(
            "Current budget can cover the simulated treatment plan."
        )

    else:

        st.warning(
            "Current budget is insufficient for all simulated treatments. "
            "Prioritization is required."
        )