"""
main.py - Entry point for the AI News Channel Debate
"""

import asyncio
import sys
import warnings
import os
import urllib3
from debate_engine import DebateEngine
from output_formatter import format_and_save_transcript
from config import GEMINI_API_KEY, DEEPSEEK_API_KEY

# Suppress warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning, module='tf_keras')

# Windows compatibility
if sys.platform == "win32":
    import types
    sys.modules['pwd'] = types.ModuleType('pwd')
    sys.modules['pwd'].getpwnam = lambda x: None

async def main():
    """Run the debate system."""
    try:
        print("[DEBUG] Starting program")
        print("[DEBUG] Current working directory: " + os.getcwd())
        print("[DEBUG] GEMINI_API_KEY present: " + ("Yes" if GEMINI_API_KEY else "No"))
        print("[DEBUG] DEEPSEEK_API_KEY present: " + ("Yes" if DEEPSEEK_API_KEY else "No"))
        
        print("\n==================================================")
        print("Welcome to the AI News Channel Debate!")
        print("==================================================\n")
        question = input("Enter the debate topic:\n> ").strip()
        if not question:
            print("No topic provided. Exiting the debate.")
            return
        
        print(f"\nToday's Hot Topic: {question}")
        print("Advocates: Gemini (Proponent) and DeepSeek (Opponent)")
        print("Let's start the lawyer-style debate!\n")
        
        engine = DebateEngine(rounds=1)
        print("[DEBUG] DebateEngine attributes: " + str(dir(engine)))  # Debug class attributes
        try:
            final_answer, history = await engine.run_debate(question)
        except Exception as e:
            print(f"[DEBUG] Debate engine error: {e}")
            final_answer = f"[Error] Debate failed: {e}"
            history = []
        
        # Ensure output is generated even on partial failure
        try:
            format_and_save_transcript(question, history, final_answer)
        except Exception as e:
            print(f"[DEBUG] Output formatting error: {e}")
            # Fallback: write raw output to file
            with open("debate_transcript_fallback.txt", "w", encoding="utf-8", errors="ignore") as f:
                f.write(f"# Debate Transcript (Fallback)\n\n")
                f.write(f"Topic: {question}\n\n")
                f.write(f"Error: {e}\n\n")
                f.write(f"Final Answer:\n{final_answer}\n\n")
                f.write("History:\n")
                for h in history:
                    f.write(f"{h['agent']} ({h['stage']}): {h['answer']}\n")
            print("[DEBUG] Fallback transcript saved to 'debate_transcript_fallback.txt'")
        
        print("[DEBUG] Program completed")
    except KeyboardInterrupt:
        print("\nDebate interrupted by user")
    except Exception as e:
        print(f"[DEBUG] Error in main: {e}")
        print("An error occurred during the debate. Please check logs and try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"[DEBUG] Fatal error: {e}")