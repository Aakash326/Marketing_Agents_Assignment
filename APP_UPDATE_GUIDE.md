# app.py Update Guide - Session Management & Clarification UI

## Overview

This guide shows what to add to `app.py` to enable:
- Session management (Feature 4)
- Clarification requests (Feature 5)
- History display

## Key Changes Needed

### 1. Initialize Session State (Add after imports)

```python
# Initialize session state for conversation history
def init_session_state(client_id):
    """Initialize session state for a client"""
    history_key = f'history_{client_id}'
    clarification_key = f'awaiting_clarification_{client_id}'

    if history_key not in st.session_state:
        st.session_state[history_key] = []

    if clarification_key not in st.session_state:
        st.session_state[clarification_key] = False
```

### 2. Add Clear History Button (In sidebar)

```python
# In sidebar, after client selection:
if st.sidebar.button("🗑️ Clear Conversation History"):
    history_key = f'history_{selected_client}'
    st.session_state[history_key] = []
    st.success("History cleared!")
```

### 3. Update Query Processing (Replace existing processing)

```python
# After submit button click:
if submit_button and query:
    # Initialize session state
    init_session_state(selected_client)
    history_key = f'history_{selected_client}'

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

                        # Process result normally (fall through to display)
                        if not result.get("needs_clarification"):
                            # Add to history
                            conversation_history.append({"role": "user", "content": enhanced_query})
                            conversation_history.append({"role": "assistant", "content": result["response"]})
                            st.session_state[history_key] = conversation_history[-10:]  # Keep last 5 Q&A pairs

                            # Display response
                            st.markdown("### 💡 Response")
                            st.markdown(result["response"])

            else:
                # No clarification needed - display response
                st.markdown("### 💡 Response")
                st.markdown(result.get("response", "No response generated."))

                # Add to conversation history (Feature 4)
                conversation_history.append({"role": "user", "content": query})
                conversation_history.append({"role": "assistant", "content": result["response"]})

                # Keep only last 5 Q&A pairs (10 messages)
                st.session_state[history_key] = conversation_history[-10:]

            # Show agent activity (existing code can stay)
            with st.expander("🔍 View Agent Activity"):
                # ... existing agent activity display ...

                # Add collaboration indicator
                if result.get("collaboration_findings"):
                    st.success("🤝 Collaboration Agent Activated")
                    collab = result["collaboration_findings"]
                    st.text(f"Synthesized {collab.get('portfolio_holdings_analyzed', 0)} holdings with {collab.get('market_data_points', 0)} market data points")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)
```

### 4. Add Conversation History Display (Before main query area)

```python
# After client selection, before query input:
if selected_client:
    history_key = f'history_{selected_client}'
    if history_key in st.session_state and len(st.session_state[history_key]) > 0:
        with st.expander("📜 Conversation History (Click to view)"):
            history = st.session_state[history_key]

            st.caption(f"Showing last {len(history)//2} interactions")

            # Display in reverse (most recent first)
            for i in range(len(history)-1, -1, -2):
                if i-1 >= 0:
                    user_msg = history[i-1]["content"]
                    asst_msg = history[i]["content"]

                    st.markdown(f"**You:** {user_msg[:150]}{'...' if len(user_msg) > 150 else ''}")
                    st.markdown(f"**Assistant:** {asst_msg[:150]}{'...' if len(asst_msg) > 150 else ''}")
                    st.markdown("---")
```

### 5. Update Sidebar Info (Add feature explanations)

```python
# In sidebar, after system info:
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
Answers enriched with SEC filing risk factors and knowledge base context.
""")
```

## Complete Code Template

Here's a minimal working template with all features:

```python
import streamlit as st
from src.graph.workflow import run_workflow

st.set_page_config(page_title="Portfolio Intelligence", page_icon="📊", layout="wide")

# Initialize session state
def init_session_state(client_id):
    history_key = f'history_{client_id}'
    if history_key not in st.session_state:
        st.session_state[history_key] = []

# Title
st.title("📊 Portfolio & Market Intelligence System")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    # Client selection
    client_options = ["CLT-001", "CLT-002", "CLT-003", "CLT-004", "CLT-005", "CLT-007", "CLT-009", "CLT-010"]
    selected_client = st.selectbox("Select Client", options=client_options, index=0)

    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state[f'history_{selected_client}'] = []
        st.success("History cleared!")

    st.markdown("---")
    st.subheader("About")
    st.markdown("Multi-agent AI system with 5 advanced features...")

# Main area - Show history
if selected_client:
    init_session_state(selected_client)
    history_key = f'history_{selected_client}'

    if len(st.session_state[history_key]) > 0:
        with st.expander(f"📜 Conversation History ({len(st.session_state[history_key])//2} interactions)"):
            for i in range(len(st.session_state[history_key])-1, -1, -2):
                if i-1 >= 0:
                    st.markdown(f"**You:** {st.session_state[history_key][i-1]['content'][:150]}...")
                    st.markdown(f"**Assistant:** {st.session_state[history_key][i]['content'][:150]}...")
                    st.markdown("---")

# Query input
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("Ask a question:", placeholder="e.g., What stocks do I own?")
with col2:
    st.write("")
    submit_button = st.button("Submit", type="primary", use_container_width=True)

# Process query
if submit_button and query:
    with st.spinner("Analyzing... 🤔"):
        try:
            conversation_history = st.session_state[history_key]
            result = run_workflow(query, selected_client, conversation_history)

            # Check clarification
            if result.get("needs_clarification"):
                st.warning("🤔 " + result.get("clarification_message", ""))
                clarification = st.text_input("Please clarify:")
                if st.button("Submit Clarification") and clarification:
                    enhanced_query = f"{query} ({clarification})"
                    result = run_workflow(enhanced_query, selected_client, conversation_history)

            if not result.get("needs_clarification"):
                # Display response
                st.markdown("### 💡 Response")
                st.markdown(result["response"])

                # Update history
                conversation_history.append({"role": "user", "content": query})
                conversation_history.append({"role": "assistant", "content": result["response"]})
                st.session_state[history_key] = conversation_history[-10:]

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Powered by LangGraph + OpenAI GPT-4o-mini</p>", unsafe_allow_html=True)
```

## Testing the Updates

After updating app.py:

1. **Test Session Management**:
   ```
   Query 1: "What stocks do I own?"
   Query 2: "Tell me about the first one"
   → Should work with context
   ```

2. **Test Clarification**:
   ```
   Query: "How's that stock doing?"
   → Should ask for clarification
   ```

3. **Test Collaboration**:
   ```
   Query: "How does Microsoft news affect my portfolio?"
   → Should show collaboration in agent activity
   ```

4. **Test History Display**:
   ```
   - Make multiple queries
   - Check history expander
   - Click "Clear History"
   ```

## Summary

Key additions to app.py:
- ✅ Session state initialization
- ✅ Conversation history display
- ✅ Clarification UI
- ✅ History management (clear button)
- ✅ Pass history to workflow

All backend features are complete - just need these UI updates!
