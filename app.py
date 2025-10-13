"""
Streamlit UI for Portfolio & Market Intelligence System.
"""

import streamlit as st
from src.graph.workflow import run_workflow

# Page configuration
st.set_page_config(
    page_title="Portfolio & Market Intelligence System",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Portfolio & Market Intelligence System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    # Client selection
    client_options = [
        "CLT-001",
        "CLT-002",
        "CLT-003",
        "CLT-004",
        "CLT-005",
        "CLT-007",
        "CLT-009",
        "CLT-010"
    ]

    selected_client = st.selectbox(
        "Select Client",
        options=client_options,
        index=0
    )

    st.markdown("---")

    # System info
    st.subheader("About This System")
    st.markdown("""
    This multi-agent AI system uses **LangGraph** to orchestrate four specialized agents:

    **🎯 Planner Agent**
    - Analyzes queries and determines which agents to activate

    **💼 Portfolio Agent**
    - Analyzes client holdings and portfolio composition

    **📈 Market Agent**
    - Fetches real-time stock prices and news

    **✅ Validator Agent**
    - Validates responses for accuracy and data grounding
    """)

    st.markdown("---")

    st.subheader("Sample Queries")
    st.markdown("""
    - "What stocks do I own?"
    - "What's the current price of NVDA?"
    - "Which of my holdings has the best return?"
    - "How is Microsoft doing in my portfolio?"
    - "What's my total portfolio value?"
    """)

# Main area
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Ask a question about your portfolio or the market:",
        placeholder="e.g., What stocks do I own?",
        key="query_input"
    )

with col2:
    st.write("")  # Spacing
    submit_button = st.button("Submit", type="primary", use_container_width=True)

# Process query
if submit_button and query:
    with st.spinner("Analyzing your query... 🤔"):
        try:
            # Run the workflow
            result = run_workflow(query, selected_client)

            # Display response
            st.markdown("### 💡 Response")
            st.markdown(result.get("response", "No response generated."))

            # Show which agents were activated
            with st.expander("🔍 View Agent Activity"):
                st.markdown("**Planning Decision:**")
                st.text(result.get("plan", "No plan generated."))

                col_a, col_b = st.columns(2)

                with col_a:
                    if result.get("needs_portfolio"):
                        st.success("✅ Portfolio Agent Activated")
                    else:
                        st.info("⏭️ Portfolio Agent Skipped")

                with col_b:
                    if result.get("needs_market"):
                        st.success("✅ Market Agent Activated")
                    else:
                        st.info("⏭️ Market Agent Skipped")

                st.markdown("**Validation:**")
                if result.get("validated"):
                    st.success("✅ Response Validated")
                else:
                    st.warning("⚠️ Response Not Validated")

            # Show raw data (optional)
            with st.expander("📊 View Raw Data"):
                if result.get("portfolio_data"):
                    st.markdown("**Portfolio Data:**")
                    st.json(result["portfolio_data"])

                if result.get("market_data"):
                    st.markdown("**Market Data:**")
                    st.json(result["market_data"])

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

elif submit_button:
    st.warning("Please enter a query.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by LangGraph, OpenAI GPT-4o-mini, and yfinance</p>
</div>
""", unsafe_allow_html=True)
