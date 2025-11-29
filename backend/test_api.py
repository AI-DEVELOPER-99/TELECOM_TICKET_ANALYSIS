"""
Test script for the Ticket Analysis API
Run this after starting the backend to verify everything is working
"""

import requests
import json
from typing import Dict

API_BASE_URL = "http://localhost:5000"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def test_health_check():
    """Test the health check endpoint"""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get('status') == 'healthy' and data.get('initialized'):
            print("✅ Backend is healthy and initialized!")
            return True
        else:
            print("⚠️  Backend is running but not fully initialized")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Test the stats endpoint"""
    print_section("Testing System Statistics")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/stats", timeout=5)
        data = response.json()
        
        if data.get('success'):
            stats = data['stats']
            print(f"Total Tickets: {stats['total_tickets']:,}")
            print(f"Embedding Model: {stats['embedding_model']}")
            print(f"LLM Model: {stats['llm_model']}")
            print(f"Embedding Dimension: {stats['embedding_dimension']}")
            print("\n✅ Stats retrieved successfully!")
            return True
        else:
            print(f"❌ Failed: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search():
    """Test the search endpoint"""
    print_section("Testing Ticket Search")
    
    query = "internet connection problems"
    print(f"Search Query: '{query}'")
    print(f"Top K: 3\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/search",
            json={"query": query, "top_k": 3},
            timeout=10
        )
        data = response.json()
        
        if data.get('success'):
            results = data['results']
            print(f"Found {len(results)} similar tickets:\n")
            
            for i, result in enumerate(results, 1):
                similarity = int(result['similarity_score'] * 100)
                print(f"{i}. {result['subject']}")
                print(f"   Similarity: {similarity}% | Type: {result['type']} | Priority: {result['priority']}")
                print(f"   Preview: {result['body'][:100]}...")
                print()
            
            print("✅ Search completed successfully!")
            return True
        else:
            print(f"❌ Failed: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analyze():
    """Test the analyze endpoint"""
    print_section("Testing Ticket Analysis")
    
    ticket_description = """
Subject: VPN Connection Failure

Description: I am unable to connect to the company VPN from my home network. 
When I try to connect, I get an error message "Connection timeout - Error 800". 
I have tried restarting my computer and router, but the problem persists. 
This is blocking my ability to work remotely. Please help urgently.
    """.strip()
    
    print(f"Ticket Description:\n{ticket_description}\n")
    print("Analyzing... (this may take 5-10 seconds)\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json={"ticket_description": ticket_description},
            timeout=30
        )
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Analysis completed!")
            print(f"Similar tickets analyzed: {data['similar_tickets_count']}\n")
            
            print("─" * 80)
            print("TOP 3 RECOMMENDED SOLUTIONS:")
            print("─" * 80 + "\n")
            
            for solution in data['solutions']:
                percentage = solution['suitability_percentage']
                
                # Color indicator
                if percentage >= 75:
                    indicator = "🟢"
                elif percentage >= 50:
                    indicator = "🟡"
                else:
                    indicator = "🔴"
                
                print(f"{indicator} Solution #{solution['rank']} - Suitability: {percentage}%")
                print("─" * 80)
                print(f"\n{solution['solution']}\n")
                print(f"Reasoning: {solution['reasoning']}")
                
                if solution['reference_tickets']:
                    refs = ', '.join(map(str, solution['reference_tickets']))
                    print(f"References: Similar tickets #{refs}")
                
                print()
            
            return True
        else:
            print(f"❌ Failed: {data.get('error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The backend might be processing slowly.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_generate_solution():
    """Test the generate solution endpoint"""
    print_section("Testing Solution Generation with LLM")
    
    ticket_description = """
Subject: Email Server Not Responding

Description: Our company email server has been unresponsive since this morning. 
Users are getting timeout errors when trying to send or receive emails. 
The server appears to be running but connections are timing out. 
We need to restore email service as soon as possible.
    """.strip()
    
    print(f"Ticket Description:\n{ticket_description}\n")
    print("Generating solution with LLM... (this may take 10-15 seconds)\n")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/generate-solution",
            json={"ticket_description": ticket_description},
            timeout=30
        )
        data = response.json()
        
        if data.get('success'):
            print(f"✅ Solution generated successfully!")
            print(f"Retrieved chunks: {data['chunks_count']}")
            print(f"LLM Model: {data['llm_model']}\n")
            
            print("─" * 80)
            print("GENERATED SOLUTION:")
            print("─" * 80 + "\n")
            print(data['generated_solution'])
            print()
            
            print("─" * 80)
            print(f"RETRIEVED CONTEXT ({data['chunks_count']} similar tickets):")
            print("─" * 80 + "\n")
            
            for i, chunk in enumerate(data['retrieved_chunks'][:3], 1):
                similarity = int(chunk['similarity_score'] * 100)
                print(f"{i}. {chunk['subject']}")
                print(f"   Similarity: {similarity}% | Type: {chunk['type']}")
                print(f"   Preview: {chunk['body'][:100]}...")
                print()
            
            return True
        else:
            print(f"❌ Failed: {data.get('error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The backend might be processing slowly.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("  TELECOM TICKET ANALYSIS API - TEST SUITE")
    print("=" * 80)
    print("\nMake sure the backend is running before running these tests!")
    print("Start backend with: cd backend && python app.py\n")
    
    input("Press Enter to start tests...")
    
    # Run tests
    results = {
        "Health Check": test_health_check(),
        "System Stats": test_stats(),
        "Ticket Search": test_search(),
        "Ticket Analysis": test_analyze(),
        "Generate Solution": test_generate_solution()
    }
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
