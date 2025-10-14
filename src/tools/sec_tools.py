"""
SEC filings tools for fetching and analyzing company filings.
Keep it SIMPLE - just fetch text, no complex parsing.
"""

from sec_edgar_downloader import Downloader
import os
from typing import Dict, Optional


def fetch_latest_filing(ticker: str, filing_type: str = "10-K") -> Dict:
    """
    Fetch the latest SEC filing for a company.

    Args:
        ticker: Stock ticker symbol
        filing_type: Type of filing ("10-K", "10-Q", "8-K")

    Returns:
        Dictionary with filing text and metadata
    """
    try:
        # Download filing
        dl = Downloader("PortfolioIntelligence", "contact@example.com", "sec_filings")
        dl.get(filing_type, ticker, limit=1)

        # Read the filing text
        filing_path = f"sec_filings/sec-edgar-filings/{ticker}/{filing_type}"

        # Find the most recent filing folder
        if os.path.exists(filing_path):
            folders = os.listdir(filing_path)
            if folders:
                latest = sorted(folders)[-1]
                filing_file = f"{filing_path}/{latest}/full-submission.txt"

                if os.path.exists(filing_file):
                    with open(filing_file, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()

                    return {
                        "ticker": ticker,
                        "filing_type": filing_type,
                        "text": text[:50000],  # First 50k chars to avoid huge docs
                        "success": True
                    }

        return {
            "ticker": ticker,
            "filing_type": filing_type,
            "error": "Filing not found",
            "success": False
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "filing_type": filing_type,
            "error": str(e),
            "success": False
        }


def extract_risk_factors(filing_text: str) -> str:
    """
    Simple extraction of risk factors section from filing.
    Just search for "Risk Factors" section.
    """
    try:
        # Find risk factors section
        start_markers = ["RISK FACTORS", "Risk Factors", "ITEM 1A"]
        end_markers = ["ITEM 1B", "ITEM 2", "Unresolved Staff Comments"]

        text_upper = filing_text.upper()

        start_idx = -1
        for marker in start_markers:
            idx = text_upper.find(marker.upper())
            if idx != -1:
                start_idx = idx
                break

        if start_idx == -1:
            return "Risk factors section not found in filing."

        # Find end of risk factors
        end_idx = len(filing_text)
        for marker in end_markers:
            idx = text_upper.find(marker.upper(), start_idx + 100)
            if idx != -1:
                end_idx = min(end_idx, idx)

        risk_section = filing_text[start_idx:end_idx]

        # Return first 5000 chars of risk section
        return risk_section[:5000]

    except Exception as e:
        return f"Error extracting risk factors: {str(e)}"


def format_sec_data_for_llm(sec_data: Dict) -> str:
    """
    Format SEC filing data for LLM consumption.

    Args:
        sec_data: Dictionary mapping tickers to SEC filing data

    Returns:
        Formatted string for LLM
    """
    if not sec_data:
        return ""

    output = "\n\nSEC Filing Risk Factors:\n"
    output += "=" * 60 + "\n"

    for ticker, data in sec_data.items():
        output += f"\n{ticker} - {data.get('filing_type', '10-K')} Risk Factors:\n"
        output += "-" * 60 + "\n"
        risk_text = data.get('risk_factors', 'No risk factors available')
        output += risk_text[:1000] + "...\n"

    return output
