import streamlit as st
from classifier import classify_ticket
from utils import load_csv, detect_message_column, extract_tickets, group_by_category, get_summary_stats

st.set_page_config(
    page_title="Triage Desk",
    page_icon="🎫",
    layout="wide"
)

if "results" not in st.session_state:
    st.session_state.results = []
if "df" not in st.session_state:
    st.session_state.df = None
if "detected_column" not in st.session_state:
    st.session_state.detected_column = None
if "confirmed_column" not in st.session_state:
    st.session_state.confirmed_column = None

with st.sidebar:
    st.markdown("## 🎫 Triage Desk")
    st.markdown("AI-powered support ticket classifier")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Classify tickets", "Bulk groups", "Insights"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("Model: Gemini 1.5 Flash")
    st.caption("Free tier · ready")

if page == "Classify tickets":
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
                if st.session_state.detected_column is None or st.session_state.get("last_file") != file_name:
                    with st.spinner("Analysing your file..."):
                        detection = detect_message_column(df)
                        st.session_state.detected_column = detection
                        st.session_state.last_file = file_name

                detection = st.session_state.detected_column
                suggested_col = detection["column"]

                st.success(f"File loaded · {len(df)} rows detected")

                with st.expander("Review message field", expanded=True):
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

                st.divider()
                if st.button("Classify all tickets", type="primary", use_container_width=True):
                    tickets = extract_tickets(df, st.session_state.confirmed_column)
                    results = []
                    total_tickets = len(tickets)
                    est_minutes = round((total_tickets * 10) / 60, 1)
                    progress = st.progress(0, text=f"Classifying tickets — estimated time: {est_minutes} minutes...")
                    for i, ticket in enumerate(tickets):
                        result = classify_ticket(ticket)
                        result["original_text"] = ticket
                        results.append(result)
                        progress.progress((i + 1) / len(tickets), text=f"Classifying ticket {i + 1} of {len(tickets)}...")
                    st.session_state.results = results
                    st.success(f"Done · {len(results)} tickets classified")
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

        import pandas as pd
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

elif page == "Bulk groups":
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

elif page == "Insights":
    st.title("Insights")
    st.caption("A summary view of your classified tickets")
    st.divider()

    if not st.session_state.results:
        st.info("No results yet. Classify some tickets first.")
    else:
        import pandas as pd
        import plotly.express as px

        valid = [r for r in st.session_state.results if "error" not in r]
        df_results = pd.DataFrame(valid)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Tickets by category")
            cat_counts = df_results["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig = px.bar(cat_counts, x="Category", y="Count",
                        color="Category", color_discrete_sequence=px.colors.qualitative.Pastel)
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
            fig2 = px.bar(pri_counts, x="Priority", y="Count",
                         color="Priority", color_discrete_map=priority_colors)
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
        fig3 = px.bar(sent_counts, x="Sentiment", y="Count",
                     color="Sentiment", color_discrete_map=sentiment_colors)
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