from dowhy import CausalModel

# Preliminary causal graph assumptions
causal_graph = """
digraph {
    PastPurchases -> DiscountReceived;
    PastPurchases -> Purchase;
    PastSpending -> DiscountReceived;
    PastSpending -> Purchase;
    DiscountReceived -> Purchase;
}
"""

print("Causal graph defined successfully!")

print(causal_graph)