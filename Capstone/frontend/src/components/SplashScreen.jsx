import React, { useState, useEffect } from 'react';

const NODES = [
  { id: '01', title: 'LEXICAL_EXTRACTOR', label: '21 URL Attributes', targetProgress: 25 },
  { id: '02', title: 'DOM_STRUCTURE', label: '20 HTML Indicators', targetProgress: 50 },
  { id: '03', title: 'RF_ENSEMBLE', label: '100 Decision Trees', targetProgress: 75 },
  { id: '04', title: 'TREE_SHAP', label: 'Local Explainability', targetProgress: 98 },
];

function SplashScreen({ onComplete }) {
  const [fading, setFading] = useState(false);
  const [progress, setProgress] = useState(8);
  const [activeNodeIndex, setActiveNodeIndex] = useState(0);
  const [tilt, setTilt] = useState({ x: 8, y: -6 });

  const dismiss = () => {
    setFading(true);
    setTimeout(() => {
      if (onComplete) onComplete();
    }, 400);
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') dismiss();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Mouse Parallax 3D tilt handler
  const handleMouseMove = (e) => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const mouseX = e.clientX - width / 2;
    const mouseY = e.clientY - height / 2;
    const maxTilt = 18;
    const tiltX = (mouseY / (height / 2)) * -maxTilt;
    const tiltY = (mouseX / (width / 2)) * maxTilt;
    setTilt({ x: Math.round(tiltX), y: Math.round(tiltY) });
  };

  useEffect(() => {
    const startTime = Date.now();
    const totalDuration = 1450;

    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const pct = Math.min(100, Math.round((elapsed / totalDuration) * 100));
      setProgress(pct);

      if (pct >= 90) {
        setActiveNodeIndex(3);
      } else if (pct >= 65) {
        setActiveNodeIndex(2);
      } else if (pct >= 35) {
        setActiveNodeIndex(1);
      } else {
        setActiveNodeIndex(0);
      }

      if (elapsed >= totalDuration) {
        clearInterval(timer);
        setTimeout(() => {
          dismiss();
        }, 280);
      }
    }, 30);

    return () => clearInterval(timer);
  }, []);

  return (
    <div
      className={`splash-overlay ${fading ? 'fading' : ''}`}
      onMouseMove={handleMouseMove}
      role="dialog"
      aria-label="System Initializing"
    >
      {/* Top Controls: Escape Pill */}
      <div style={{ position: 'absolute', top: 24, right: 28 }}>
        <button
          type="button"
          onClick={dismiss}
          className="btn btn-secondary"
          style={{
            fontSize: 11,
            fontFamily: 'var(--font-mono)',
            padding: '4px 10px',
            borderRadius: 'var(--radius-xs)',
            letterSpacing: '0.04em',
          }}
        >
          SKIP BOOT [ESC]
        </button>
      </div>

      {/* Main 3D Perspective Viewport */}
      <div className="splash-3d-stage">
        <div
          className="splash-3d-card"
          style={{
            transform: `rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
          }}
        >
          {/* 3D Multi-Ring Gyroscope and Shield Core */}
          <div className="gyro-container">
            {/* Outer 3D Gyro Ring */}
            <div className="gyro-ring gyro-ring-outer" />

            {/* Mid Gyro Ring */}
            <div className="gyro-ring gyro-ring-mid" />

            {/* Core Floating Shield Plate */}
            <div className="gyro-core-plate">
              {/* Sweeping Laser Line */}
              <div className="laser-sweep-line" />

              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
            </div>
          </div>

          {/* Brand Header */}
          <h1 style={{
            fontSize: '1.75rem',
            fontWeight: 800,
            letterSpacing: '0.14em',
            textTransform: 'uppercase',
            color: 'var(--text-ink)',
            lineHeight: 1.1,
            fontFamily: 'var(--font-sans)',
            marginBottom: 6,
          }}>
            PhishShield
          </h1>

          <div style={{
            fontSize: 10.5,
            fontWeight: 700,
            color: 'var(--text-muted)',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            fontFamily: 'var(--font-mono)',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
          }}>
            <span>SYSTEM // PHISHSHIELD-ENGINE-V2.4</span>
            <span style={{ color: 'var(--accent)' }}>&bull;</span>
            <span>41-DIM SCHEMA</span>
          </div>

          {/* Precision Hairline Progress Bar */}
          <div className="splash-progress-track">
            <div
              className="splash-progress-bar"
              style={{ width: `${progress}%` }}
            />
          </div>

          {/* Telemetry Progress Readout */}
          <div style={{
            width: '100%',
            maxWidth: 480,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: 11,
            fontFamily: 'var(--font-mono)',
            color: 'var(--text-muted)',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span className="heartbeat-dot" style={{ width: 6, height: 6 }} />
              <span>BOOT CALIBRATION</span>
            </div>
            <div style={{ fontWeight: 700, color: 'var(--text-ink)' }}>
              {progress}%
            </div>
          </div>

          {/* 4-Node Live Diagnostic Pipeline Grid */}
          <div className="diagnostic-node-grid">
            {NODES.map((node, i) => {
              const isPassed = progress >= node.targetProgress;
              const isCurrent = i === activeNodeIndex;

              return (
                <div
                  key={node.id}
                  className={`diagnostic-node ${isCurrent ? 'active' : ''}`}
                  style={{
                    borderLeft: isPassed ? '2px solid var(--accent)' : '1px solid var(--border-subtle)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ color: isPassed ? 'var(--accent)' : 'var(--text-faint)', fontWeight: 700 }}>
                      {node.id}
                    </span>
                    <span style={{
                      fontSize: 9,
                      color: isPassed ? 'var(--safe)' : 'var(--text-faint)',
                      fontWeight: 600,
                    }}>
                      {isPassed ? 'OK' : '..'}
                    </span>
                  </div>
                  <div style={{ fontWeight: 600, color: 'var(--text-ink)', marginTop: 2, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {node.title}
                  </div>
                  <div style={{ fontSize: 9.5, color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {node.label}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Minimal Benchmark Metadata */}
          <div style={{
            fontSize: 10,
            color: 'var(--text-faint)',
            marginTop: 18,
            letterSpacing: '0.04em',
            fontFamily: 'var(--font-mono)',
          }}>
            CORPUS: 235,795 PHIUSIIL URLS | RESCALE: MINMAX
          </div>
        </div>
      </div>
    </div>
  );
}

export default SplashScreen;
