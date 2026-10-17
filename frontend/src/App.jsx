import { useState } from 'react'
import Papa from 'papaparse'
import Sidebar from './components/Sidebar'
import BudgetInput from './components/BudgetInput'
import DataPreview from './components/DataPreview'
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
      <Sidebar page={page} setPage={setPage} />

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
                <DataPreview columns={columns} rows={rows} />
              )}
            </div>
          )}
          {page === 'budget' && (
  <BudgetInput
    budget={budget}
    setBudget={setBudget}
    budgetError={budgetError}
    savedBudget={savedBudget}
    onSave={handleSaveBudget}
    customerCount={rows.length}
  />
)}
        </div>
      </div>
    </div>
  )
}

export default App