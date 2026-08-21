# Project Structure

```text
Prochure-Ai/
├── app.py                         # Flask entry point and compatibility/API routes
├── config.py                      # Environment-backed configuration
├── data/
│   ├── db.py                      # JSON request persistence adapter
│   ├── purchase_requests.json     # Demo request store
│   └── seed_data.py               # Demo Odoo/vendor/quotation data
├── services/
│   ├── ai_service.py              # AI explanation integration and fallback
│   ├── approval_engine.py         # Approval thresholds and authorization
│   ├── odoo_client.py             # Odoo/demo integration adapter
│   ├── risk_engine.py             # Procurement risk rules
│   └── vendor_scoring.py          # Recommendation scoring
├── static/
│   ├── css/
│   │   ├── app.css                # Authenticated workspace design system
│   │   ├── landing.css             # Public marketing visual system
│   │   └── style.css               # Legacy template compatibility styles
│   └── js/
│       ├── app.js                 # API-backed SPA views and interactions
│       └── dashboard.js            # Legacy dashboard compatibility script
├── templates/
│   ├── app.html                   # SPA shell for public and authenticated entry points
│   └── legacy Jinja views         # Compatibility pages during migration
├── docs/architecture/             # Architecture and migration documentation
└── test_*.py                      # Domain and workflow regression tests
```

## Runtime Boundaries

- Public marketing: `/`
- Authenticated SPA shell: `/dashboard`
- SPA API: `/api/*`
- Legacy page compatibility: existing `/purchase-requests`, `/approvals`, vendor, and detail routes
- Domain behavior: `services/`
- Persistence/integration adapters: `data/` and `services/odoo_client.py`

The API is the source of truth for the new frontend. The legacy templates are retained until feature parity and deployment migration are complete.
