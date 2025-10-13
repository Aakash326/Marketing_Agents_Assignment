# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🧪 Optional: Test Before Running

Run the test suite to verify everything works:

```bash
python test_system.py
```

---

## 📋 What You Built

A multi-agent system with **4 AI agents** working together:

1. **Planner Agent** - Decides which agents to activate
2. **Portfolio Agent** - Analyzes client holdings
3. **Market Agent** - Fetches real-time prices and news
4. **Validator Agent** - Ensures response accuracy

---

## 🎯 Sample Queries to Try

- "What stocks do I own?"
- "What's the current price of NVDA?"
- "Which holding has the best return?"
- "How is Microsoft doing in my portfolio?"

---

## 📊 Available Clients

Select from: CLT-001, CLT-002, CLT-003, CLT-004, CLT-005, CLT-007, CLT-009, CLT-010

---

## 🛠 Troubleshooting

**"OPENAI_API_KEY not found"**
→ Create `.env` file with your API key

**"No module named 'langgraph'"**
→ Run `pip install -r requirements.txt`

**"Error loading portfolio"**
→ Ensure `portfolios.xlsx` is in the project root

---

## 📚 Learn More

See [README.md](README.md) for complete documentation.
