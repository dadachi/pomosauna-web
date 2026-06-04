# Security Policy

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

The preferred way to report a vulnerability is privately through GitHub:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability** to open a private security advisory.

If you can't use the advisory flow, email **daisukeadachi@myturntag.com**
with the details instead.

Please include:

- A description of the issue and its impact.
- Steps to reproduce (a minimal proof of concept is ideal).
- Any affected URL, browser, or configuration.

You can expect an initial acknowledgement within a few days. Once a fix is
released we're happy to credit you, unless you'd prefer to stay anonymous.

## Scope

PomoSauna is a single static `index.html` served over GitHub Pages — no
backend, no accounts, and no server-side data. The only data it stores is your
sound preferences in `localStorage` (`pomosauna.prefs`), kept entirely in your
own browser.

Reports we're especially interested in:

- Cross-site scripting (XSS) or other client-side code execution.
- Supply-chain issues in the third-party snippets the page loads
  (e.g. the GoatCounter analytics script).
- Anything that could compromise a visitor's browser.
