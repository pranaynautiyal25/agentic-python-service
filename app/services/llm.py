import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm(api_key=None, model=None):
    return ChatGroq(
        api_key=api_key or os.getenv("GROQ_API_KEY"),
        model=model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
    )


def llm_text(prompt, api_key=None, model=None):
    llm = get_llm(api_key=api_key, model=model)
    response = llm.invoke(prompt)
    return response.content


def llm_enhancer_prompt(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_ENHANCER_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_ENHANCER_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_summary(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_SUMMARY_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_SUMMARY_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_plan(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_PLAN_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_PLAN_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_divide_work(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_DIVIDE_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_DIVIDE_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_explain(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_EXPLAIN_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_EXPLAIN_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_mail(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_MAIL_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_MAIL_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def llm_simple(prompt):
    return llm_text(
        prompt,
        api_key=os.getenv("GROQ_SIMPLE_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_SIMPLE_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )


def router_decision_llm(prompt):
    llm = get_llm(
        api_key=os.getenv("GROQ_ROUTER_API_KEY", os.getenv("GROQ_API_KEY")),
        model=os.getenv("GROQ_ROUTER_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "actions" in data and isinstance(data["actions"], list):
            return data["actions"]
    except Exception:
        pass

    return [text]

