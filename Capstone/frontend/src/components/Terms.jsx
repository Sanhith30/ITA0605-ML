import React from 'react';

function Terms() {
  return (
    <div style={{ maxWidth: 860, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* Masthead */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div className="badge badge-neutral" style={{ width: 'fit-content' }}>
          Terms of Service & Licensing
        </div>
        <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-ink)', letterSpacing: '-0.025em' }}>
          Terms and Conditions
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
            Core terms governing usage of the PhishShield platform
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 14 }}>
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--safe)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Defensive Research Scope</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              The platform is provided for security research, defensive testing, threat triage, and educational benchmarking.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--accent)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Fair Use Rate Limits</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              A ceiling of 30 requests per minute per IP address is enforced to guarantee fair access and protect API availability.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: 'var(--warn)' }} />
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>MIT Academic License</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Software source code and feature schemas are licensed under the MIT License for open academic study and reproducible validation.
            </p>
          </div>
        </div>
      </div>

      {/* Main Terms Content */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            1. Acceptance of Terms
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            By accessing or using the PhishShield detection console, REST API endpoints, or Chrome extension, you agree to comply with these terms of use. This platform is provided for research, testing, and defensive cybersecurity threat evaluation.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            2. Acceptable Use Policy
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            Users of this system agree not to:
          </p>
          <ul style={{ paddingLeft: 22, display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, color: 'var(--text-body)', lineHeight: 1.5 }}>
            <li>
              Attempt denial-of-service, automated flood attacks, or resource exhaustion against the diagnostic API endpoints.
            </li>
            <li>
              Circumvent client or server rate limiting controls (30 requests per minute ceiling).
            </li>
            <li>
              Use the headless crawler service to violate third-party terms of service or scrape copyrighted intellectual property.
            </li>
            <li>
              Rely entirely on automated machine learning output for mission-critical, legal, medical, or life-safety authorization decisions without secondary human verification.
            </li>
          </ul>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            3. Research Model Disclaimer
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            While our deployed Random Forest ensemble maintains verified high test precision (99.98% accuracy on the PhiUSIIL benchmark), all heuristic machine learning models produce probabilistic classifications. PhishShield provides risk indices as an auxiliary diagnostic tool and disclaims express warranties of zero false positives or zero false negatives.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            4. Attribution and Dataset Reference
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            The 41-feature extraction schema and training corpora cite the UCI Machine Learning Repository PhiUSIIL Phishing URL Dataset (235,795 labeled records). The platform software codebase is distributed under the open MIT Academic License.
          </p>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: 10, borderTop: '1px solid var(--border-subtle)', paddingTop: 16 }}>
          <h2 style={{ fontSize: 15, fontWeight: 700, color: 'var(--text-ink)' }}>
            5. Contact and Inquiries
          </h2>
          <p style={{ fontSize: 13, color: 'var(--text-body)', lineHeight: 1.6 }}>
            Questions regarding licensing, custom enterprise deployments, or academic collaboration should be directed to the project maintainer:
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
              <span style={{ color: 'var(--text-muted)', minWidth: 60, fontWeight: 600 }}>License:</span>
              <span style={{ color: 'var(--text-body)' }}>MIT Academic License</span>
            </div>
          </div>
        </section>
      </div>

    </div>
  );
}

export default Terms;
