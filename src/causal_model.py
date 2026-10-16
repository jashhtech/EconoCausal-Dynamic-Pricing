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

# Check that DoWhy can parse the graph
model = CausalModel(
    data=None,
    treatment="DiscountReceived",
    outcome="Purchase",
    graph=causal_graph
)

print("Causal graph definition created successfully!")
print("\nTreatment: DiscountReceived")
print("Outcome: Purchase")
print("Potential confounders: PastPurchases, PastSpending")