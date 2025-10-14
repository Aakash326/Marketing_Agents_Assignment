"""
Streamlit UI for Portfolio & Market Intelligence System.
Enhanced with session management and clarification features.
"""

import streamlit as st
from src.graph.workflow import run_workflow


def init_session_state(client_id):
    """Initialize session state for conversation history"""
    history_key = f'history_{client_id}'
    if history_key not in st.session_state:
        st.session_state[history_key] = []


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

    # Clear history button
    if st.button("🗑️ Clear Conversation History", use_container_width=True):
        history_key = f'history_{selected_client}'
        st.session_state[history_key] = []
        st.success("History cleared!")

    st.markdown("---")

    # System info
    st.subheader("About This System")
    st.markdown("""
    This multi-agent AI system uses **LangGraph** to orchestrate five specialized agents:

    **🎯 Planner Agent**
    - Analyzes queries and determines which agents to activate

    **💼 Portfolio Agent**
    - Analyzes client holdings and portfolio composition

    **📈 Market Agent**
    - Fetches real-time stock prices, news, SEC filings, and RAG context

    **🤝 Collaboration Agent**
    - Synthesizes portfolio + market insights for complex queries

    **✅ Validator Agent**
    - Validates responses and requests clarification when needed
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

    st.markdown("---")

    st.subheader("🆕 New Features")
    st.markdown("""
    **Conversation Memory**
    Ask follow-up questions! System remembers last 5 interactions.

    **Smart Clarification**
    System asks for clarification on ambiguous queries.

    **Enhanced Collaboration**
    Complex queries automatically trigger synthesis agent.

    **SEC Filings & RAG**
    Answers enriched with SEC filing risk factors and knowledge base.
    """)

# Main area

# Initialize session state
if selected_client:
    init_session_state(selected_client)
    history_key = f'history_{selected_client}'

    # Show conversation history
    if len(st.session_state[history_key]) > 0:
        with st.expander(f"📜 Conversation History ({len(st.session_state[history_key])//2} interactions)"):
            history = st.session_state[history_key]
            # Display in reverse (most recent first)
            for i in range(len(history)-1, -1, -2):
                if i-1 >= 0:
                    user_msg = history[i-1]["content"]
                    asst_msg = history[i]["content"]
                    st.markdown(f"**You:** {user_msg[:200]}{'...' if len(user_msg) > 200 else ''}")
                    st.markdown(f"**Assistant:** {asst_msg[:200]}{'...' if len(asst_msg) > 200 else ''}")
                    st.markdown("---")

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
            # Get conversation history
            conversation_history = st.session_state[history_key]

            # Run the workflow with history
            result = run_workflow(query, selected_client, conversation_history)

            # Check if clarification is needed (Feature 5)
            if result.get("needs_clarification"):
                st.warning("🤔 Clarification Needed")
                st.info(result.get("clarification_message", "Please clarify your query."))

                # Show clarification input
                with st.form("clarification_form"):
                    clarification = st.text_input(
                        "Your clarification:",
                        placeholder="e.g., AAPL, best by return, past month"
                    )
                    clarify_button = st.form_submit_button("Submit Clarification")

                    if clarify_button and clarification:
                        # Rerun with enhanced query
                        enhanced_query = f"{query} ({clarification})"
                        result = run_workflow(enhanced_query, selected_client, conversation_history)

                        # Process result normally if no longer needs clarification
                        if not result.get("needs_clarification"):
                            # Display response
                            st.markdown("### 💡 Response")
                            st.markdown(result["response"])

                            # Add to history
                            conversation_history.append({"role": "user", "content": enhanced_query})
                            conversation_history.append({"role": "assistant", "content": result["response"]})
                            st.session_state[history_key] = conversation_history[-10:]  # Keep last 5 Q&A pairs

            else:
                # No clarification needed - display response
                st.markdown("### 💡 Response")
                st.markdown(result.get("response", "No response generated."))

                # Add to conversation history (Feature 4)
                conversation_history.append({"role": "user", "content": query})
                conversation_history.append({"role": "assistant", "content": result["response"]})

                # Keep only last 5 Q&A pairs (10 messages)
                st.session_state[history_key] = conversation_history[-10:]

            # Show which agents were activated
            with st.expander("🔍 View Agent Activity"):
                st.markdown("**Planning Decision:**")
                st.text(result.get("plan", "No plan generated."))

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    if result.get("needs_portfolio"):
                        st.success("✅ Portfolio Agent")
                    else:
                        st.info("⏭️ Portfolio Agent")

                with col_b:
                    if result.get("needs_market"):
                        st.success("✅ Market Agent")
                    else:
                        st.info("⏭️ Market Agent")

                with col_c:
                    if result.get("collaboration_findings"):
                        st.success("✅ Collaboration Agent")
                        collab = result["collaboration_findings"]
                        st.caption(f"Synthesized {collab.get('portfolio_holdings_analyzed', 0)} holdings with {collab.get('market_data_points', 0)} market data points")
                    else:
                        st.info("⏭️ Collaboration Agent")

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
