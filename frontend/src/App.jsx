import { useState } from 'react'

function App() {
  const [page, setPage] = useState('upload')

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
          {page === 'upload' && <h2>Upload Data page</h2>}
          {page === 'budget' && <h2>Set Budget page</h2>}
        </div>
      </div>
    </div>
  )
}

export default App