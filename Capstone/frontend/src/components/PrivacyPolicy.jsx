import React from 'react';

function PrivacyPolicy() {
  return (
    <div style={{ maxWidth: 860, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* Masthead */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div className="badge badge-neutral" style={{ width: 'fit-content' }}>
          Data Governance & Privacy
        </div>
        <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-ink)', letterSpacing: '-0.025em' }}>
          Privacy Policy
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          Effective: November 2026. Academic Capstone Security Research Protocol.
        </p>
      </div>

      {/* At a Glance Summary Callout Box */}
      <div className="card" style={{ borderLeft: '4px solid var(--accent)', display: 'flex', flexDirection: 'column', gap: 14 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--accent)' }}>
            At a Glance
          </span>
          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
            Key privacy commitments of the PhishShield platform
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 14 }}>
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--safe)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Zero Cookie Tracking</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              No third-party tracking pixels, marketing beacons, or behavioral advertising cookies are used anywhere on this service.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--accent)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Strictly In-Memory Scans</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Submitted URLs and feature vectors are processed ephemerally in RAM during inspection. We do not persist submitted query strings to permanent databases.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--warn)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>No Credential Retention</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              The diagnostic crawler strictly checks structural HTML attributes (presence of tags). User credentials, passwords, session tokens, and POST bodies are never stored.
            </p>
          </div>
        </div>
      </div>

      {/* Main Policy Content */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            1. Scope and Research Purpose
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            PhishShield is an open-source cybersecurity research platform developed for real-time lexical and DOM-based phishing website detection. This policy outlines how URL inspection queries and telemetry data are handled during diagnostic operations across our web interface, API endpoints, and browser extension.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            2. Data Processed During Diagnostics
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            When a URL is submitted for evaluation via the scanner input or API:
          </p>
          <ul style={{ paddingLeft: 22, display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--text-body)', lineHeight: 1.5 }}>
            <li>
              <strong>Lexical Analysis:</strong> The URL string is parsed for character entropy, length ratios, delimiter frequencies, and suspicious keyword tokens.
            </li>
            <li>
              <strong>DOM Structure:</strong> If headless inspection is enabled, public HTML markup is fetched to compute structural ratios (count of forms, iframes, hyperlinks, and action targets).
            </li>
            <li>
              <strong>Model Inference:</strong> Extracted feature vectors are passed to our 100-tree Random Forest classifier and Tree SHAP explainer to calculate localized threat attribution.
            </li>
            <li>
              <strong>Zero Secret Capture:</strong> User login credentials, passwords, submitted form values, and private tokens are never accessed, captured, or retained.
            </li>
          </ul>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            3. Logging and Session State
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            Session scan histories displayed in the browser interface reside entirely in your local browser state. Query logs on the FastAPI runtime are limited to operational error debugging traces without persistent database recording of visitor IP addresses or identity.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            4. Local Storage and Client Preferences
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            PhishShield uses browser <code style={{ fontFamily: 'var(--font-mono)', fontSize: 12, background: 'var(--bg-subtle)', padding: '2px 5px', borderRadius: 'var(--radius-xs)' }}>localStorage</code> strictly to remember your interface preferences (such as Light or Dark color mode and session preferences). We do not deploy third-party advertising or cross-site tracking mechanisms.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 10, borderTop: '1px solid var(--border-subtle)', paddingTop: 16 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            5. Contact and Researcher Inquiries
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            For questions regarding our privacy protocol, academic research benchmarks, or dataset verification, contact the project maintainer directly:
          </p>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13, maxWidth: 440 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: 'var(--text-muted)', minWidth: 60, fontWeight: 600 }}>Email:</span>
              <a href="mailto:sanhithreddy5131@gmail.com" className="text-link" style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent)', fontWeight: 600 }}>
                sanhithreddy5131@gmail.com
              </a>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: 'var(--text-muted)', minWidth: 60, fontWeight: 600 }}>Phone:</span>
              <a href="tel:9381681832" className="text-link" style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-ink)', fontWeight: 600 }}>
                +91 9381681832
              </a>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ color: 'var(--text-muted)', minWidth: 60, fontWeight: 600 }}>Project:</span>
              <span style={{ color: 'var(--text-body)' }}>PhishShield URL Threat Intelligence Platform</span>
            </div>
          </div>
        </section>
      </div>

    </div>
  );
}

export default PrivacyPolicy;
