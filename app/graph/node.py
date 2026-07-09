from __future__ import annotations

from app.schemas.state import GraphState
from app.services.llm import llm_text
from app.services.search import search_with_fallback
from app.utils.helper import add_step, make_mailto_url, search_results_to_text


def _combined_text(state: GraphState) -> str:
    inp = state["input_one"]
    return f"{inp.get('messy_note', '')}\n{inp.get('what_to_do', '')}"


def _infer_main_actions(text: str) -> list[str]:
    text = text.lower()
    actions: list[str] = []

    if any(k in text for k in ["summarize", "summary", "expand", "shorten"]):
        actions.append("summarize")

    if any(k in text for k in ["plan", "deadline", "deadlines", "timeline", "schedule"]):
        actions.append("plan")

    if any(k in text for k in ["divide work", "assign", "split work", "distribution"]):
        actions.append("divide")

    if any(k in text for k in ["resource", "resources", "external", "reference", "references"]):
        actions.append("resources")

    if not actions:
        actions.append("explain")

    return list(dict.fromkeys(actions))


def _infer_post_actions(text: str) -> list[str]:
    text = text.lower()
    actions: list[str] = []

    if any(k in text for k in ["document", "txt", "file", "report", "pdf", "save note"]):
        actions.append("document")

    if any(k in text for k in ["mail", "email", "gmail", "draft mail", "draft email", "send email", "send mail"]):
        actions.append("human_input")

    return list(dict.fromkeys(actions))


def enhance_prompt(state: GraphState) -> GraphState:
    note = state["input_one"].get("messy_note", "")
    task = state["input_one"].get("what_to_do", "")

    prompt = f"""
Clean this meeting request into a short, clear instruction.

Meeting notes:
{note}

User task:
{task}

Return only the cleaned instruction.
""".strip()

    formatted = llm_text(prompt)
    outputs = add_step(state.get("outputs"), "formatted_prompt", formatted, kind="text")
    return {"formatted_prompt": formatted, "outputs": outputs}


def route_main(state: GraphState) -> GraphState:
    actions = _infer_main_actions(_combined_text(state))
    outputs = add_step(state.get("outputs"), "main_router", actions, kind="text")
    return {"selected_actions": actions, "outputs": outputs}


def route_post(state: GraphState) -> GraphState:
    actions = _infer_post_actions(_combined_text(state))
    outputs = add_step(state.get("outputs"), "post_router", actions or ["end"], kind="text")
    return {"post_actions": actions, "outputs": outputs}


def summarize_node(state: GraphState) -> GraphState:
    prompt = f"""
Summarize these meeting notes in simple bullet points:

{state['input_one'].get('messy_note', '')}
""".strip()

    result = llm_text(prompt)
    outputs = add_step(state.get("outputs"), "summary", result, kind="text")
    return {"outputs": outputs}


def plan_node(state: GraphState) -> GraphState:
    prompt = f"""
Create a practical team plan with deadlines.

Meeting notes:
{state['input_one'].get('messy_note', '')}

Task:
{state['input_one'].get('what_to_do', '')}
""".strip()

    result = llm_text(prompt)
    outputs = add_step(state.get("outputs"), "plan", result, kind="text")
    return {"outputs": outputs}


def divide_work_node(state: GraphState) -> GraphState:
    prompt = f"""
Divide the work among team members in a practical way.

Meeting notes:
{state['input_one'].get('messy_note', '')}

Task:
{state['input_one'].get('what_to_do', '')}
""".strip()

    result = llm_text(prompt)
    outputs = add_step(state.get("outputs"), "divide_work", result, kind="text")
    return {"outputs": outputs}


def resources_node(state: GraphState) -> GraphState:
    query = state.get("formatted_prompt") or state["input_one"].get("what_to_do", "")
    results = search_with_fallback(query)
    text_view = search_results_to_text(results)

    outputs = add_step(state.get("outputs"), "external_resources", text_view, kind="text")
    return {"search_results": results, "outputs": outputs}


def explain_node(state: GraphState) -> GraphState:
    prompt = f"""
Explain the meeting outcome in clear bullet points.

Meeting notes:
{state['input_one'].get('messy_note', '')}

Task:
{state['input_one'].get('what_to_do', '')}
""".strip()

    result = llm_text(prompt)
    outputs = add_step(state.get("outputs"), "explain", result, kind="text")
    return {"outputs": outputs}


def execute_main_actions(state: GraphState) -> GraphState:
    actions = state.get("selected_actions", [])
    outputs = state.get("outputs", [])

    handlers = {
        "summarize": summarize_node,
        "plan": plan_node,
        "divide": divide_work_node,
        "resources": resources_node,
        "explain": explain_node,
    }

    for action in actions:
        current_state = {**state, "outputs": outputs}
        handler = handlers.get(action, explain_node)
        result = handler(current_state)
        outputs = result["outputs"]
        state = {**state, **result}

    return {
        "outputs": outputs,
        "search_results": state.get("search_results", []),
        "formatted_prompt": state.get("formatted_prompt", ""),
    }

def document_node(state: GraphState) -> GraphState:
    outputs = add_step(
        state.get("outputs", []),
        "document",
        "Document upload is currently unavailable due to an issue.",
        kind="text",
        title="Document",
    )

    return {
        **state,
        "document_url": None,
        "outputs": outputs,
    }



def human_input_node(state: GraphState) -> GraphState:
    human = state.get("human_input", {})

    recipient_email = human.get("recipient_email", "")
    recipient_name = human.get("recipient_name", "")
    sender_name = human.get("sender_name", "")
    subject = human.get("subject", "Draft Email")
    key_points = human.get("key_points", "")
    tone = human.get("tone", "professional")

    prompt = f"""
Write a simple email body.

Tone: {tone}
Sender: {sender_name}
Recipient: {recipient_name}

Key points:
{key_points}

Return only the email body.
""".strip()

    body = llm_text(prompt)
    mail_url = make_mailto_url(recipient_email, subject, body)

    outputs = add_step(
        state.get("outputs"),
        "human_input",
        "Click to compose mail",
        kind="url",
        title="Compose Mail",
        url=mail_url,
    )

    return {
        "human_input_url": mail_url,
        "human_input_subject": subject,
        "human_input_body": body,
        "mail_status": "ready",
        "mail_message": "Human approval step created.",
        "outputs": outputs,
    }


def execute_post_actions(state: GraphState) -> GraphState:
    actions = state.get("post_actions", [])
    outputs = state.get("outputs", [])
    current_state = dict(state)
    current_state["outputs"] = outputs

    for action in actions:
        if action == "document":
            result = document_node(current_state)
        elif action == "human_input":
            result = human_input_node(current_state)
        else:
            continue

        outputs = result["outputs"]
        current_state = {**current_state, **result, "outputs": outputs}

    return {
        "outputs": outputs,
        "document_url": current_state.get("document_url"),
        "human_input_url": current_state.get("human_input_url"),
        "human_input_subject": current_state.get("human_input_subject"),
        "human_input_body": current_state.get("human_input_body"),
        "mail_status": current_state.get("mail_status"),
        "mail_message": current_state.get("mail_message"),
    }