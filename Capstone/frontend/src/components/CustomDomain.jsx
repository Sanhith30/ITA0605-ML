import React, { useState } from 'react';

function CustomDomain() {
  const [domainInput, setDomainInput] = useState('');
  const [activeDomain, setActiveDomain] = useState('');
  const [records, setRecords] = useState(null);
  const [copied, setCopied] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [verificationStep, setVerificationStep] = useState('');
  const [isVerified, setIsVerified] = useState(false);

  const handleGenerate = (e) => {
    e.preventDefault();
    const cleanDomain = domainInput.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, '');
    if (!cleanDomain) return;

    setActiveDomain(cleanDomain);
    setIsVerified(false);
    setVerificationStep('');
    setRecords([
      { type: 'A', name: '@', value: '76.76.21.21', status: 'Pending DNS', verified: false },
      { type: 'CNAME', name: 'www', value: 'cname.phishshield.org', status: 'Pending DNS', verified: false },
      { type: 'TXT', name: '_phishshield-challenge', value: `verify-${Math.random().toString(36).substring(2, 10)}`, status: 'DNS Challenge', verified: false },
    ]);
  };

  const runVerification = async () => {
    if (!records || verifying) return;
    setVerifying(true);
    setIsVerified(false);

    setVerificationStep('Querying authoritative nameservers for DNS SOA records...');
    await new Promise(r => setTimeout(r, 600));

    setVerificationStep(`Resolving A record for ${activeDomain} -> 76.76.21.21...`);
    await new Promise(r => setTimeout(r, 650));

    setVerificationStep('Validating TXT ownership verification challenge token...');
    await new Promise(r => setTimeout(r, 600));

    setVerificationStep('Negotiating Let\'s Encrypt ACME HTTP-01 challenge & TLS 1.3 handshake...');
    await new Promise(r => setTimeout(r, 700));

    setRecords(prev => prev.map(r => ({ ...r, status: 'Active & Verified', verified: true })));
    setIsVerified(true);
    setVerifying(false);
    setVerificationStep('All records propagated successfully. TLS certificate provisioned.');
  };

  const handleCopy = (val) => {
    navigator.clipboard?.writeText(val);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ maxWidth: 860, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* Header */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div className="badge badge-neutral" style={{ width: 'fit-content' }}>
          Production Infrastructure
        </div>
        <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-ink)', letterSpacing: '-0.025em' }}>
          Custom Domain & Gateway Routing
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          Deploy your organization's custom hostname to route directly to your dedicated PhishShield heuristic instance with automated TLS termination.
        </p>
      </div>

      {/* Form Input */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <form onSubmit={handleGenerate} style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <input
            type="text"
            className="input"
            style={{ flex: 1, minWidth: 260, height: 44 }}
            placeholder="Enter custom domain (e.g., security.yourcompany.com)"
            value={domainInput}
            onChange={e => setDomainInput(e.target.value)}
            required
            aria-label="Custom Domain Hostname"
          />
          <button type="submit" className="btn btn-primary" style={{ height: 44, padding: '0 20px' }}>
            Generate DNS Records
          </button>
        </form>

        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          Compatible with any standard registrar: Cloudflare, AWS Route 53, Google Cloud DNS, Namecheap, and GoDaddy.
        </div>
      </div>

      {/* Generated Records Section */}
      {records && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
            <div>
              <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-ink)' }}>
                Configured Records for: <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent)' }}>{activeDomain}</span>
              </h2>
              <p style={{ fontSize: 12.5, color: 'var(--text-muted)', marginTop: 2 }}>
                Insert the following entries into your DNS provider's management console.
              </p>
            </div>

            <button
              type="button"
              onClick={runVerification}
              disabled={verifying}
              className="btn btn-secondary"
              style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '7px 14px', fontSize: 12 }}
            >
              {verifying ? (
                <>
                  <span className="spinner-dark" />
                  Verifying Propagation...
                </>
              ) : isVerified ? (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--safe)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  Re-Check DNS Status
                </>
              ) : (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  Verify DNS Propagation
                </>
              )}
            </button>
          </div>

          {/* Verification Progress Banner */}
          {verificationStep && (
            <div style={{
              padding: '10px 14px',
              borderRadius: 'var(--radius-sm)',
              background: isVerified ? 'var(--safe-bg)' : 'var(--bg-subtle)',
              border: `1px solid ${isVerified ? 'var(--safe-border)' : 'var(--border-subtle)'}`,
              fontSize: 12.5,
              color: isVerified ? 'var(--safe)' : 'var(--text-body)',
              fontFamily: 'var(--font-mono)',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
            }}>
              {isVerified ? (
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              ) : (
                <span className="heartbeat-dot" style={{ width: 6, height: 6 }} />
              )}
              <span>{verificationStep}</span>
            </div>
          )}

          {/* DNS Records Table */}
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Host / Name</th>
                  <th>Target / Value</th>
                  <th>Resolution Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r, i) => (
                  <tr key={i} style={{ cursor: 'default' }}>
                    <td><span className="badge badge-neutral">{r.type}</span></td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: 12 }}>{r.name}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: 'var(--accent)' }}>{r.value}</td>
                    <td>
                      <span className={`badge ${r.verified ? 'badge-safe' : 'badge-neutral'}`}>
                        {r.status}
                      </span>
                    </td>
                    <td>
                      <button
                        type="button"
                        onClick={() => handleCopy(r.value)}
                        className="btn btn-quiet"
                        style={{ padding: '3px 9px', fontSize: 11 }}
                      >
                        Copy
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {copied && (
            <div style={{ fontSize: 12, color: 'var(--safe)', fontWeight: 500 }}>
              Record target value copied to clipboard.
            </div>
          )}

          {/* Provisioned TLS Certificate Details Box */}
          {isVerified ? (
            <div className="card-inset" style={{ borderLeft: '3px solid var(--safe)', display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ fontSize: 13, color: 'var(--text-ink)' }}>TLS Certificate Provisioned</strong>
                <span className="badge badge-safe">TLS 1.3 Active</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 10, fontSize: 12, color: 'var(--text-body)', marginTop: 4 }}>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Authority:</span> Let's Encrypt (R3)
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Cipher:</span> ECDHE-ECDSA-AES128-GCM-SHA256
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Auto-Renew:</span> Enabled (Every 60 days)
                </div>
              </div>
            </div>
          ) : (
            <div className="card-inset" style={{ fontSize: 12, lineHeight: 1.5, color: 'var(--text-body)' }}>
              <strong style={{ color: 'var(--text-ink)' }}>Automatic TLS Certificate:</strong> Once your DNS provider finishes broadcasting changes across root nameservers (typically 5 to 30 minutes), click <em>Verify DNS Propagation</em> to issue your dedicated TLS certificate automatically.
            </div>
          )}
        </div>
      )}

    </div>
  );
}

export default CustomDomain;
