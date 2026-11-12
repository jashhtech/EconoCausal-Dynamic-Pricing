import { useState } from 'react'
import Papa from 'papaparse'

// Real columns the dataset must contain (matches data/retail_data.csv)
const REQUIRED_COLUMNS = [
  'ID', 'age', 'Income', 'Kidhome', 'Teenhome', 'Recency',
  'Education', 'Marital_Status', 'campaign_exposure', 'campaign_response',
]

// Results from the team's scripts (results/*.csv, docs/week4_nuisance_evaluation.md)
const RAW_GAP = 0.4069 - 0.0823
const ROBUSTNESS = [
  { label: 'Baseline, Random Forest', est: 0.2835, lo: 0.2376, hi: 0.3293, n: 2237 },
  { label: 'Trim propensity 0.05 to 0.95', est: 0.2837, lo: 0.2373, hi: 0.3301, n: 2121 },
  { label: 'Trim propensity 0.10 to 0.90', est: 0.2795, lo: 0.2305, hi: 0.3285, n: 1670 },
  { label: 'Add purchase columns', est: 0.2473, lo: 0.1996, hi: 0.2949, n: 2237, flag: true },
  { label: 'Gradient Boosting models', est: 0.2672, lo: 0.2211, hi: 0.3132, n: 2237 },
  { label: 'Logistic models', est: 0.2943, lo: 0.2492, hi: 0.3395, n: 2237 },
]
const MODELS = {
  'Outcome: campaign_response': [
    ['Random Forest depth 10', 0.7809], ['Random Forest (selected)', 0.7780, true],
    ['Random Forest leaf 10', 0.7754], ['Gradient Boosting depth 2', 0.7741],
    ['Gradient Boosting', 0.7718], ['LightGBM small', 0.7725],
    ['Random Forest depth 5', 0.7699], ['LightGBM', 0.7661], ['Logistic regression', 0.7489],
  ],
  'Treatment: campaign_exposure': [
    ['Gradient Boosting depth 2', 0.7272], ['Random Forest depth 10', 0.7270],
    ['Random Forest (selected)', 0.7264, true], ['LightGBM small', 0.7244],
    ['Random Forest leaf 10', 0.7241], ['Gradient Boosting', 0.7238],
    ['Random Forest depth 5', 0.7236], ['Logistic regression', 0.7148], ['LightGBM', 0.7113],
  ],
}
const GROUPS = [
  { name: 'Exposed customers', n: 462, min: 0.0201, p25: 0.1502, med: 0.29, p75: 0.5113, max: 0.7895 },
  { name: 'Unexposed customers', n: 1775, min: 0.013, p25: 0.0926, med: 0.1432, p75: 0.216, max: 0.7525 },
]
const TRIM = [
  ['0.01 to 0.99', 2237, '100%', 0, 0],
  ['0.05 to 0.95', 2121, '94.8%', 11, 105],
  ['0.10 to 0.90', 1670, '74.7%', 51, 516],
]
const TABS = ['Findings', 'Data', 'Models', 'Overlap', 'Budget']

const CSS = `
.ec{--ink:#16233b;--soft:#5a6a82;--paper:#f3f5f8;--card:#fff;--line:#dbe1ea;--teal:#0e7c7b;--amber:#b4580c;--wash:#e6f2f1;
min-height:100vh;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
.ec *{box-sizing:border-box}
.ec h1,.ec h2,.ec h3{font-family:Georgia,"Iowan Old Style",Palatino,serif;font-weight:700;margin:0;letter-spacing:-.01em}
.ec header{background:var(--ink);color:#fff;padding:22px 32px 0}
.ec .brand{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.ec .brand h1{font-size:28px}
.ec .brand span{color:#aebbd0;font-size:14px}
.ec nav{display:flex;gap:4px;margin-top:18px;overflow-x:auto}
.ec nav button{background:none;border:0;color:#aebbd0;font:inherit;font-size:15px;padding:10px 16px;cursor:pointer;border-bottom:3px solid transparent}
.ec nav button:hover{color:#fff}
.ec nav button[aria-current=page]{color:#fff;border-color:#5fd0cd;font-weight:600}
.ec button:focus-visible,.ec input:focus-visible{outline:3px solid #5fd0cd;outline-offset:2px}
.ec main{max-width:1040px;margin:0 auto;padding:32px 24px 64px}
.ec h2{font-size:26px;margin-bottom:6px}
.ec .lead{color:var(--soft);max-width:68ch;margin:0 0 24px}
.ec .panel{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:22px;margin-bottom:20px}
.ec .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:20px}
.ec .stat{border-left:4px solid var(--teal);padding:4px 0 4px 14px}
.ec .stat.warn{border-color:var(--amber)}
.ec .stat b{display:block;font:700 28px/1.2 Georgia,serif}
.ec .stat span{color:var(--soft);font-size:14px}
.ec .note{background:#fdf3e8;border:1px solid #f0d3b3;border-radius:8px;padding:16px 20px}
.ec .note ul{margin:8px 0 0;padding-left:20px}
.ec table{width:100%;border-collapse:collapse;font-size:14px}
.ec th,.ec td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}
.ec th{color:var(--soft);font-weight:600}
.ec .scroll{overflow-x:auto}
.ec .drop{display:block;border:2px dashed var(--line);border-radius:8px;padding:28px;text-align:center;cursor:pointer;background:var(--card)}
.ec .drop:hover{border-color:var(--teal);background:var(--wash)}
.ec .err{background:#fdecec;border:1px solid #f3b9b9;color:#8a1c1c;border-radius:8px;padding:14px 18px;margin-top:16px}
.ec .ok{background:var(--wash);border:1px solid #b5dad8;color:#0b5a59;border-radius:8px;padding:14px 18px;margin-top:16px}
.ec .bars{display:grid;grid-template-columns:minmax(170px,230px) 1fr 56px;gap:8px 12px;align-items:center;font-size:14px}
.ec .bar{height:16px;background:#cfd8e3;border-radius:3px}
.ec .bar.sel{background:var(--teal)}
.ec .sel-l{font-weight:700}
.ec label{font-weight:600;display:block;margin-bottom:6px}
.ec input[type=number]{font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:6px;width:220px}
.ec .btn{font:inherit;font-weight:600;background:var(--teal);color:#fff;border:0;border-radius:6px;padding:10px 20px;cursor:pointer;margin-left:10px}
.ec .btn:hover{background:#0a6564}
.ec svg{width:100%;height:auto;display:block}
.ec svg text{font:13px system-ui,sans-serif;fill:var(--ink)}
.ec svg .dim{fill:var(--soft)}
@media (max-width:640px){.ec header{padding:18px 16px 0}.ec main{padding:24px 14px 48px}.ec .bars{grid-template-columns:1fr 1fr 48px}}
@media (prefers-reduced-motion:reduce){.ec *{transition:none!important}}
`

function ForestPlot() {
  const W = 760, L = 230, R = 24, T = 36, RH = 40
  const lo = 0.18, hi = 0.36
  const x = (v) => L + ((v - lo) / (hi - lo)) * (W - L - R)
  const rows = [{ label: 'Raw difference, no adjustment', raw: true }, ...ROBUSTNESS]
  const H = T + rows.length * RH + 34
  const ticks = [0.2, 0.24, 0.28, 0.32, 0.36]
  return (
    <svg viewBox={`0 0 ${W} ${H}`} role="img"
      aria-label="Estimated effect of prior campaign acceptance on response, six specifications with confidence intervals">
      {ticks.map((t) => (
        <g key={t}>
          <line x1={x(t)} x2={x(t)} y1={T - 10} y2={H - 30} stroke="#dbe1ea" />
          <text x={x(t)} y={H - 10} textAnchor="middle" className="dim">{t.toFixed(2)}</text>
        </g>
      ))}
      <text x={x(0.27)} y={16} textAnchor="middle" className="dim">Change in probability of responding</text>
      {rows.map((r, i) => {
        const y = T + i * RH + RH / 2
        return (
          <g key={r.label}>
            <text x={L - 14} y={y + 4} textAnchor="end">{r.label}</text>
            {r.raw ? (
              <>
                <circle cx={x(RAW_GAP)} cy={y} r="7" fill="#fff" stroke="#5a6a82" strokeWidth="2.5" />
                <text x={x(RAW_GAP) + 14} y={y + 4} className="dim">{RAW_GAP.toFixed(3)}</text>
              </>
            ) : (
              <>
                <line x1={x(r.lo)} x2={x(r.hi)} y1={y} y2={y} stroke={r.flag ? '#b4580c' : '#0e7c7b'} strokeWidth="3" />
                <circle cx={x(r.est)} cy={y} r="6" fill={r.flag ? '#b4580c' : '#0e7c7b'} />
                <text x={x(r.hi) + 10} y={y + 4} className="dim">{r.est.toFixed(3)}</text>
              </>
            )}
          </g>
        )
      })}
    </svg>
  )
}

function Findings() {
  return (
    <>
      <h2>Does earlier campaign acceptance still predict a response after adjustment?</h2>
      <p className="lead">
        Customers who accepted an earlier campaign respond far more often. Adjusting for age, income,
        household and recency shrinks that gap only a little, and every check keeps it clearly above zero.
      </p>
      <div className="stats">
        <div className="stat"><b>8.2% vs 40.7%</b><span>Response rate, unexposed (1,775) vs exposed (462)</span></div>
        <div className="stat"><b>+0.28</b><span>Adjusted estimate, baseline (95% interval 0.24 to 0.33)</span></div>
        <div className="stat warn"><b>−0.036</b><span>Shift when purchase columns are added back</span></div>
      </div>
      <div className="panel">
        <h3 style={{ fontSize: 18, marginBottom: 10 }}>Six ways to estimate it</h3>
        <ForestPlot />
        <p className="lead" style={{ margin: '10px 0 0', fontSize: 14 }}>
          Dots are estimates, lines are 95% intervals. The grey ring is the raw difference with no adjustment.
          The amber line is the one result that moves: it adds purchase columns whose timing is unknown.
        </p>
      </div>
      <div className="note">
        <b>Read these as preliminary estimates, not proven causal effects.</b>
        <ul>
          <li>The treatment is prior campaign acceptance (AcceptedCmp1 to 5), a stand-in for exposure. No assigned discount exists in this dataset.</li>
          <li>Customers who accepted earlier may simply be more responsive, and that is not among the measured confounders.</li>
          <li>The data has no timestamps, so purchase columns cannot be confirmed as measured before exposure.</li>
        </ul>
      </div>
    </>
  )
}

function DataPage() {
  const [state, setState] = useState(null)
  const [error, setError] = useState('')
  function onFile(e) {
    const file = e.target.files[0]
    if (!file) return
    setError(''); setState(null)
    Papa.parse(file, {
      header: true, skipEmptyLines: true, dynamicTyping: true,
      complete: (res) => {
        const cols = res.meta.fields || []
        const missing = REQUIRED_COLUMNS.filter((c) => !cols.includes(c))
        if (missing.length) { setError(`Missing required columns: ${missing.join(', ')}. Upload data/retail_data.csv or a file with these columns.`); return }
        const rows = res.data
        const rate = (k) => {
          const g = rows.filter((r) => r.campaign_exposure === k)
          return { n: g.length, rate: g.length ? g.reduce((s, r) => s + (r.campaign_response === 1 ? 1 : 0), 0) / g.length : 0 }
        }
        setState({ name: file.name, rows, cols: cols.length, ex: rate(1), un: rate(0) })
      },
      error: (err) => setError(`Could not read the file: ${err.message}`),
    })
  }
  const show = ['ID', 'age', 'Income', 'Education', 'campaign_exposure', 'campaign_response']
  return (
    <>
      <h2>Check your campaign data</h2>
      <p className="lead">Upload the historical campaign file. The dashboard checks the columns the models need and summarises who was exposed and who responded.</p>
      <label className="drop">
        <input type="file" accept=".csv" onChange={onFile} style={{ display: 'none' }} />
        <b>{state ? state.name : 'Choose a CSV file'}</b>
        <div style={{ color: 'var(--soft)', fontSize: 14 }}>Try data/retail_data.csv from the repository</div>
      </label>
      {error && <div className="err" role="alert">{error}</div>}
      {state && (
        <>
          <div className="ok">All {REQUIRED_COLUMNS.length} required columns found.</div>
          <div className="stats" style={{ marginTop: 20 }}>
            <div className="stat"><b>{state.rows.length.toLocaleString()}</b><span>Customers, {state.cols} columns</span></div>
            <div className="stat"><b>{(state.ex.rate * 100).toFixed(1)}%</b><span>Respond among exposed ({state.ex.n})</span></div>
            <div className="stat"><b>{(state.un.rate * 100).toFixed(1)}%</b><span>Respond among unexposed ({state.un.n})</span></div>
          </div>
          <div className="panel scroll">
            <table>
              <thead><tr>{show.map((c) => <th key={c}>{c}</th>)}</tr></thead>
              <tbody>{state.rows.slice(0, 6).map((r, i) => <tr key={i}>{show.map((c) => <td key={c}>{String(r[c])}</td>)}</tr>)}</tbody>
            </table>
          </div>
        </>
      )}
    </>
  )
}

function Models() {
  return (
    <>
      <h2>Which models predict best?</h2>
      <p className="lead">Each bar is a 5-fold cross-fitted AUC (higher is better). Differences between the top models are about 0.003, within noise for one split, so Random Forest stays the default for both.</p>
      {Object.entries(MODELS).map(([title, list]) => (
        <div className="panel" key={title}>
          <h3 style={{ fontSize: 18, marginBottom: 12 }}>{title}</h3>
          <div className="bars">
            {list.map(([name, auc, sel]) => (
              <Row key={name} name={name} auc={auc} sel={sel} />
            ))}
          </div>
        </div>
      ))}
    </>
  )
}
function Row({ name, auc, sel }) {
  const w = Math.max(2, ((auc - 0.7) / 0.1) * 100)
  return (
    <>
      <span className={sel ? 'sel-l' : ''}>{name}</span>
      <div style={{ background: '#eef1f6', borderRadius: 3 }}><div className={'bar' + (sel ? ' sel' : '')} style={{ width: w + '%' }} /></div>
      <span>{auc.toFixed(4)}</span>
    </>
  )
}

function Overlap() {
  const W = 760, L = 170, sx = (v) => L + (v / 0.8) * (W - L - 20)
  return (
    <>
      <h2>Do exposed and unexposed customers look comparable?</h2>
      <p className="lead">Propensity scores show how likely each customer was to be exposed. Both groups cover almost the whole range, so comparison is possible, though few customers score below 0.05.</p>
      <div className="panel">
        <svg viewBox={`0 0 ${W} 190`} role="img" aria-label="Propensity score ranges for exposed and unexposed customers">
          {[0, 0.2, 0.4, 0.6, 0.8].map((t) => (
            <g key={t}><line x1={sx(t)} x2={sx(t)} y1="14" y2="140" stroke="#dbe1ea" /><text x={sx(t)} y="164" textAnchor="middle" className="dim">{t.toFixed(1)}</text></g>
          ))}
          {GROUPS.map((g, i) => {
            const y = 44 + i * 58
            const c = i === 0 ? '#0e7c7b' : '#5a6a82'
            return (
              <g key={g.name}>
                <text x={L - 12} y={y + 4} textAnchor="end">{g.name}</text>
                <line x1={sx(g.min)} x2={sx(g.max)} y1={y} y2={y} stroke={c} strokeWidth="2" />
                <rect x={sx(g.p25)} y={y - 13} width={sx(g.p75) - sx(g.p25)} height="26" fill={c} opacity="0.25" stroke={c} />
                <line x1={sx(g.med)} x2={sx(g.med)} y1={y - 13} y2={y + 13} stroke={c} strokeWidth="3" />
              </g>
            )
          })}
        </svg>
        <p className="lead" style={{ margin: '4px 0 0', fontSize: 14 }}>Line: full range. Box: middle half of customers. Tick: median (exposed 0.29, unexposed 0.14).</p>
      </div>
      <div className="panel scroll">
        <h3 style={{ fontSize: 18, marginBottom: 8 }}>What if extreme scores are trimmed?</h3>
        <table>
          <thead><tr><th>Keep scores between</th><th>Customers kept</th><th>Share</th><th>Exposed dropped</th><th>Unexposed dropped</th></tr></thead>
          <tbody>{TRIM.map((t) => <tr key={t[0]}>{t.map((c, i) => <td key={i}>{c}</td>)}</tr>)}</tbody>
        </table>
        <p className="lead" style={{ margin: '10px 0 0', fontSize: 14 }}>Trimming changes the estimate by less than 0.005, so thin overlap is not driving the result.</p>
      </div>
    </>
  )
}

function Budget() {
  const [value, setValue] = useState('5000')
  const [saved, setSaved] = useState(null)
  const [err, setErr] = useState('')
  function save() {
    const n = Number(value)
    if (!value || Number.isNaN(n) || n <= 0) { setErr('Enter a budget greater than 0.'); setSaved(null); return }
    setErr(''); setSaved(n)
  }
  return (
    <>
      <h2>Set the campaign budget</h2>
      <p className="lead">The budget is the limit the optimiser will spend. Discount allocation is built after the treatment definition and effect estimates are final.</p>
      <div className="panel">
        <label htmlFor="budget">Total budget (USD)</label>
        <input id="budget" type="number" min="1" value={value} onChange={(e) => setValue(e.target.value)} />
        <button className="btn" onClick={save}>Save budget</button>
        {err && <div className="err" role="alert">{err}</div>}
        {saved && <div className="ok">Budget saved: ${saved.toLocaleString()}</div>}
      </div>
    </>
  )
}

export default function App() {
  const [tab, setTab] = useState('Findings')
  const pages = { Findings: <Findings />, Data: <DataPage />, Models: <Models />, Overlap: <Overlap />, Budget: <Budget /> }
  return (
    <div className="ec">
      <style>{CSS}</style>
      <header>
        <div className="brand"><h1>EconoCausal</h1><span>Dynamic pricing with Double Machine Learning</span></div>
        <nav aria-label="Sections">
          {TABS.map((t) => (
            <button key={t} aria-current={tab === t ? 'page' : undefined} onClick={() => setTab(t)}>{t}</button>
          ))}
        </nav>
      </header>
      <main>{pages[tab]}</main>
    </div>
  )
}
