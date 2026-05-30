# Web App Readiness

Review browser-facing apps and user flows.

## Evidence To Look For

- Core user journeys verified in a browser.
- Loading, empty, error, and success states.
- Responsive behavior for expected viewports.
- Basic accessibility: labels, focus, keyboard paths, contrast, semantic controls.
- Browser console free of release-relevant errors.
- Form validation and safe error messages.
- No server-only secrets in client bundles.
- Performance budget for initial load and key interactions.

## Findings To Flag

- Critical flows only tested through code inspection.
- Buttons or forms without disabled, loading, or error states.
- Mobile layout overlap or clipped text.
- Auth or payment flows with unclear failure behavior.
- Sensitive environment variables exposed to the client.
- Console errors during normal use.

## Ready Evidence

A web app is ready when target users can complete critical flows on expected devices with accessible, resilient, and observable behavior.
