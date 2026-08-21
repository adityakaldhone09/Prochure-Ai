# Refactoring Notes

## Completed

- Added a public landing route at `/`.
- Moved the authenticated dashboard entry point to `/dashboard`.
- Added an API boundary for auth, dashboard, requests, analysis, comparison, approvals, rejection, and vendor performance.
- Added a responsive SPA shell and a separate premium landing visual system.
- Added reduced-motion handling and scroll-triggered workflow reveals.
- Preserved legacy routes, service engines, Odoo adapter, JSON data, and existing response semantics.

## Compatibility

The legacy Jinja routes remain available so existing links, tests, and integrations do not break while the SPA is adopted. New UI actions use the explicit `/api/purchase-requests/...` endpoints. Existing `/api/approve/...` and `/api/reject/...` endpoints remain supported.

## Follow-up Migration

- Move route orchestration into Flask blueprints by domain (`auth`, `requests`, `vendors`, `approvals`, `dashboard`).
- Replace JSON persistence with SQLite/PostgreSQL and add migrations.
- Persist purchase orders and immutable audit events.
- Add CSRF protection and stronger production session configuration.
- Add automated browser tests for public landing, login, request creation, analysis, approval, rejection, and responsive breakpoints.
- Remove legacy templates only after browser parity is confirmed.
