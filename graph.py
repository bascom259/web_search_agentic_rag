from langgraph.graph import StateGraph, END

from agents import (
    planner_agent,
    researcher_agent,
    retriever_agent,
    answer_agent,
    critic_agent
)


def build_graph():

    workflow = StateGraph(dict)

    workflow.add_node(
        "planner",
        planner_agent
    )

    workflow.add_node(
        "researcher",
        researcher_agent
    )

    workflow.add_node(
        "retriever",
        retriever_agent
    )

    workflow.add_node(
        "answer",
        answer_agent
    )

    workflow.add_node(
        "critic",
        critic_agent
    )

    workflow.set_entry_point("planner")

    workflow.add_edge(
        "planner",
        "researcher"
    )

    workflow.add_edge(
        "researcher",
        "retriever"
    )

    workflow.add_edge(
        "retriever",
        "answer"
    )

    workflow.add_edge(
        "answer",
        "critic"
    )


    # -----------------------------
    # Agent Loop
    # -----------------------------
    def should_continue(state):

        critique = state.get(
            "critique",
            ""
        )

        if "OK" in critique.upper():
            return END

        return "planner"


    workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        END: END,
        "planner": "planner"
    }
    )

    return workflow.compile()