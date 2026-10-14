import { useState } from 'react'
import Papa from 'papaparse'
const REQUIRED_COLUMNS = [
  'customer_id',
  'age',
  'past_spend',
  'visits_per_month',
  'tenure_months',
  'region',
  'discount_given',
  'purchased',
]

function App() {
  const [page, setPage] = useState('upload')
  const [fileName, setFileName] = useState('')
  const [rows, setRows] = useState([])
  const [columns, setColumns] = useState([])
  const [error, setError] = useState('')
  const [budget, setBudget] = useState('5000')
  const [budgetError, setBudgetError] = useState('')
  const [savedBudget, setSavedBudget] = useState(null)

    function handleFileChange(event) {
    const file = event.target.files[0]
    if (!file) return

    setFileName(file.name)
    setError('')
    setRows([])
    setColumns([])

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        const fields = result.meta.fields
        const missing = REQUIRED_COLUMNS.filter((col) => !fields.includes(col))

        if (missing.length > 0) {
          setError('Missing required columns: ' + missing.join(', '))
          return
        }

        setRows(result.data)
        setColumns(fields)
      },
    })
  }
    function handleSaveBudget() {
    const value = Number(budget)

    if (budget.trim() === '' || Number.isNaN(value)) {
      setBudgetError('Please enter a budget amount.')
      return
    }
    if (value <= 0) {
      setBudgetError('Budget must be greater than 0.')
      return
    }

    setBudgetError('')
    setSavedBudget(value)
  }
  return (
    <div className="layout">
      <div className="sidebar">
        <h2>EconoCausal</h2>
        <button
          className={page === 'upload' ? 'nav-item active' : 'nav-item'}
          onClick={() => setPage('upload')}
        >
          Upload Data
        </button>
        <button
          className={page === 'budget' ? 'nav-item active' : 'nav-item'}
          onClick={() => setPage('budget')}
        >
          Set Budget
        </button>
        <button className="nav-item" disabled>Uplift Curves (soon)</button>
        <button className="nav-item" disabled>Prescription (soon)</button>
      </div>

      <div className="content">
        <div className="header">
          <h1>EconoCausal Dashboard</h1>
          <p>Dynamic Pricing using Double Machine Learning</p>
        </div>
        <div className="main">
          {page === 'upload' && (
            <div>
              <h2>Upload Historical Campaign Data</h2>
              <input type="file" accept=".csv" onChange={handleFileChange} />
              {error && <p className="error-box">{error}</p>}
                {fileName && !error && (
                <p className="file-info">
                  File: <strong>{fileName}</strong> | Rows: <strong>{rows.length}</strong> | Columns: <strong>{columns.length}</strong>
                </p>
              )}

              {rows.length > 0 && (
                <div className="table-wrapper">
                  <table className="preview-table">
                    <thead>
                      <tr>
                        {columns.map((col) => (
                          <th key={col}>{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {rows.slice(0, 10).map((row, index) => (
                        <tr key={index}>
                          {columns.map((col) => (
                            <td key={col}>{row[col]}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
          {page === 'budget' && (
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
      <button className="save-btn" onClick={handleSaveBudget}>
        Save Budget
      </button>
      {budgetError && <p className="error-box">{budgetError}</p>}
    </div>

    {savedBudget !== null && (
      <div className="summary-card">
        <strong>Budget: ${savedBudget.toLocaleString()}</strong>
        {' | '}
        Customers uploaded: <strong>{rows.length}</strong>
      </div>
    )}
  </div>
)}
        </div>
      </div>
    </div>
  )
}

export default App