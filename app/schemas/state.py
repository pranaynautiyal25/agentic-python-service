from typing import Any, TypedDict


class GraphState(TypedDict, total=False):
    input_one: dict[str, Any]
    human_input: dict[str, Any]

    formatted_prompt: str
    selected_actions: list[str]
    post_actions: list[str]

    outputs: list[dict[str, Any]]
    search_results: list[dict[str, Any]]

    file_path: str
    file_url: str
    document_url: str

    human_input_url: str
    human_input_subject: str
    human_input_body: str
    mail_status: str
    mail_message: str