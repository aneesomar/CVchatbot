#!/usr/bin/env python3
"""
Test script to verify personality modes are working correctly.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_agent import PersonalChatbotAgent
import config

def test_personality_modes():
    """Test different personality modes"""
    
    print("🧪 Testing Personality Modes")
    print("=" * 50)
    
    # Test question
    test_question = "Tell me about your programming experience"
    
    for mode_key, mode_info in config.PERSONALITY_MODES.items():
        print(f"\n🎭 Testing {mode_info['name']} ({mode_key})")
        print(f"📝 Description: {mode_info['description']}")
        print("-" * 40)
        
        # Create agent with this mode
        agent = PersonalChatbotAgent(personality_mode=mode_key)
        
        # Test direct chat (without documents)
        try:
            response = agent.chat_direct(test_question)
            print(f"Response: {response[:200]}...")
            
            # Verify mode change
            current_mode = agent.get_current_mode()
            if current_mode and current_mode['mode'] == mode_key:
                print("✅ Mode correctly set")
            else:
                print("❌ Mode not set correctly")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

def test_mode_switching():
    """Test switching between modes"""
    
    print("🔄 Testing Mode Switching")
    print("=" * 50)
    
    agent = PersonalChatbotAgent()
    
    for mode_key in ['interview', 'storytelling', 'fast_facts']:
        print(f"\n🔄 Switching to {mode_key}")
        success = agent.set_personality_mode(mode_key)
        
        if success:
            current_mode = agent.get_current_mode()
            if current_mode and current_mode['mode'] == mode_key:
                print(f"✅ Successfully switched to {current_mode['name']}")
            else:
                print("❌ Mode switch failed")
        else:
            print("❌ Mode switch returned False")

if __name__ == "__main__":
    print("🤖 Anees's Personal AI Assistant - Personality Mode Tests\n")
    
    # Check if we can import the modules
    try:
        test_personality_modes()
        test_mode_switching()
        print("\n🎉 All tests completed!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed and Ollama is running.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
