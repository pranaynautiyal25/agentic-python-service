from __future__ import annotations

from app.graph.workflow import graph
from app.graph.node import human_input_node
from app.schemas.input_models import UserRequest, HumanInputRequest
from app.schemas.output_models import FinalResponse, StepData


def run_pipeline(payload: UserRequest) -> FinalResponse:
    initial_state = {
        "input_one": payload.input_one.model_dump(),
        "outputs": [],
    }

    result = graph.invoke(initial_state)
    outputs = [StepData(**item) for item in result.get("outputs", [])]

    return FinalResponse(
        outputs=outputs,
        document_url=result.get("document_url"),
        human_input_url=result.get("human_input_url"),
        human_input_subject=result.get("human_input_subject"),
        human_input_body=result.get("human_input_body"),
        mail_status=result.get("mail_status"),
        mail_message=result.get("mail_message"),
    )


def human_input_pipeline(payload: HumanInputRequest) -> FinalResponse:
    initial_state = {
        "input_one": payload.input_one.model_dump(),
        "human_input": payload.human_input.model_dump(),
        "outputs": [],
    }

    result = human_input_node(initial_state)
    outputs = [StepData(**item) for item in result.get("outputs", [])]

    return FinalResponse(
        outputs=outputs,
        human_input_url=result.get("human_input_url"),
        human_input_subject=result.get("human_input_subject"),
        human_input_body=result.get("human_input_body"),
        mail_status=result.get("mail_status"),
        mail_message=result.get("mail_message"),
    )