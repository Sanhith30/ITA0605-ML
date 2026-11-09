import React, { useState } from 'react';

function Pricing({ onSelectPlan }) {
  const [billingCycle, setBillingCycle] = useState('monthly');

  const tiers = [
    {
      id: 'research',
      name: 'Academic and Research',
      tag: 'Open Source',
      price: '$0',
      period: 'perpetual',
      desc: 'Full model binaries and dataset access for university research, students, and defensive analysts.',
      features: [
        'Complete 235,795 URL PhiUSIIL dataset corpus',
        'Pre-trained Random Forest deployment model binaries',
        'FastAPI REST API source code with Tree SHAP',
        'Manifest V3 Chrome Extension client included',
        'Local inference with zero third-party telemetry',
        'Community GitHub repository support',
      ],
      limit: '30 queries / minute (local)',
      cta: 'Explore Open Repository',
      highlight: false,
    },
    {
      id: 'team',
      name: 'SecOps Gateway',
      tag: 'Managed Cloud',
      price: billingCycle === 'monthly' ? '$49' : '$39',
      period: 'per month',
      desc: 'Hosted high-throughput API gateway for security operation centers, email gateways, and firewalls.',
      features: [
        '100,000 hosted API threat evaluations per month',
        'Automated headless browser crawler for dynamic JS',
        'Real-time webhook notifications on Critical threats',
        'Sub-50ms inference latency guarantee',
        'Shared Slack and email technical support',
        '99.9% uptime service level agreement',
      ],
      limit: '600 queries / minute',
      cta: 'Request Gateway Access',
      highlight: true,
    },
    {
      id: 'enterprise',
      name: 'Enterprise Air-Gapped',
      tag: 'On-Premise',
      price: 'Custom',
      period: 'annual agreement',
      desc: 'Fully isolated deployment for banking, defense, and healthcare infrastructure with zero external egress.',
      features: [
        'Self-contained Docker container cluster deployment',
        'Custom model retraining on internal corporate URLs',
        'Direct SIEM connector for Splunk, Elastic, and Sentinel',
        'Unlimited internal network link inspections',
        'Dedicated onboarding engineer and model auditing',
        '24/7 emergency incident response channel',
      ],
      limit: 'Uncapped internal bandwidth',
      cta: 'Contact Security Team',
      highlight: false,
    },
  ];

  const comparisonRows = [
    { feature: 'Training Dataset Access (235k URLs)', research: 'Full CSV', team: 'Hosted Cloud', enterprise: 'Hosted + Internal' },
    { feature: 'Feature Extraction Indicators', research: '41 Features', team: '41 Features', enterprise: '41 + Custom Telemetry' },
    { feature: 'Tree SHAP Attribution Ledger', research: 'Local Engine', team: 'JSON API Stream', enterprise: 'SIEM Structured Feed' },
    { feature: 'Chrome Extension License', research: 'Unpacked Source', team: 'Enterprise Fleet Pack', enterprise: 'Custom Group Policy Pack' },
    { feature: 'Query Rate Ceiling', research: '30 / min', team: '600 / min', enterprise: 'Custom Uncapped' },
    { feature: 'Data Egress Policy', research: 'Zero (Local)', team: 'Encrypted TLS 1.3', enterprise: 'Strict Zero Egress' },
    { feature: 'Dedicated Engineer SLA', research: 'Community', team: '24 Hour Response', enterprise: '1 Hour Dedicated SLA' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 40, maxWidth: 1160, margin: '0 auto' }}>

      {/* Editorial Header */}
      <div style={{ textAlign: 'center', maxWidth: 720, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div className="badge badge-neutral" style={{ alignSelf: 'center' }}>
          Deployment Options
        </div>
        <h1 style={{ fontSize: '2.5rem', lineHeight: 1.15 }}>
          Transparent access for researchers, teams, and enterprises.
        </h1>
        <p style={{ fontSize: '1rem', color: 'var(--text-body)', lineHeight: 1.6 }}>
          PhishShield is rooted in open academic security research. Run the pre-trained weights locally at zero cost, or deploy our managed gateway for production firewall integration.
        </p>

        {/* Billing Toggle: Precise Border Style */}
        <div style={{
          display: 'inline-flex',
          alignSelf: 'center',
          marginTop: 12,
          background: 'var(--bg-subtle)',
          border: '1px solid var(--border-strong)',
          borderRadius: 'var(--radius-sm)',
          padding: 3,
        }}>
          <button
            type="button"
            onClick={() => setBillingCycle('monthly')}
            style={{
              padding: '6px 16px',
              fontFamily: 'var(--font-sans)',
              fontSize: 12.5,
              fontWeight: 600,
              background: billingCycle === 'monthly' ? 'var(--bg-surface)' : 'transparent',
              color: billingCycle === 'monthly' ? 'var(--text-ink)' : 'var(--text-muted)',
              border: billingCycle === 'monthly' ? '1px solid var(--border-strong)' : '1px solid transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
            }}
          >
            Monthly Billing
          </button>
          <button
            type="button"
            onClick={() => setBillingCycle('annual')}
            style={{
              padding: '6px 16px',
              fontFamily: 'var(--font-sans)',
              fontSize: 12.5,
              fontWeight: 600,
              background: billingCycle === 'annual' ? 'var(--bg-surface)' : 'transparent',
              color: billingCycle === 'annual' ? 'var(--text-ink)' : 'var(--text-muted)',
              border: billingCycle === 'annual' ? '1px solid var(--border-strong)' : '1px solid transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
            }}
          >
            Annual Billing (20% Savings)
          </button>
        </div>
      </div>

      {/* Grid: 3 Clean Pricing Tiers */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: 24,
        alignItems: 'stretch',
      }}>
        {tiers.map((tier) => (
          <div
            key={tier.id}
            className="card"
            style={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: 24,
              borderTop: tier.highlight ? '4px solid var(--accent)' : '1px solid var(--border-subtle)',
              background: tier.highlight ? '#ffffff' : 'var(--bg-surface)',
              position: 'relative',
            }}
          >
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-neutral" style={{ fontSize: 10 }}>
                  {tier.tag}
                </span>
                <span style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {tier.limit}
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.35rem', marginBottom: 6 }}>{tier.name}</h3>
                <p style={{ fontSize: 12.5, color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  {tier.desc}
                </p>
              </div>

              {/* Price Display */}
              <div style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: 16, marginTop: 4 }}>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
                  <span style={{ fontSize: '2.5rem', fontWeight: 700, fontFamily: 'var(--font-serif)', color: 'var(--text-ink)', lineHeight: 1 }}>
                    {tier.price}
                  </span>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                    / {tier.period}
                  </span>
                </div>
              </div>

              {/* Feature Bullet List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 4 }}>
                <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                  Included Capabilities
                </div>
                {tier.features.map((item, idx) => (
                  <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: 9, fontSize: 12.5, color: 'var(--text-body)', lineHeight: 1.4 }}>
                    <span style={{ color: 'var(--accent)', fontWeight: 700, fontSize: 11, marginTop: 1 }}>+</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* CTA Button */}
            <div style={{ paddingTop: 16, borderTop: '1px solid var(--border-subtle)' }}>
              {tier.id === 'research' ? (
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-secondary"
                  style={{ width: '100%' }}
                >
                  {tier.cta}
                </a>
              ) : tier.id === 'team' ? (
                <button
                  type="button"
                  onClick={() => onSelectPlan(tier.id)}
                  className="btn btn-primary"
                  style={{ width: '100%' }}
                >
                  {tier.cta}
                </button>
              ) : (
                <a
                  href="mailto:security@phishshield.org?subject=Enterprise%20Air-Gapped%20Deployment%20Inquiry"
                  className="btn btn-secondary"
                  style={{ width: '100%' }}
                >
                  {tier.cta}
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Feature Comparison Matrix */}
      <section className="card">
        <div style={{ marginBottom: 16, borderBottom: '1px solid var(--border-subtle)', paddingBottom: 12 }}>
          <h2 style={{ fontSize: '1.35rem' }}>Detailed Specification Matrix</h2>
          <p style={{ fontSize: 12.5, color: 'var(--text-muted)', marginTop: 4 }}>
            Direct architectural comparison between self-hosted research files and production gateway agreements.
          </p>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '38%' }}>Platform Specification</th>
                <th style={{ width: '20%' }}>Academic Research</th>
                <th style={{ width: '21%' }}>SecOps Gateway</th>
                <th style={{ width: '21%' }}>Enterprise Air-Gap</th>
              </tr>
            </thead>
            <tbody>
              {comparisonRows.map((row, idx) => (
                <tr key={idx} style={{ cursor: 'default' }}>
                  <td style={{ fontWeight: 600, color: 'var(--text-ink)' }}>{row.feature}</td>
                  <td style={{ fontSize: 12.5, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{row.research}</td>
                  <td style={{ fontSize: 12.5, color: 'var(--text-ink)', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>{row.team}</td>
                  <td style={{ fontSize: 12.5, color: 'var(--accent)', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>{row.enterprise}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Transparent Procurement FAQs */}
      <section className="card-subtle" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <h3 style={{ fontSize: '1.2rem' }}>Deployment and Licensing Questions</h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20 }}>
          <div>
            <h4 style={{ fontSize: 13, marginBottom: 4 }}>Can we run the model without cloud connectivity?</h4>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.55 }}>
              Yes. The deployment model binary (deployment_model.pkl) runs completely within local Python memory. It requires zero cloud connectivity or telemetry to generate classifications.
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: 13, marginBottom: 4 }}>How are false positives addressed?</h4>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.55 }}>
              The API maintains an embedded whitelist for verified global domains and allows corporate tenants to supply internal subnets to completely eliminate false flags on trusted systems.
            </p>
          </div>

          <div>
            <h4 style={{ fontSize: 13, marginBottom: 4 }}>Is there a minimum volume commitment?</h4>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.55 }}>
              No. Academic tiers remain permanently free under MIT licensing. SecOps Gateway plans can be initiated or cancelled on monthly billing cycles without lock-in.
            </p>
          </div>
        </div>
      </section>

    </div>
  );
}

export default Pricing;

