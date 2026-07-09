from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from app.graph.node import (
    enhance_prompt,
    route_main,
    execute_main_actions,
    route_post,
    execute_post_actions,
    simple_answer_node,
)
from app.schemas.state import GraphState


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("enhance_prompt", enhance_prompt)
    builder.add_node("route_main", route_main)
    builder.add_node("execute_main_actions", execute_main_actions)
    builder.add_node("route_post", route_post)
    builder.add_node("execute_post_actions", execute_post_actions)

    builder.add_edge(START, "enhance_prompt")
    builder.add_edge("enhance_prompt", "route_main")
    builder.add_edge("route_main", "execute_main_actions")
    builder.add_edge("execute_main_actions", "route_post")
    builder.add_edge("route_post", "execute_post_actions")
    builder.add_edge("execute_post_actions", END)

    return builder.compile()


graph = build_graph()