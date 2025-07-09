#!/usr/bin/env python3
"""
Test script for SpeakoAI API
Run this script to test all the main endpoints
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"

async def test_endpoint(session: aiohttp.ClientSession, method: str, endpoint: str, data: Dict[Any, Any] = None) -> Dict[str, Any]:
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            async with session.get(url) as response:
                return {
                    "status": response.status,
                    "data": await response.json() if response.status == 200 else await response.text()
                }
        elif method.upper() == "POST":
            async with session.post(url, json=data) as response:
                return {
                    "status": response.status,
                    "data": await response.json() if response.status in [200, 201] else await response.text()
                }
        elif method.upper() == "PUT":
            async with session.put(url, json=data) as response:
                return {
                    "status": response.status,
                    "data": await response.json() if response.status == 200 else await response.text()
                }
        elif method.upper() == "DELETE":
            async with session.delete(url) as response:
                return {
                    "status": response.status,
                    "data": await response.text()
                }
    except Exception as e:
        return {"status": "ERROR", "data": str(e)}

async def run_tests():
    """Run all API tests"""
    print("🚀 Starting SpeakoAI API Tests...\n")
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Health Check
        print("1. Testing Health Check...")
        result = await test_endpoint(session, "GET", "/")
        print(f"   Status: {result['status']}")
        print(f"   Response: {result['data']}\n")
        
        # Test 2: Create User
        print("2. Testing User Creation...")
        user_data = {
            "tg_id": 123456789,
            "first_name": "Test User",
            "username": "testuser"
        }
        result = await test_endpoint(session, "POST", "/users/", user_data)
        print(f"   Status: {result['status']}")
        print(f"   Response: {result['data']}\n")
        
        # Test 3: Get All Users
        print("3. Testing Get All Users...")
        result = await test_endpoint(session, "GET", "/users/")
        print(f"   Status: {result['status']}")
        print(f"   Users found: {len(result['data']) if isinstance(result['data'], list) else 'N/A'}\n")
        
        # Test 4: Get Questions by Part
        print("4. Testing Get Questions by Part...")
        for part in [1, 2, 3]:
            result = await test_endpoint(session, "GET", f"/questions/part/{part}")
            print(f"   Part {part} - Status: {result['status']}")
            print(f"   Questions found: {len(result['data']) if isinstance(result['data'], list) else 'N/A'}")
        print()
        
        # Test 5: Get All Questions
        print("5. Testing Get All Questions...")
        result = await test_endpoint(session, "GET", "/questions/")
        print(f"   Status: {result['status']}")
        print(f"   Total questions: {len(result['data']) if isinstance(result['data'], list) else 'N/A'}\n")
        
        # Test 6: Create a Response (if we have users and questions)
        print("6. Testing Response Creation...")
        # First get a user and question
        users_result = await test_endpoint(session, "GET", "/users/")
        questions_result = await test_endpoint(session, "GET", "/questions/")
        
        if (isinstance(users_result['data'], list) and len(users_result['data']) > 0 and
            isinstance(questions_result['data'], list) and len(questions_result['data']) > 0):
            
            user_id = users_result['data'][0]['id']
            question_id = questions_result['data'][0]['id']
            
            response_data = {
                "user_id": user_id,
                "question_id": question_id,
                "response_text": "This is a test response for the IELTS speaking practice. I am testing the system functionality.",
                "fluency_score": 7.5,
                "pronunciation_score": 7.0,
                "grammar_score": 8.0,
                "vocabulary_score": 7.5,
                "overall_score": 7.5,
                "ai_feedback": "Good test response with clear structure and appropriate vocabulary."
            }
            
            result = await test_endpoint(session, "POST", "/responses/", response_data)
            print(f"   Status: {result['status']}")
            print(f"   Response: {result['data']}\n")
        else:
            print("   Skipped - No users or questions available\n")
        
        # Test 7: Get User Analytics
        print("7. Testing User Analytics...")
        if isinstance(users_result['data'], list) and len(users_result['data']) > 0:
            user_id = users_result['data'][0]['id']
            result = await test_endpoint(session, "GET", f"/analytics/user/{user_id}")
            print(f"   Status: {result['status']}")
            print(f"   Analytics: {result['data']}\n")
        else:
            print("   Skipped - No users available\n")
        
        # Test 8: Get Leaderboard
        print("8. Testing Leaderboard...")
        result = await test_endpoint(session, "GET", "/analytics/leaderboard")
        print(f"   Status: {result['status']}")
        print(f"   Leaderboard entries: {len(result['data']) if isinstance(result['data'], list) else 'N/A'}\n")
        
        # Test 9: Create Feedback
        print("9. Testing Feedback Creation...")
        if isinstance(users_result['data'], list) and len(users_result['data']) > 0:
            user_id = users_result['data'][0]['id']
            feedback_data = {
                "user_id": user_id,
                "ai_comment": "This is a test feedback comment for the user. Keep practicing to improve your scores!"
            }
            
            result = await test_endpoint(session, "POST", "/feedbacks/", feedback_data)
            print(f"   Status: {result['status']}")
            print(f"   Response: {result['data']}\n")
        else:
            print("   Skipped - No users available\n")
        
        # Test 10: Telegram Integration
        print("10. Testing Telegram Integration...")
        result = await test_endpoint(session, "POST", "/telegram/user?tg_id=987654321&first_name=TelegramUser&username=tguser")
        print(f"   Status: {result['status']}")
        print(f"   Response: {result['data']}\n")
        
        print("✅ All tests completed!")

if __name__ == "__main__":
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Run: cd backend && python main.py")
    print()
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        print("Make sure the server is running and accessible at http://localhost:8000") 