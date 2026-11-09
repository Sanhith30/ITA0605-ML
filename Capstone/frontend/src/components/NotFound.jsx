import React from 'react';

function NotFound({ onHome }) {
  return (
    <div className="card" style={{
      maxWidth: 600,
      margin: '60px auto',
      textAlign: 'center',
      padding: '48px 32px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 16,
    }}>
      <div style={{
        fontSize: '4.5rem',
        fontWeight: 700,
        fontFamily: 'var(--font-serif)',
        color: 'var(--text-muted)',
        lineHeight: 1,
      }}>
        404
      </div>
      <h2 style={{ fontSize: '1.5rem', color: 'var(--text-ink)' }}>Page Not Found</h2>
      <p style={{ color: 'var(--text-muted)', fontSize: 13.5, maxWidth: 420 }}>
        The requested route or diagnostic view does not exist on this PhishShield instance.
      </p>
      <button
        type="button"
        onClick={onHome}
        className="btn btn-primary"
        style={{ marginTop: 8 }}
      >
        Return to Diagnostic Scanner
      </button>
    </div>
  );
}

export default NotFound;
