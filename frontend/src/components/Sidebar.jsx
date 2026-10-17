function Sidebar({ page, setPage }) {
  return (
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
  )
}

export default Sidebar