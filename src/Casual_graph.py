def save_causal_graph(output_path="docs/causal_dag.png"):
    import os

    graph = build_causal_graph()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pos = {
        "Past Purchases": (0, 1.5),
        "Past Spending": (0, -1.5),
        "Discount Received": (3, 1.5),
        "Purchase": (6, 0),
    }

    plt.figure(figsize=(13, 7))

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=4200,
        node_color="#DCEBFA",
        edgecolors="#315A7D",
        linewidths=1.8,
    )

    nx.draw_networkx_labels(
    graph,
    pos,
    labels={
        "Past Purchases": "Past\nPurchases",
        "Past Spending": "Past\nSpending",
        "Discount Received": "Discount\nReceived",
        "Purchase": "Purchase",
    },
    font_size=9,
    font_weight="bold",
    verticalalignment="center",
)

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=24,
        width=1.8,
        edge_color="#526777",
        connectionstyle="arc3,rad=0.08",
        min_source_margin=28,
        min_target_margin=28,
    )

    plt.title(
        "EconoCausal — Initial Causal DAG (Week 1)",
        fontsize=16,
        fontweight="bold",
        pad=25,
    )

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Causal DAG saved to {output_path}")