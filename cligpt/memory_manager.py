# memory_manager.py

import os
import datetime
import re
import json
from config import CONTEXT_FILE, PERMANENT_MEMORY_FILE, DELIMITER, MAX_CONTEXT_TOKENS

def estimate_tokens(text):
    """Estimate token count by splitting text on whitespace."""
    return len(text.split())

def load_context_blocks():
    """Load context blocks from CONTEXT_FILE as a list of blocks."""
    if not os.path.exists(CONTEXT_FILE):
        return []
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return content.split(DELIMITER) if content else []

def save_context_block(block):
    """Append a block to CONTEXT_FILE."""
    with open(CONTEXT_FILE, "a", encoding="utf-8") as f:
        f.write(block + DELIMITER)

def load_permanent_memories():
    """Load permanent memories from PERMANENT_MEMORY_FILE as a list of entries."""
    if not os.path.exists(PERMANENT_MEMORY_FILE):
        return []
    with open(PERMANENT_MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            memories = json.load(f)
            return memories if isinstance(memories, list) else []
        except json.JSONDecodeError:
            return []

def save_permanent_memories(memories):
    """Save the list of permanent memories to PERMANENT_MEMORY_FILE."""
    with open(PERMANENT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2)

def add_permanent_memory(text):
    """Add a text block to permanent memory with a timestamp.
    
    This entry will be exempt from pruning.
    """
    memories = load_permanent_memories()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"id": len(memories) + 1, "timestamp": timestamp, "text": text}
    memories.append(entry)
    save_permanent_memories(memories)
    return entry

def view_permanent_memory():
    """Return a list of permanent memory entries as formatted strings."""
    memories = load_permanent_memories()
    lines = []
    for mem in memories:
        lines.append(f"[{mem['id']}] ({mem['timestamp']}) {mem['text']}")
    return lines

def forget_permanent_memory(entry_id):
    """Remove a permanent memory entry by its id."""
    memories = load_permanent_memories()
    new_memories = [mem for mem in memories if mem["id"] != entry_id]
    # Reassign IDs sequentially
    for idx, mem in enumerate(new_memories, start=1):
        mem["id"] = idx
    save_permanent_memories(new_memories)
    return new_memories

def export_permanent_memory(output_file):
    """Export permanent memories to the specified file in JSON format."""
    memories = load_permanent_memories()
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2)
    return output_file

def prune_context(user_prompt):
    """
    Assemble context for the AI prompt in prioritized order:
      1. Permanent memories (always included)
      2. Recent context blocks (within the last hour)
    Older blocks can be added if there’s remaining token space.
    
    Returns:
      pruned_context (str), count of selected non-permanent blocks,
      a dummy aggregated topic_tags, and the oldest timestamp found.
    """
    now = datetime.datetime.now()

    # Load permanent memories and format them as context blocks.
    permanent_memories = load_permanent_memories()
    perm_texts = []
    for mem in permanent_memories:
        perm_texts.append(f"[{mem['timestamp']}] (PERMANENT) {mem['text']}")
    permanent_context = "\n".join(perm_texts)

    blocks = load_context_blocks()
    selected_blocks = []
    accumulated_tokens = estimate_tokens(permanent_context)

    for block in blocks:
        # Check if block is recent (within last hour)
        is_recent = False
        m_time = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", block)
        if m_time:
            try:
                block_time = datetime.datetime.strptime(m_time.group(1), "%Y-%m-%d %H:%M:%S")
                if now - block_time <= datetime.timedelta(hours=1):
                    is_recent = True
            except Exception:
                pass
        if is_recent:
            tokens = estimate_tokens(block)
            if accumulated_tokens + tokens > MAX_CONTEXT_TOKENS:
                break
            selected_blocks.append(block)
            accumulated_tokens += tokens

    # Assemble final context: permanent memories come first.
    pruned_context = permanent_context
    if permanent_context:
        pruned_context += "\n" + DELIMITER
    pruned_context += DELIMITER.join(selected_blocks)

    # Dummy topic tags and oldest timestamp calculation.
    topic_tags = "permanent, recent" if selected_blocks else "permanent"
    oldest_timestamp = "None"
    if selected_blocks:
        times = []
        for block in selected_blocks:
            m_time = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", block)
            if m_time:
                try:
                    t = datetime.datetime.strptime(m_time.group(1), "%Y-%m-%d %H:%M:%S")
                    times.append(t)
                except Exception:
                    pass
        if times:
            oldest_timestamp = min(times).strftime("%Y-%m-%d %H:%M:%S")
    return pruned_context, len(selected_blocks), topic_tags, oldest_timestamp

def add_to_context(user_prompt, answer_text, topics):
    """
    Append a new conversation block to the context file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    topics_str = ", ".join(topics) if topics else "None"
    block = f"[{timestamp}] >>> {user_prompt}\n[Response] {answer_text}\nTopic Tags: {topics_str}"
    save_context_block(block)

