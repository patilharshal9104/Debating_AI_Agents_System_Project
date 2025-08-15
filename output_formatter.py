"""
output_formatter.py - Functions for formatting and saving debate output
"""

import os
from typing import List, Dict
from utils import safe_json_parse

def format_and_save_transcript(question: str, history: List[Dict], final_answer: str, filename: str = "debate_transcript.md"):
    """Format debate output and save to Markdown file."""
    print("[DEBUG] Formatting and saving transcript")
    print("[DEBUG] Saving to: " + os.path.abspath(filename))
    
    # Initialize transcript content
    transcript = f"# AI News Channel Debate Transcript\n\n"
    transcript += f"## Topic: {question}\n\n"
    
    # Print to console and build transcript
    print("==================================================")
    print("Debate Transcript")
    print("==================================================\n")
    
    print("Initial Suggestions:\n")
    transcript += f"## Initial Suggestions\n\n"
    for round_data in [h for h in history if h['stage'] == "initial_suggestion"]:
        print(f"{round_data['agent']} suggests:")
        answer_text = round_data["answer"]
        json_block = safe_json_parse(round_data["raw_response"], "initial_suggestion")
        answer_text = json_block.get("answer", answer_text) if json_block else answer_text
        print(answer_text)
        valid_count = len([r for r in round_data['references'] if r.valid])
        print(f"Supporting References: {valid_count} valid\n")
        transcript += f"### {round_data['agent']}\n"
        transcript += f"{answer_text}\n\n"
        transcript += f"#### References\n"
        for ref in round_data['references']:
            if ref.valid:
                transcript += f"- {ref.url} (Domain: {ref.domain}, Authority: {ref.authority_score}/3)\n"
        transcript += "\n"
    
    for r in range(1, max((h['round'] for h in history if h['stage'] in ["critique", "refinement"]), default=0) + 1):
        print(f"Critique Round {r}:\n")
        transcript += f"## Critique Round {r}\n\n"
        for round_data in [h for h in history if h['stage'] == "critique" and h['round'] == r]:
            print(f"{round_data['agent']} critiques:")
            answer_text = round_data["answer"]
            json_block = safe_json_parse(round_data["raw_response"], "critique")
            answer_text = json_block.get("critique", answer_text) if json_block else answer_text
            print(answer_text)
            valid_count = len([r for r in round_data['references'] if r.valid])
            print(f"Supporting References: {valid_count} valid\n")
            transcript += f"### {round_data['agent']}\n"
            transcript += f"{answer_text}\n\n"
            transcript += f"#### References\n"
            for ref in round_data['references']:
                if ref.valid:
                    transcript += f"- {ref.url} (Domain: {ref.domain}, Authority: {ref.authority_score}/3)\n"
            transcript += "\n"
        
        print(f"Refinement Round {r}:\n")
        transcript += f"## Refinement Round {r}\n\n"
        for round_data in [h for h in history if h['stage'] == "refinement" and h['round'] == r]:
            print(f"{round_data['agent']} refines:")
            answer_text = round_data["answer"]
            json_block = safe_json_parse(round_data["raw_response"], "refinement")
            answer_text = json_block.get("answer", answer_text) if json_block else answer_text
            print(answer_text)
            valid_count = len([r for r in round_data['references'] if r.valid])
            print(f"Supporting References: {valid_count} valid\n")
            transcript += f"### {round_data['agent']}\n"
            transcript += f"{answer_text}\n\n"
            transcript += f"#### References\n"
            for ref in round_data['references']:
                if ref.valid:
                    transcript += f"- {ref.url} (Domain: {ref.domain}, Authority: {ref.authority_score}/3)\n"
            transcript += "\n"
    
    print("==================================================")
    print("Debate Summary")
    print("==================================================\n")
    print(final_answer)
    transcript += f"## Final Answer\n\n"
    transcript += final_answer.replace("```json", "").replace("```", "").strip() + "\n"
    
    # Save to Markdown
    try:
        with open(filename, "w", encoding="utf-8", errors="ignore") as f:
            f.write(transcript)
        print(f"\nFull debate transcript saved to '{os.path.abspath(filename)}'")
    except Exception as e:
        print(f"[DEBUG] Failed to save transcript to {filename}: {e}")
        # Fallback: save to a backup file
        backup_file = "debate_transcript_backup.md"
        with open(backup_file, "w", encoding="utf-8", errors="ignore") as f:
            f.write(transcript)
        print(f"[DEBUG] Saved transcript to backup file: '{os.path.abspath(backup_file)}'")