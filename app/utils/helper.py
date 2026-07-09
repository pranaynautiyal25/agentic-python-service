from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def current_utc_time() -> str:
    return datetime.now(timezone.utc).isoformat()


def add_step(
    outputs: list[dict[str, Any]] | None,
    step: str,
    data: Any,
    kind: str = "text",
    title: str | None = None,
    url: str | None = None,
) -> list[dict[str, Any]]:
    if outputs is None:
        outputs = []

    outputs.append(
        {
            "step": step,
            "kind": kind,
            "title": title or step.replace("_", " ").title(),
            "data": data,
            "url": url,
        }
    )
    return outputs


def save_text_file(content: str, prefix: str = "meeting_output") -> str:
    folder = PROJECT_ROOT / "generated_files"
    folder.mkdir(exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = folder / f"{prefix}_{stamp}.txt"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


def search_results_to_text(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No search results found."

    lines = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "")
        url = item.get("url", "")
        snippet = item.get("snippet", "")
        lines.append(f"{i}. {title}\n   {url}\n   {snippet}")

    return "\n\n".join(lines)


def make_mailto_url(to_email: str, subject: str, body: str) -> str:
    subject_q = quote(subject)
    body_q = quote(body)
    if to_email:
        return f"mailto:{to_email}?subject={subject_q}&body={body_q}"
    return f"mailto:?subject={subject_q}&body={body_q}"