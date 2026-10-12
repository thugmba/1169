"""Chat-window styling for prompts in lecture-note decks.

Prompts are shown inside a generic "AI Chat" window so students can see that
the text is typed or pasted into an AI chat box. A colored label above the
window says whether to avoid or use the prompt.
"""

from __future__ import annotations

import html

LABELS = {
    "weak": "Do not use",
    "good": "Copy and send",
    "plain": "Fill in, then send",
}

CHAT_CSS = r'''
.chat-wrap { min-width: 0; }
.chat-label { display: inline-block; font-size: 17px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; padding: 5px 12px; border-radius: 6px; margin-bottom: 8px; color: #fff; }
.chat-label.weak { background: #be123c; }
.chat-label.good { background: #15803d; }
.chat-label.plain { background: #475569; }
.chat { border: 1px solid #cbd5e1; border-radius: 14px; background: #fff; overflow: hidden; }
.chat-bar { background: #f1f5f9; border-bottom: 1px solid #e2e8f0; padding: 5px 14px; font-size: 16px; color: #475569; font-weight: bold; }
.dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 5px; vertical-align: middle; }
.d1 { background: #f87171; } .d2 { background: #fbbf24; } .d3 { background: #4ade80; }
.chat-bar .title { margin-left: 8px; vertical-align: middle; }
.chat-body { padding: 8px 10px; background: #fafafa; }
.bubble { margin-left: 2%; background: #e8eefc; border: 1px solid #c7d2fe; border-radius: 16px 16px 4px 16px; padding: 6px 12px; }
.bubble .who { font-size: 15px; font-weight: 800; color: #3730a3; margin-bottom: 2px; }
.bubble pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 15pt/1.24 Arial, Helvetica, sans-serif; color: #172033; }
.bubble table { width: 100%; border-collapse: collapse; }
.bubble td { width: 50%; vertical-align: top; padding: 0 12px 0 0; }
.bubble td + td { padding: 0 0 0 12px; border-left: 1px solid #c7d2fe; }
.chat-input { border-top: 1px solid #e2e8f0; padding: 5px 12px; }
.chat-input .ph { display: block; border: 1px solid #cbd5e1; border-radius: 20px; padding: 6px 16px; margin-right: 46px; color: #94a3b8; font-size: 17px; }
.send { float: right; width: 32px; height: 32px; margin-top: 1px; }
.send svg { display: block; }
'''


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _split_columns(text: str) -> tuple[str, str]:
    """Split a long prompt at the paragraph break nearest its middle."""
    blocks = text.split("\n\n")
    if len(blocks) < 2:
        lines = text.splitlines()
        half = (len(lines) + 1) // 2
        return "\n".join(lines[:half]), "\n".join(lines[half:])
    sizes = [len(b.splitlines()) + 1 for b in blocks]
    best = min(range(1, len(blocks)), key=lambda i: abs(sum(sizes[:i]) - sum(sizes[i:])))
    return "\n\n".join(blocks[:best]), "\n\n".join(blocks[best:])


def chat(text: str, kind: str = "good", label: str | None = None, cols: bool = False) -> str:
    """Return a chat window holding the prompt text.

    kind: "weak" (red label), "good" (green label), or "plain" (gray label).
    cols: split a long prompt into two columns inside the bubble.
    """
    label = label or LABELS[kind]
    if cols:
        left, right = _split_columns(text)
        inner = (f'<table><tr><td><pre>{_esc(left)}</pre></td>'
                 f'<td><pre>{_esc(right)}</pre></td></tr></table>')
    else:
        inner = f"<pre>{_esc(text)}</pre>"
    return (f'<div class="chat-wrap"><span class="chat-label {kind}">{_esc(label)}</span>'
            '<div class="chat"><div class="chat-bar"><span class="dot d1"></span><span class="dot d2"></span>'
            '<span class="dot d3"></span><span class="title">AI Chat</span></div>'
            f'<div class="chat-body"><div class="bubble"><div class="who">You</div>{inner}</div></div>'
            '<div class="chat-input"><span class="send">'
            '<svg viewBox="0 0 24 24" width="32" height="32"><circle cx="12" cy="12" r="12" fill="#172033"/>'
            '<path d="M12 17V7M7.5 11.5L12 7l4.5 4.5" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="ph">Message AI...</span></div>'
            "</div></div>")
