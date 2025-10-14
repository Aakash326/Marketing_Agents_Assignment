"""
Run this to populate the knowledge base with SEC filings.
Usage: python ingest_knowledge.py
"""

from src.tools.knowledge_ingestion import (
    ingest_portfolio_sec_filings,
    ingest_multiple_clients,
    get_knowledge_base_stats
)
import sys


def main():
    print("\n" + "="*70)
    print("KNOWLEDGE BASE INGESTION TOOL")
    print("="*70)
    print("\nThis script will download SEC 10-K filings for portfolio holdings")
    print("and store them in a vector database for semantic search.\n")

    # Check if user wants to ingest specific clients or all
    if len(sys.argv) > 1:
        clients = sys.argv[1:]
        print(f"Ingesting for specific clients: {', '.join(clients)}\n")
    else:
        # Default: ingest for CLT-001 only (for testing)
        clients = ["CLT-001"]
        print(f"Ingesting for default client: CLT-001")
        print("(To ingest for multiple clients, run: python ingest_knowledge.py CLT-001 CLT-002 ...)\n")

    # Run ingestion
    try:
        for client in clients:
            ingest_portfolio_sec_filings(client)

        # Show final stats
        print("\n" + "="*70)
        get_knowledge_base_stats()
        print("="*70)

        print("\n✅ Ingestion complete!")
        print("\nThe knowledge base is now ready for use in the application.")
        print("Run: streamlit run app.py\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion interrupted by user")
        print("Partial data may have been stored.")
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
