function BudgetInput({
  budget,
  setBudget,
  budgetError,
  savedBudget,
  onSave,
  customerCount,
}) {
  return (
    <div>
      <h2>Set Marketing Budget</h2>

      <div className="budget-card">
        <label htmlFor="budget">Total budget ($)</label>
        <input
          id="budget"
          type="number"
          className="budget-input"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />
        <p className="hint">Discount options: $10 and $20</p>
        <button className="save-btn" onClick={onSave}>
          Save Budget
        </button>
        {budgetError && <p className="error-box">{budgetError}</p>}
      </div>

      {savedBudget !== null && (
        <div className="summary-card">
          <strong>Budget: ${savedBudget.toLocaleString()}</strong>
          {' | '}
          Customers uploaded: <strong>{customerCount}</strong>
        </div>
      )}
    </div>
  )
}

export default BudgetInput