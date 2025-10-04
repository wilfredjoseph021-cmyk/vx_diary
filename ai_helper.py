def summarize_note(note):
    # Rare simple “AI-style” summary
    sentences = note.split(".")
    return sentences[0] if sentences else note

# Example usage:
note = "This is my first secret plan. I will test it tomorrow."
print("Summary:", summarize_note(note))

