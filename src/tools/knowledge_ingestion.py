"""
Ingest data into knowledge base.
Run this script to populate the knowledge base with SEC filings.
"""

from src.tools.rag_tools import SimpleKnowledgeBase
from src.tools.sec_tools import fetch_latest_filing
from src.tools.portfolio_tools import load_portfolio_data
import time


def ingest_portfolio_sec_filings(client_id: str):
    """
    Ingest SEC filings for all stocks in a client's portfolio.

    Args:
        client_id: Client ID (e.g., 'CLT-001')
    """
    kb = SimpleKnowledgeBase()

    # Load client portfolio
    portfolio = load_portfolio_data("portfolios.xlsx", client_id)

    if "holdings" not in portfolio:
        print(f"No holdings found for {client_id}")
        return

    # Get unique tickers
    tickers = set()
    for holding in portfolio["holdings"]:
        ticker = holding["symbol"]
        if ticker.upper() != "CASH":
            tickers.add(ticker)

    print(f"Ingesting SEC filings for {len(tickers)} stocks...")

    # Fetch and store SEC filings
    success_count = 0
    for ticker in tickers:
        print(f"Fetching 10-K for {ticker}...")
        filing = fetch_latest_filing(ticker, "10-K")

        if filing.get("success"):
            doc_id = f"sec_{ticker}_10K"
            metadata = {
                "type": "sec_filing",
                "ticker": ticker,
                "filing_type": "10-K",
                "client_id": client_id
            }

            success = kb.add_document(
                text=filing["text"],
                metadata=metadata,
                doc_id=doc_id
            )

            if success:
                print(f"  ✓ Stored {ticker} 10-K")
                success_count += 1
            else:
                print(f"  ✗ Failed to store {ticker}")
        else:
            print(f"  ✗ Failed to fetch {ticker}: {filing.get('error')}")

        time.sleep(2)  # Be nice to SEC servers

    stats = kb.get_stats()
    print(f"\nKnowledge base now has {stats['total_documents']} documents")
    print(f"Successfully ingested {success_count}/{len(tickers)} SEC filings")


def ingest_multiple_clients(client_ids: list):
    """
    Ingest SEC filings for multiple clients.

    Args:
        client_ids: List of client IDs
    """
    for client in client_ids:
        print(f"\n{'='*60}")
        print(f"Processing {client}")
        print('='*60)
        ingest_portfolio_sec_filings(client)


def get_knowledge_base_stats():
    """Get and display knowledge base statistics"""
    kb = SimpleKnowledgeBase()
    stats = kb.get_stats()

    print("\n" + "="*60)
    print("Knowledge Base Statistics")
    print("="*60)
    print(f"Collection: {stats['collection_name']}")
    print(f"Total Documents: {stats['total_documents']}")
    print("="*60)


if __name__ == "__main__":
    # Ingest for one client to test
    print("Starting knowledge base ingestion...")
    ingest_portfolio_sec_filings("CLT-001")

    # Show stats
    get_knowledge_base_stats()
