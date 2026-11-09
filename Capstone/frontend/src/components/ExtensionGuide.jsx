import React, { useState } from 'react';

function ExtensionGuide({ onHome }) {
  const [copiedPath, setCopiedPath] = useState(false);
  const extensionPath = 'c:\\ML Capstone\\chrome-extension';

  const copyPath = () => {
    navigator.clipboard?.writeText(extensionPath);
    setCopiedPath(true);
    setTimeout(() => setCopiedPath(false), 2000);
  };

  return (
    <div style={{ maxWidth: 880, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* Header */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
          <div className="badge badge-neutral">
            Browser Threat Sentinel
          </div>
          <span className="badge badge-safe">
            Manifest V3 Standard
          </span>
        </div>

        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--text-ink)', letterSpacing: '-0.025em' }}>
          PhishShield Chrome Extension
        </h1>
        <p style={{ color: 'var(--text-body)', fontSize: 13.5, lineHeight: 1.6 }}>
          Run real-time lexical threat evaluation and headless DOM inspection directly inside your Chromium browser tabs before entering credentials.
        </p>
      </div>

      {/* 3-Step Installation Guide */}
      <div className="card" style={{ borderLeft: '4px solid var(--accent)', display: 'flex', flexDirection: 'column', gap: 18 }}>
        <div>
          <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-ink)' }}>
            Quick Installation (Unpacked Developer Mode)
          </h2>
          <p style={{ fontSize: 12.5, color: 'var(--text-muted)', marginTop: 2 }}>
            The extension files are already built and bundled in your local workspace.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 14 }}>
          {/* Step 1 */}
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{
                width: 22,
                height: 22,
                borderRadius: 'var(--radius-xs)',
                background: 'var(--accent)',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 11,
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
              }}>
                1
              </span>
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Locate Folder</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Use the extension directory path located in your workspace:
            </p>
            <div style={{ display: 'flex', gap: 6, marginTop: 'auto' }}>
              <input
                type="text"
                readOnly
                value={extensionPath}
                className="input"
                style={{ fontSize: 11, fontFamily: 'var(--font-mono)', padding: '4px 8px', height: 32 }}
              />
              <button
                type="button"
                onClick={copyPath}
                className="btn btn-secondary"
                style={{ fontSize: 11, padding: '0 10px', height: 32, whiteSpace: 'nowrap' }}
              >
                {copiedPath ? 'Copied!' : 'Copy'}
              </button>
            </div>
          </div>

          {/* Step 2 */}
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{
                width: 22,
                height: 22,
                borderRadius: 'var(--radius-xs)',
                background: 'var(--accent)',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 11,
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
              }}>
                2
              </span>
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Open Extensions Tab</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              In Google Chrome, Brave, Chromium, or Microsoft Edge, navigate to:
            </p>
            <div style={{
              background: 'var(--bg-subtle)',
              border: '1px solid var(--border-subtle)',
              padding: '6px 10px',
              borderRadius: 'var(--radius-xs)',
              fontFamily: 'var(--font-mono)',
              fontSize: 11.5,
              color: 'var(--text-ink)',
              marginTop: 'auto',
            }}>
              chrome://extensions
            </div>
          </div>

          {/* Step 3 */}
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{
                width: 22,
                height: 22,
                borderRadius: 'var(--radius-xs)',
                background: 'var(--accent)',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 11,
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
              }}>
                3
              </span>
              <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Load Unpacked</strong>
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Toggle <strong>Developer mode</strong> in the top-right corner, click <strong>Load unpacked</strong>, and select the folder.
            </p>
            <div style={{ fontSize: 11, color: 'var(--safe)', fontWeight: 600, marginTop: 'auto' }}>
              &check; Extension active on all tabs immediately
            </div>
          </div>
        </div>
      </div>

      {/* Feature Capabilities */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-ink)' }}>
          Capabilities & Local Architecture
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 14 }}>
          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Zero Cloud Telemetry</strong>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              The extension communicates strictly with your local FastAPI engine (<code style={{ fontFamily: 'var(--font-mono)' }}>http://localhost:8000</code>). No browsing histories are transmitted to third parties.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Active Tab DOM Extraction</strong>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Automatically scans for cross-origin form post actions, suspicious iframes, and credential interception fields on active pages.
            </p>
          </div>

          <div className="card-inset" style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>Visual Risk Dial Popup</strong>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>
              Clicking the PhishShield shield icon in the browser toolbar instantly reveals the 0-100 risk score and top SHAP attribution factors.
            </p>
          </div>
        </div>
      </div>

      {/* Manifest V3 Specification Ledger */}
      <div className="card-subtle" style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div style={{ fontSize: 12, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)' }}>
          Manifest Specification Summary
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12, fontSize: 12 }}>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Specification:</span>
            <div style={{ fontWeight: 600, color: 'var(--text-ink)' }}>Manifest V3 (Chrome 88+)</div>
          </div>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Background Worker:</span>
            <div style={{ fontWeight: 600, color: 'var(--text-ink)' }}>Service Worker (background.js)</div>
          </div>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Permissions:</span>
            <div style={{ fontWeight: 600, color: 'var(--text-ink)' }}>activeTab, scripting, storage</div>
          </div>
          <div>
            <span style={{ color: 'var(--text-muted)' }}>Endpoint Access:</span>
            <div style={{ fontWeight: 600, color: 'var(--text-ink)' }}>http://localhost:8000/*</div>
          </div>
        </div>
      </div>

      {/* Return to Scanner */}
      <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
        <button
          type="button"
          onClick={onHome}
          className="btn btn-secondary"
          style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 16px', fontSize: 13 }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Return to Diagnostic Scanner
        </button>
      </div>

    </div>
  );
}

export default ExtensionGuide;

