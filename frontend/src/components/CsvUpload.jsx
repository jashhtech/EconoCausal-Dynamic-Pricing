import DataPreview from './DataPreview'

function CsvUpload({ fileName, rows, columns, error, onFileChange }) {
  return (
    <div>
      <h2>Upload Historical Campaign Data</h2>
      <input type="file" accept=".csv" onChange={onFileChange} />

      {error && <p className="error-box">{error}</p>}

      {fileName && !error && (
        <p className="file-info">
          File: <strong>{fileName}</strong> | Rows: <strong>{rows.length}</strong> | Columns: <strong>{columns.length}</strong>
        </p>
      )}

      {rows.length > 0 && <DataPreview columns={columns} rows={rows} />}
    </div>
  )
}

export default CsvUpload