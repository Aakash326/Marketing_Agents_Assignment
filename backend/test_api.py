"""
Test script for Portfolio Intelligence API endpoints.
Run this after starting the FastAPI server to verify all endpoints work correctly.

Usage:
    python test_api.py
"""

import requests
import json
from typing import Dict, Any
import time


# API Base URL
BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"


def print_response(title: str, response: requests.Response):
    """Pretty print API response."""
    print("\n" + "=" * 60)
    print(f"✨ {title}")
    print("=" * 60)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def test_health_check():
    """Test health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed")


def test_root():
    """Test root endpoint."""
    response = requests.get(BASE_URL)
    print_response("Root Endpoint", response)
    assert response.status_code == 200
    print("✅ Root endpoint passed")


def test_query_portfolio():
    """Test main query endpoint."""
    payload = {
        "query": "What stocks do I own?",
        "client_id": "CLT-001"
    }
    
    response = requests.post(f"{API_V1}/query", json=payload)
    print_response("Query Portfolio", response)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "session_id" in data
    assert len(data["response"]) > 0
    
    print("✅ Query portfolio passed")
    return data["session_id"]


def test_get_portfolio():
    """Test get client portfolio endpoint."""
    response = requests.get(f"{API_V1}/clients/CLT-001/portfolio")
    print_response("Get Client Portfolio", response)
    
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == "CLT-001"
    assert data["total_holdings"] > 0
    assert len(data["holdings"]) > 0
    
    print("✅ Get portfolio passed")


def test_session_management(session_id: str):
    """Test session endpoints."""
    # Get session
    response = requests.get(f"{API_V1}/session/{session_id}")
    print_response("Get Session", response)
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "conversation_history" in data
    
    print("✅ Get session passed")
    
    # Delete session
    response = requests.delete(f"{API_V1}/session/{session_id}")
    print_response("Delete Session", response)
    
    assert response.status_code == 200
    assert response.json()["success"] == True
    
    print("✅ Delete session passed")


def test_conversation_continuity():
    """Test multi-turn conversation."""
    # First query
    payload1 = {
        "query": "What stocks do I own?",
        "client_id": "CLT-001"
    }
    response1 = requests.post(f"{API_V1}/query", json=payload1)
    session_id = response1.json()["session_id"]
    print_response("First Query", response1)
    
    # Second query with same session
    time.sleep(1)  # Brief delay
    payload2 = {
        "query": "Which of my holdings has the best return?",
        "client_id": "CLT-001",
        "session_id": session_id
    }
    response2 = requests.post(f"{API_V1}/query", json=payload2)
    print_response("Second Query (Same Session)", response2)
    
    assert response2.json()["session_id"] == session_id
    print("✅ Conversation continuity passed")
    
    # Clean up
    requests.delete(f"{API_V1}/session/{session_id}")


def test_invalid_client():
    """Test error handling with invalid client ID."""
    payload = {
        "query": "What stocks do I own?",
        "client_id": "INVALID"
    }
    
    response = requests.post(f"{API_V1}/query", json=payload)
    print_response("Invalid Client ID (Should Fail)", response)
    
    assert response.status_code == 400  # Bad request
    print("✅ Invalid client handling passed")


def test_404_client():
    """Test non-existent client."""
    response = requests.get(f"{API_V1}/clients/CLT-999/portfolio")
    print_response("Non-existent Client (Should 404)", response)
    
    assert response.status_code == 404
    print("✅ 404 handling passed")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 Portfolio Intelligence API - Test Suite")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print("=" * 60)
    
    try:
        # Basic endpoints
        test_health_check()
        test_root()
        
        # Main functionality
        session_id = test_query_portfolio()
        test_get_portfolio()
        test_session_management(session_id)
        
        # Advanced tests
        test_conversation_continuity()
        
        # Error handling
        test_invalid_client()
        test_404_client()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\n✅ The Portfolio Intelligence API is working correctly!")
        print(f"📖 View documentation at: {BASE_URL}/docs")
        print("=" * 60)
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        return 1
    
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 60)
        print("❌ CONNECTION ERROR")
        print("=" * 60)
        print(f"Could not connect to API at {BASE_URL}")
        print("\nMake sure the server is running:")
        print("  cd backend")
        print("  python main.py")
        print("=" * 60)
        return 1
    
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
