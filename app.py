"""
Streamlit UI for Portfolio & Market Intelligence System.
Enhanced with session management, clarification features, and portfolio analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
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

# Portfolio Analytics Dashboard
st.markdown("---")
st.header("📈 Portfolio Analytics Dashboard")

@st.cache_data
def load_portfolio_data():
    """Load portfolio data from Excel file"""
    try:
        df = pd.read_excel('portfolios.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading portfolio data: {str(e)}")
        return None

# Load data
portfolio_df = load_portfolio_data()

if portfolio_df is not None and selected_client:
    # Filter data for selected client
    client_data = portfolio_df[portfolio_df['client_id'] == selected_client].copy()

    if len(client_data) > 0:
        # Calculate portfolio metrics
        client_data['market_value'] = client_data['quantity'] * client_data['Purchase Price']
        total_value = client_data['market_value'].sum()
        num_holdings = len(client_data)

        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Portfolio Value",
                value=f"${total_value:,.2f}"
            )

        with col2:
            st.metric(
                label="Number of Holdings",
                value=num_holdings
            )

        with col3:
            unique_sectors = client_data['sector'].nunique()
            st.metric(
                label="Sectors",
                value=unique_sectors
            )

        with col4:
            unique_asset_classes = client_data['asset_class'].nunique()
            st.metric(
                label="Asset Classes",
                value=unique_asset_classes
            )

        st.markdown("---")

        # Create visualizations
        viz_col1, viz_col2 = st.columns(2)

        with viz_col1:
            # Asset Class Allocation Pie Chart
            st.subheader("Asset Class Allocation")
            asset_allocation = client_data.groupby('asset_class')['market_value'].sum().reset_index()
            asset_allocation['percentage'] = (asset_allocation['market_value'] / total_value * 100).round(2)

            fig_asset = px.pie(
                asset_allocation,
                values='market_value',
                names='asset_class',
                title=f'Portfolio Composition by Asset Class',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig_asset.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(fig_asset, use_container_width=True)

        with viz_col2:
            # Sector Allocation Pie Chart
            st.subheader("Sector Allocation")
            sector_allocation = client_data.groupby('sector')['market_value'].sum().reset_index()
            sector_allocation['percentage'] = (sector_allocation['market_value'] / total_value * 100).round(2)

            fig_sector = px.pie(
                sector_allocation,
                values='market_value',
                names='sector',
                title=f'Portfolio Composition by Sector',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            fig_sector.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(fig_sector, use_container_width=True)

        # Holdings Breakdown Bar Chart
        st.subheader("Holdings Breakdown")
        holdings_sorted = client_data.sort_values('market_value', ascending=False)

        fig_holdings = go.Figure()
        fig_holdings.add_trace(go.Bar(
            x=holdings_sorted['symbol'],
            y=holdings_sorted['market_value'],
            text=holdings_sorted['market_value'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside',
            marker=dict(
                color=holdings_sorted['market_value'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Value ($)")
            ),
            hovertemplate='<b>%{x}</b><br>Market Value: $%{y:,.2f}<br>Shares: %{customdata[0]}<br>Price: $%{customdata[1]:.2f}<extra></extra>',
            customdata=holdings_sorted[['quantity', 'Purchase Price']].values
        ))

        fig_holdings.update_layout(
            title=f'Holdings Value Distribution - {selected_client}',
            xaxis_title='Stock Symbol',
            yaxis_title='Market Value ($)',
            showlegend=False,
            height=500,
            hovermode='x'
        )

        st.plotly_chart(fig_holdings, use_container_width=True)

        # Detailed Holdings Table
        st.subheader("Detailed Holdings")

        # Prepare display dataframe
        display_df = client_data[['symbol', 'security_name', 'asset_class', 'sector', 'quantity', 'Purchase Price', 'market_value', 'purchase_date']].copy()
        display_df['percentage'] = (display_df['market_value'] / total_value * 100).round(2)
        display_df = display_df.sort_values('market_value', ascending=False)

        # Format columns
        display_df['Purchase Price'] = display_df['Purchase Price'].apply(lambda x: f'${x:.2f}')
        display_df['market_value'] = display_df['market_value'].apply(lambda x: f'${x:,.2f}')
        display_df['percentage'] = display_df['percentage'].apply(lambda x: f'{x}%')
        display_df['purchase_date'] = pd.to_datetime(display_df['purchase_date']).dt.strftime('%Y-%m-%d')

        # Rename columns for display
        display_df.columns = ['Symbol', 'Security Name', 'Asset Class', 'Sector', 'Shares', 'Purchase Price', 'Market Value', 'Purchase Date', 'Portfolio %']

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(f"No portfolio data found for {selected_client}")
else:
    if portfolio_df is None:
        st.warning("Unable to load portfolio data. Please ensure portfolios.xlsx exists.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by LangGraph, OpenAI GPT-4o-mini, and yfinance</p>
</div>
""", unsafe_allow_html=True)
