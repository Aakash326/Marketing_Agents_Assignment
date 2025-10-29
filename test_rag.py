#!/usr/bin/env python3
"""
RAG System Testing and Validation Script

Tests the complete RAG pipeline with various queries to validate
accuracy, relevance, and response quality.

Usage:
    python test_rag.py                    # Run all tests
    python test_rag.py --interactive      # Interactive query mode
    python test_rag.py --category basics  # Test specific category
"""

import argparse
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_system.pipeline import RAGPipeline
from rag_system import config


def test_basic_queries():
    """Test basic stock market concept queries."""
    print("=" * 80)
    print("TEST 1: BASIC STOCK MARKET CONCEPTS")
    print("=" * 80)

    rag = RAGPipeline()

    test_queries = [
        {
            'question': 'What is a P/E ratio?',
            'expected_terms': ['price', 'earnings', 'share', 'valuation']
        },
        {
            'question': 'Explain market capitalization',
            'expected_terms': ['shares', 'outstanding', 'value', 'company']
        },
        {
            'question': 'What is EPS?',
            'expected_terms': ['earnings', 'per', 'share', 'profit']
        }
    ]

    results = []

    for i, test in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{test['question']}'")

        response = rag.query(test['question'], k=3)

        # Check for expected terms
        answer_lower = response.answer.lower()
        found_terms = [term for term in test['expected_terms'] if term in answer_lower]

        accuracy = len(found_terms) / len(test['expected_terms'])

        print(f"   Answer: {response.answer[:200]}...")
        print(f"   Sources: {len(response.sources)}")
        print(f"   Processing time: {response.processing_time:.2f}s")
        print(f"   Term coverage: {len(found_terms)}/{len(test['expected_terms'])} ({'✅' if accuracy >= 0.5 else '⚠️'})")

        results.append({
            'query': test['question'],
            'accuracy': accuracy,
            'processing_time': response.processing_time,
            'num_sources': len(response.sources)
        })

    # Summary
    avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
    avg_time = sum(r['processing_time'] for r in results) / len(results)

    print(f"\n{'=' * 80}")
    print("SUMMARY:")
    print(f"  Average term coverage: {avg_accuracy*100:.1f}%")
    print(f"  Average processing time: {avg_time:.2f}s")
    print(f"  Status: {'✅ PASS' if avg_accuracy >= 0.6 else '❌ FAIL'}")
    print("=" * 80)


def test_category_queries():
    """Test queries across different categories."""
    print("\n" + "=" * 80)
    print("TEST 2: CATEGORY-SPECIFIC QUERIES")
    print("=" * 80)

    rag = RAGPipeline()

    category_tests = {
        'valuation': 'How do you calculate price-to-book ratio?',
        'strategies': 'What is value investing?',
        'terminology': 'What is the difference between a bull and bear market?',
        'economics': 'How does inflation affect stock prices?',
        'risk': 'What is beta in stock market?'
    }

    for category, question in category_tests.items():
        print(f"\nCategory: {category}")
        print(f"Question: '{question}'")

        response = rag.search_by_category(question, category, k=3)

        print(f"   Answer: {response.answer[:150]}...")
        print(f"   Sources: {len(response.sources)}")
        print(f"   Time: {response.processing_time:.2f}s")

    print("\n" + "=" * 80)


def test_retrieval_quality():
    """Test retrieval relevance and quality."""
    print("\n" + "=" * 80)
    print("TEST 3: RETRIEVAL QUALITY")
    print("=" * 80)

    rag = RAGPipeline()

    query = "What financial metrics should I look at when evaluating a stock?"

    print(f"\nQuery: '{query}'")
    print("\nRetrieved Documents:")

    response = rag.query(query, k=5)

    for i, doc in enumerate(response.retrieved_docs, 1):
        metadata = doc.get('metadata', {})
        score = doc.get('score', 0)

        print(f"\n  {i}. Category: {metadata.get('category', 'unknown')}")
        print(f"     Source: {metadata.get('source', 'unknown')}")
        print(f"     Relevance: {score:.3f} ({'✅' if score >= 0.7 else '⚠️' if score >= 0.5 else '❌'})")
        print(f"     Preview: {doc['text'][:100]}...")

    avg_score = sum(doc['score'] for doc in response.retrieved_docs) / len(response.retrieved_docs)

    print(f"\nAverage relevance score: {avg_score:.3f}")
    print(f"Status: {'✅ PASS' if avg_score >= 0.6 else '⚠️ MARGINAL' if avg_score >= 0.4 else '❌ FAIL'}")

    print("=" * 80)


def test_source_attribution():
    """Test source citation accuracy."""
    print("\n" + "=" * 80)
    print("TEST 4: SOURCE ATTRIBUTION")
    print("=" * 80)

    rag = RAGPipeline()

    query = "What is dividend yield?"

    print(f"\nQuery: '{query}'")

    response = rag.get_answer_with_sources(query, k=3)

    print(f"\nAnswer:\n{response['answer']}")

    print(f"\nSources ({len(response['sources'])}):")
    for i, source in enumerate(response['sources'], 1):
        print(f"  {i}. {source}")

    has_sources = len(response['sources']) > 0
    print(f"\nSource attribution: {'✅ PASS' if has_sources else '❌ FAIL'}")

    print("=" * 80)


def test_response_time():
    """Test response time performance."""
    print("\n" + "=" * 80)
    print("TEST 5: RESPONSE TIME PERFORMANCE")
    print("=" * 80)

    rag = RAGPipeline()

    queries = [
        "What is a stock?",
        "Explain P/E ratio",
        "What are assets and liabilities?",
        "How does diversification work?",
        "What is market volatility?"
    ]

    times = []

    print("\nTesting response times for 5 queries...\n")

    for i, query in enumerate(queries, 1):
        response = rag.query(query, k=3)
        times.append(response.processing_time)
        print(f"  {i}. {query[:40]:<40} {response.processing_time:.2f}s")

    avg_time = sum(times) / len(times)
    max_time = max(times)

    print(f"\nAverage time: {avg_time:.2f}s")
    print(f"Max time: {max_time:.2f}s")
    print(f"Status: {'✅ PASS' if avg_time < 5.0 else '⚠️ SLOW' if avg_time < 10.0 else '❌ TOO SLOW'}")

    print("=" * 80)


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n" + "=" * 80)
    print("TEST 6: EDGE CASES")
    print("=" * 80)

    rag = RAGPipeline()

    edge_cases = [
        ("", "Empty query"),
        ("asdfghjkl zxcvbnm qwerty", "Nonsense query"),
        ("What is cryptocurrency blockchain NFT?", "Out-of-domain query"),
        ("x" * 1000, "Very long query"),
    ]

    print("\nTesting edge cases...\n")

    for i, (query, description) in enumerate(edge_cases, 1):
        print(f"{i}. {description}")
        print(f"   Query: '{query[:50]}{'...' if len(query) > 50 else ''}'")

        try:
            response = rag.query(query, k=3)
            has_answer = len(response.answer) > 0
            print(f"   Result: {'✅ Handled' if has_answer else '⚠️ Empty response'}")
        except Exception as e:
            print(f"   Result: ❌ Error: {str(e)[:50]}...")

    print("\n" + "=" * 80)


def interactive_mode():
    """Interactive query mode."""
    print("=" * 80)
    print("INTERACTIVE QUERY MODE")
    print("=" * 80)

    rag = RAGPipeline()

    print("\nInitialized RAG system. Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            question = input("📊 Ask a question: ").strip()

            if not question:
                continue

            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            print()

            response = rag.query(question, k=5)

            print(f"💬 Answer:\n{response.answer}\n")

            if response.sources:
                print(f"📚 Sources:")
                for i, source in enumerate(response.sources, 1):
                    print(f"  {i}. {source}")

            print(f"\n⏱️  Response time: {response.processing_time:.2f}s")
            print(f"📊 Documents used: {len(response.retrieved_docs)}")
            print()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def test_all():
    """Run all tests."""
    print("\n" + "=" * 80)
    print(" " * 20 + "RAG SYSTEM VALIDATION TESTS")
    print("=" * 80)

    # Check if knowledge base exists
    rag = RAGPipeline()
    stats = rag.get_stats()

    if stats.get('total_documents', 0) == 0:
        print("\n❌ Knowledge base is empty!")
        print("Run 'python rag_system/ingest_knowledge.py' first to populate the knowledge base.")
        return 1

    print(f"\nKnowledge base: {stats.get('total_documents', 0)} documents")
    print("=" * 80)

    # Run tests
    test_basic_queries()
    test_category_queries()
    test_retrieval_quality()
    test_source_attribution()
    test_response_time()
    test_edge_cases()

    print("\n" + "=" * 80)
    print(" " * 25 + "✅ ALL TESTS COMPLETE")
    print("=" * 80 + "\n")

    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test and validate the RAG system"
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive query mode'
    )

    parser.add_argument(
        '--category',
        type=str,
        help='Test a specific category only'
    )

    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run only quick tests (skip slow ones)'
    )

    args = parser.parse_args()

    try:
        if args.interactive:
            interactive_mode()
        elif args.category:
            print(f"Testing category: {args.category}")
            rag = RAGPipeline()
            response = rag.search_by_category(
                f"Tell me about {args.category}",
                args.category,
                k=5
            )
            print(f"\nAnswer:\n{response.answer}")
            print(f"\nSources: {len(response.sources)}")
        else:
            return test_all()

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
