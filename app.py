import streamlit as st
import pandas as pd
import plotly.express as px
from classifier import classify_ticket
from utils import load_csv, detect_message_column, extract_tickets, group_by_category, get_summary_stats


def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background-color: #0f0f0f;
    }

    .block-container {
        padding-top: 4rem !important;
        max-width: 1100px;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #1e1e1e !important;
        min-width: 210px !important;
        max-width: 210px !important;
    }

    /* Sidebar nav buttons */
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #f0f0f0 !important;
        border: none !important;
        border-radius: 11px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: -0.2px !important;
        text-align: left !important;
        padding: 11px 16px !important;
        box-shadow: none !important;
        width: 100% !important;
        transition: color 0.2s, background 0.2s !important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(79,156,249,0.08) !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* ── TYPOGRAPHY ── */
    h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -1.5px !important;
        color: #f0f0f0 !important;
    }
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
        color: #f0f0f0 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #505050 !important;
        font-size: 13px !important;
    }

    /* ── METRICS ── */
    [data-testid="stMetric"] {
        background: #1c1c1c;
        border: 1px solid #252525;
        border-radius: 16px;
        padding: 20px 24px;
    }
    [data-testid="stMetricLabel"] {
        color: #909090 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    [data-testid="stMetricValue"] {
        color: #4f9cf9 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
    }

    /* ── BUTTONS ── */
    .stButton > button[kind="primary"] {
        background: #4f9cf9 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 12px 28px !important;
        box-shadow: 0 4px 24px rgba(79,156,249,0.25) !important;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.88 !important;
        box-shadow: 0 6px 32px rgba(79,156,249,0.35) !important;
    }

    /* Secondary buttons scoped to main only */
    .main .stButton > button,
    .main [data-testid="stBaseButton-secondary"] {
        background: #1c1c1c !important;
        color: #909090 !important;
        border: 1px solid #252525 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    .main .stButton > button:hover,
    .main [data-testid="stBaseButton-secondary"]:hover {
        border-color: #333 !important;
        color: #f0f0f0 !important;
    }

    /* ── EXPANDERS ── */
    [data-testid="stExpander"] {
        background: #1c1c1c !important;
        border: 1px solid #252525 !important;
        border-radius: 14px !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(79,156,249,0.25) !important;
    }

    /* ── INPUTS ── */
    [data-testid="stFileUploader"] {
        background: #161616 !important;
        border: 1px dashed #252525 !important;
        border-radius: 14px !important;
    }
    textarea {
        background: #161616 !important;
        border: 1px solid #252525 !important;
        border-radius: 12px !important;
        color: #f0f0f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background: #161616 !important;
        border: 1px solid #252525 !important;
        border-radius: 10px !important;
        color: #f0f0f0 !important;
    }

    /* ── TABS ── */
    [data-testid="stTabs"] [role="tab"] {
        font-weight: 500 !important;
        font-size: 13px !important;
        color: #505050 !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #4f9cf9 !important;
        border-bottom-color: #4f9cf9 !important;
    }
    [data-testid="stTabs"] [role="tabpanel"] {
        min-height: 300px !important;
    }

    /* ── MISC ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #252525 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    hr {
        border-color: #1e1e1e !important;
        margin: 1.5rem 0 !important;
    }
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background: rgba(79,156,249,0.1) !important;
        color: #4f9cf9 !important;
        border: 1px solid rgba(79,156,249,0.2) !important;
        border-radius: 100px !important;
        font-size: 12px !important;
    }
    [data-testid="stDownloadButton"] > button {
        background: #1c1c1c !important;
        color: #4f9cf9 !important;
        border: 1px solid rgba(79,156,249,0.25) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: rgba(79,156,249,0.08) !important;
        border-color: rgba(79,156,249,0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Triage Desk",
    page_icon="🎫",
    layout="wide"
)

apply_custom_styles()

# ── SESSION STATE ──
if "results" not in st.session_state:
    st.session_state.results = []
if "df" not in st.session_state:
    st.session_state.df = None
if "detected_column" not in st.session_state:
    st.session_state.detected_column = None
if "confirmed_column" not in st.session_state:
    st.session_state.confirmed_column = None
if "page" not in st.session_state:
    st.session_state.page = "Classify tickets"
if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
            <div style='
                padding: 20px 8px 20px 8px;
                border-bottom: 1px solid #1e1e1e;
                margin-bottom: 16px;
            '>
                <div style='
                    font-size: 26px;
                    font-weight: 700;
                    color: #f0f0f0;
                    letter-spacing: -1px;
                    line-height: 1.1;
                '>Triage Desk</div>
                <div style='
                    font-size: 12px;
                    color: #505050;
                    margin-top: 5px;
                '>AI ticket classifier</div>
            </div>
        """, unsafe_allow_html=True)

    for label in ["Classify tickets", "Bulk groups", "Insights"]:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()


# ── CLASSIFY PAGE ──
if st.session_state.page == "Classify tickets":
    st.title("Classify tickets")
    st.caption("Upload a CSV file or paste a single ticket to get started")
    st.divider()

    tab1, tab2 = st.tabs(["Upload CSV", "Paste a ticket"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=["csv"],
            help="Supports exports from Zendesk, Intercom, Excel, or any CSV format"
        )

        if uploaded_file:
            df, error = load_csv(uploaded_file)

            if error:
                st.error(error["error"])
            else:
                st.session_state.df = df
                file_name = uploaded_file.name

                if st.session_state.detected_column is None or st.session_state.last_file != file_name:
                    with st.spinner("Analysing your file..."):
                        detection = detect_message_column(df)
                        st.session_state.detected_column = detection
                        st.session_state.last_file = file_name

                detection = st.session_state.detected_column
                suggested_col = detection["column"]

                st.success(f"File loaded · {len(df)} rows detected")

                with st.expander("✓ Message field confirmed — expand to change", expanded=False):
                    st.caption(f"Message field identified: **{suggested_col}** · Use the dropdown below to change if needed")
                    confirmed = st.selectbox(
                        "Message field",
                        options=df.columns.tolist(),
                        index=df.columns.tolist().index(suggested_col),
                        label_visibility="collapsed"
                    )
                    st.dataframe(
                        df[[confirmed]].head(3),
                        use_container_width=True,
                        hide_index=True
                    )
                    st.session_state.confirmed_column = confirmed

                if st.session_state.confirmed_column is None:
                    st.session_state.confirmed_column = suggested_col

                st.divider()

                if st.button("Classify all tickets", type="primary", use_container_width=True):
                    tickets = extract_tickets(df, st.session_state.confirmed_column)
                    results = []
                    total_tickets = len(tickets)
                    progress = st.progress(0)
                    status = st.empty()
                    for i, ticket in enumerate(tickets):
                        tickets_remaining = total_tickets - i
                        seconds_remaining = tickets_remaining * 10
                        minutes = seconds_remaining // 60
                        seconds = seconds_remaining % 60
                        if minutes > 0:
                            time_str = f"{minutes}m {seconds}s remaining"
                        else:
                            time_str = f"{seconds}s remaining"
                        status.caption(f"Classifying ticket {i + 1} of {total_tickets} · {time_str}")
                        result = classify_ticket(ticket)
                        result["original_text"] = ticket
                        results.append(result)
                        progress.progress((i + 1) / total_tickets)
                    status.caption(f"Done · {total_tickets} tickets classified")
                    st.session_state.results = results
                    st.rerun()

    with tab2:
        ticket_input = st.text_area(
            "Paste your ticket here",
            height=150,
            placeholder="e.g. Hi, I haven't received my payslip for January and it's been three weeks..."
        )
        if st.button("Classify this ticket", type="primary"):
            if ticket_input.strip():
                with st.spinner("Classifying..."):
                    result = classify_ticket(ticket_input)
                    result["original_text"] = ticket_input
                    st.session_state.results = [result]
                    st.rerun()
            else:
                st.warning("Please enter some ticket text before classifying.")

    if st.session_state.results:
        results = st.session_state.results
        stats = get_summary_stats(results)

        st.divider()
        st.subheader("Results")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total tickets", stats["total"])
        col2.metric("High priority", stats["high"])
        col3.metric("Frustrated", stats["frustrated"])
        col4.metric("Errors", stats["errors"])

        st.divider()

        priority_filter = st.multiselect(
            "Filter by priority",
            options=["High", "Medium", "Low"],
            default=["High", "Medium", "Low"]
        )

        filtered = [r for r in results if "error" not in r and r.get("priority") in priority_filter]

        for i, result in enumerate(filtered):
            with st.expander(f"#{i+1} · {result.get('summary', 'No summary')} · {result.get('priority', '')}"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Category:** {result.get('category', 'N/A')}")
                c2.markdown(f"**Priority:** {result.get('priority', 'N/A')}")
                c3.markdown(f"**Sentiment:** {result.get('sentiment', 'N/A')}")
                st.markdown(f"**Suggested action:** {result.get('suggested_action', 'N/A')}")
                st.markdown(f"**Priority reason:** {result.get('priority_reason', 'N/A')}")
                st.markdown("**Original ticket:**")
                st.caption(result.get("original_text", ""))

        export_data = [{
            "summary": r.get("summary"),
            "category": r.get("category"),
            "priority": r.get("priority"),
            "priority_reason": r.get("priority_reason"),
            "sentiment": r.get("sentiment"),
            "suggested_action": r.get("suggested_action"),
            "original_text": r.get("original_text")
        } for r in results if "error" not in r]

        st.download_button(
            label="Export results as CSV",
            data=pd.DataFrame(export_data).to_csv(index=False),
            file_name="triage_results.csv",
            mime="text/csv"
        )


# ── BULK GROUPS PAGE ──
elif st.session_state.page == "Bulk groups":
    st.title("Bulk groups")
    st.caption("Tickets grouped by category — ideal for drafting a single reply to multiple similar tickets")
    st.divider()

    if not st.session_state.results:
        st.info("No results yet. Classify some tickets first.")
    else:
        groups = group_by_category(st.session_state.results)
        for category, tickets in groups.items():
            with st.expander(f"{category} · {len(tickets)} tickets"):
                for i, t in enumerate(tickets):
                    st.markdown(f"**{i+1}.** {t.get('original_text', '')}")
                    st.caption(f"Priority: {t.get('priority')} · Sentiment: {t.get('sentiment')} · Action: {t.get('suggested_action')}")
                    st.divider()


# ── INSIGHTS PAGE ──
elif st.session_state.page == "Insights":
    st.title("Insights")
    st.caption("A summary view of your classified tickets")
    st.divider()

    if not st.session_state.results:
        st.info("No results yet. Classify some tickets first.")
    else:
        valid = [r for r in st.session_state.results if "error" not in r]
        df_results = pd.DataFrame(valid)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Tickets by category")
            cat_counts = df_results["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig = px.bar(
                cat_counts, x="Category", y="Count",
                color="Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                showlegend=False,
                xaxis_tickangle=0,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="",
                yaxis_title="Tickets"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Tickets by priority")
            pri_counts = df_results["priority"].value_counts().reset_index()
            pri_counts.columns = ["Priority", "Count"]
            priority_colors = {"High": "#E05C5C", "Medium": "#E0A84B", "Low": "#5CB85C"}
            fig2 = px.bar(
                pri_counts, x="Priority", y="Count",
                color="Priority",
                color_discrete_map=priority_colors
            )
            fig2.update_layout(
                showlegend=False,
                xaxis_tickangle=0,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="",
                yaxis_title="Tickets"
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Tickets by sentiment")
        sent_counts = df_results["sentiment"].value_counts().reset_index()
        sent_counts.columns = ["Sentiment", "Count"]
        sentiment_colors = {"Frustrated": "#E05C5C", "Neutral": "#A0A0A0", "Positive": "#5CB85C"}
        fig3 = px.bar(
            sent_counts, x="Sentiment", y="Count",
            color="Sentiment",
            color_discrete_map=sentiment_colors
        )
        fig3.update_layout(
            showlegend=False,
            xaxis_tickangle=0,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis_title="",
            yaxis_title="Tickets"
        )
        st.plotly_chart(fig3, use_container_width=True)