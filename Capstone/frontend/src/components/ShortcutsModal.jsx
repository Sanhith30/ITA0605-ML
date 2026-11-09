import React, { useEffect } from 'react';

const SHORTCUTS = [
  { key: '1', action: 'Go to Diagnostic Scanner' },
  { key: '2', action: 'Go to Research & Benchmarks' },
  { key: '3', action: 'Go to Deployment & Pricing' },
  { key: '4', action: 'Go to Custom Domain Setup' },
  { key: '5', action: 'Go to Privacy Policy' },
  { key: '6', action: 'Go to Terms & Conditions' },
  { key: 'S', action: 'Focus URL Scanner Input' },
  { key: 'B', action: 'Toggle Single / Batch URL Mode' },
  { key: 'L', action: 'Toggle Feature Simulation Lab' },
  { key: 'T', action: 'Toggle Dark / Light Mode' },
  { key: '?', action: 'Open / Close Shortcuts Palette' },
  { key: 'Esc', action: 'Dismiss Dialog / Modal' },
];

function ShortcutsModal({ isOpen, onClose }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        background: 'rgba(0, 0, 0, 0.65)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
      }}
      onClick={onClose}
      role="dialog"
      aria-label="Keyboard Shortcuts"
    >
      <div
        className="card"
        style={{
          maxWidth: 500,
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          gap: 18,
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.5)',
          border: '1px solid var(--border-strong)',
        }}
        onClick={e => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-subtle)', paddingBottom: 12 }}>
          <div>
            <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-muted)' }}>
              Developer Navigation
            </div>
            <h3 style={{ fontSize: '1.25rem', marginTop: 2 }}>
              Keyboard Shortcuts
            </h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="btn btn-quiet"
            style={{ fontSize: 16, padding: '4px 8px' }}
            aria-label="Close dialog"
          >
            &times;
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 380, overflowY: 'auto' }}>
          {SHORTCUTS.map((item, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '6px 10px',
                background: 'var(--bg-subtle)',
                borderRadius: 'var(--radius-xs)',
                border: '1px solid var(--border-subtle)',
              }}
            >
              <span style={{ fontSize: 13, color: 'var(--text-body)' }}>
                {item.action}
              </span>
              <kbd style={{
                fontFamily: 'var(--font-mono)',
                fontSize: 11,
                fontWeight: 700,
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-strong)',
                borderRadius: 'var(--radius-xs)',
                padding: '2px 8px',
                color: 'var(--text-ink)',
                boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
              }}>
                {item.key}
              </kbd>
            </div>
          ))}
        </div>

        <div style={{ fontSize: 11.5, color: 'var(--text-muted)', borderTop: '1px solid var(--border-subtle)', paddingTop: 10, display: 'flex', justifyContent: 'space-between' }}>
          <span>Press [Esc] or click outside to dismiss</span>
          <span style={{ fontFamily: 'var(--font-mono)' }}>PhishShield v2.4.1</span>
        </div>
      </div>
    </div>
  );
}

export default ShortcutsModal;

