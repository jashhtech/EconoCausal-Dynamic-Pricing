# EconoCausal Dashboard (Frontend)

React dashboard for **EconoCausal: Dynamic Pricing via Double Machine Learning**.
Built by Vridhi Gautam (branch: `vridhi-gautam`).

## Purpose
The marketing director uploads historical campaign data, sets a discount budget,
and (in later weeks) sees uplift curves and the optimal discount per customer.

## Tech stack
- React (Vite, JavaScript)
- PapaParse (CSV parsing, Week 1)
- Plotly.js (uplift/Qini curves, Week 2)

## Week 1 scope (Dashboard Scaffolding)
- [x] React app setup with Vite
- [x] Dashboard layout: sidebar, header, page switching
- [x] Historical campaign data upload (CSV) with preview table
- [x] Column validation with clear error messages
- [ ] Budget input (default 5000, no negative or empty values)
- [ ] Split into components (Sidebar, CsvUpload, DataPreview, BudgetInput)

## Planned CSV schema (to be confirmed with the data teammate)
customer_id, age, past_spend, visits_per_month, tenure_months,
region, discount_given, purchased

## Roadmap
- Week 2: Plotly Qini and uplift curves, filter thousands of ITE scores
- Week 3: Allocation matrix (customer and optimal discount)
- Week 4: Natural-language summaries, connect to REST API

## Run locally
1. Install Node.js
2. `cd frontend`
3. `npm install`
4. `npm run dev`
