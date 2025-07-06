#!/usr/bin/env python3
"""
SpeakoAI Startup Script
This script helps you start the SpeakoAI application
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_database():
    """Check if database exists and initialize if needed"""
    print("🗄️  Checking database...")
    
    db_path = Path("backend/data.db")
    if not db_path.exists():
        print("📝 Initializing database...")
        try:
            import asyncio
            from backend.models import init_db
            asyncio.run(init_db())
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
    else:
        print("✅ Database already exists")
    
    return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting SpeakoAI API server...")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Server started successfully!")
            print("🌐 API available at: http://localhost:8000")
            print("📚 Documentation at: http://localhost:8000/docs")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def open_browser():
    """Open browser to API documentation"""
    print("🌐 Opening API documentation in browser...")
    try:
        webbrowser.open("http://localhost:8000/docs")
        print("✅ Browser opened successfully")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please manually visit: http://localhost:8000/docs")

def show_menu():
    """Show the main menu"""
    print("\n" + "="*50)
    print("🎯 SpeakoAI - IELTS Speaking Practice Platform")
    print("="*50)
    print("1. Start API Server")
    print("2. Start Telegram Bot (requires bot token)")
    print("3. Run API Tests")
    print("4. Open API Documentation")
    print("5. Exit")
    print("="*50)

def start_telegram_bot():
    """Start the Telegram bot"""
    print("🤖 Starting Telegram Bot...")
    
    # Check if bot token is configured
    bot_file = Path("backend/telegram_bot.py")
    if not bot_file.exists():
        print("❌ Telegram bot file not found")
        return
    
    with open(bot_file, 'r') as f:
        content = f.read()
        if "YOUR_TELEGRAM_BOT_TOKEN" in content:
            print("❌ Please configure your Telegram bot token first!")
            print("1. Get a bot token from @BotFather on Telegram")
            print("2. Edit backend/telegram_bot.py")
            print("3. Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual token")
            return
    
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "telegram_bot.py"])
    except Exception as e:
        print(f"❌ Error starting Telegram bot: {e}")

def run_tests():
    """Run API tests"""
    print("🧪 Running API tests...")
    
    test_file = Path("test_api.py")
    if not test_file.exists():
        print("❌ Test file not found")
        return
    
    try:
        subprocess.run([sys.executable, "test_api.py"])
    except Exception as e:
        print(f"❌ Error running tests: {e}")

def main():
    """Main function"""
    print("🎉 Welcome to SpeakoAI!")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check database
    if not check_database():
        return
    
    server_process = None
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            if server_process is None or server_process.poll() is not None:
                server_process = start_server()
                if server_process:
                    open_browser()
            else:
                print("✅ Server is already running!")
        
        elif choice == "2":
            start_telegram_bot()
        
        elif choice == "3":
            if server_process is None or server_process.poll() is not None:
                print("❌ Please start the server first (option 1)")
            else:
                run_tests()
        
        elif choice == "4":
            open_browser()
        
        elif choice == "5":
            print("👋 Goodbye!")
            if server_process and server_process.poll() is None:
                print("🛑 Stopping server...")
                server_process.terminate()
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 