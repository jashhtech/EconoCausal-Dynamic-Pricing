"""
EconoCausal — Week 1: Initial causal graph (DAG)

IMPORTANT:
- This graph expresses initial causal assumptions, not facts proven by data.
- Confirm the variable names with the teammate preparing the dataset.
- Update the graph if the actual dataset uses different columns.
"""

import networkx as nx
import matplotlib.pyplot as plt


def build_causal_graph():
    graph = nx.DiGraph()

    graph.add_nodes_from([
        "Past Purchases",
        "Past Spending",
        "Discount Received",
        "Purchase",
    ])

    graph.add_edges_from([
        ("Past Purchases", "Discount Received"),
        ("Past Purchases", "Purchase"),
        ("Past Spending", "Discount Received"),
        ("Past Spending", "Purchase"),
        ("Discount Received", "Purchase"),
    ])
    return graph


def save_causal_graph(output_path="docs/causal_dag.png"):
    graph = build_causal_graph()
    pos = {
        "Past Purchases": (0, 1),
        "Past Spending": (0, -1),
        "Discount Received": (2, 1),
        "Purchase": (4, 0),
    }

    plt.figure(figsize=(11, 5.5))
    nx.draw_networkx_nodes(
        graph, pos, node_size=3300, node_color="#DCEBFA",
        edgecolors="#315A7D", linewidths=1.5
    )
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight="bold")
    nx.draw_networkx_edges(
        graph, pos, arrows=True, arrowstyle="-|>", arrowsize=22,
        width=1.8, edge_color="#526777",
        connectionstyle="arc3,rad=0.04",
        min_source_margin=22, min_target_margin=22
    )
    plt.title("EconoCausal — Initial Causal DAG (Week 1)",
              fontsize=15, fontweight="bold", pad=18)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    save_causal_graph()
    print("Causal DAG saved to docs/causal_dag.png")
