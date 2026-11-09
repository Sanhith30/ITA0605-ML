import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics';
import Pricing from './components/Pricing';
import PrivacyPolicy from './components/PrivacyPolicy';
import Terms from './components/Terms';
import CustomDomain from './components/CustomDomain';
import ExtensionGuide from './components/ExtensionGuide';
import NotFound from './components/NotFound';
import SplashScreen from './components/SplashScreen';
import ShortcutsModal from './components/ShortcutsModal';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [showSplash, setShowSplash] = useState(true);
  const [showShortcuts, setShowShortcuts] = useState(false);

  // Theme Management (Carbon & Paper / Pure Obsidian)
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('phishshield_theme');
    if (saved === 'dark' || saved === 'light') return saved;
    if (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('phishshield_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  const [scanHistory, setScanHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('phishshield_scan_history');
      if (saved) return JSON.parse(saved);
    } catch (e) {
      console.error(e);
    }
    return [
      {
        id: '1',
        url: 'https://secure-login-paypal.com/signin',
        timestamp: '10 mins ago',
        prediction: 'Phishing',
        confidence: 98.4,
        risk_score: 96,
      },
      {
        id: '2',
        url: 'https://www.google.com',
        timestamp: '1 hour ago',
        prediction: 'Legitimate',
        confidence: 100.0,
        risk_score: 0,
      },
      {
        id: '3',
        url: 'http://mybank-update-alert.net/login.php',
        timestamp: '2 hours ago',
        prediction: 'Phishing',
        confidence: 88.5,
        risk_score: 75,
      },
    ];
  });

  useEffect(() => {
    try {
      localStorage.setItem('phishshield_scan_history', JSON.stringify(scanHistory));
    } catch (e) {
      console.error(e);
    }
  }, [scanHistory]);

  const addScanToHistory = (url, prediction, confidence, risk_score) => {
    const newScan = {
      id: Date.now().toString(),
      url,
      timestamp: 'Just now',
      prediction,
      confidence,
      risk_score,
    };
    setScanHistory(prev => [newScan, ...prev].slice(0, 20));
  };

  const clearScanHistory = () => {
    setScanHistory([]);
    try {
      localStorage.removeItem('phishshield_scan_history');
    } catch (e) {
      console.error(e);
    }
  };

  const navigateTo = (tab) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Global Keyboard Shortcuts Listener
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;

      if (e.key === '?' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) {
        e.preventDefault();
        setShowShortcuts(prev => !prev);
      } else if (e.key === '1') {
        navigateTo('dashboard');
      } else if (e.key === '2') {
        navigateTo('analytics');
      } else if (e.key === '3') {
        navigateTo('pricing');
      } else if (e.key === '4') {
        navigateTo('domain');
      } else if (e.key === '5') {
        navigateTo('privacy');
      } else if (e.key === '6') {
        navigateTo('terms');
      } else if (e.key === 't' || e.key === 'T') {
        toggleTheme();
      } else if (e.key === 's' || e.key === 'S') {
        e.preventDefault();
        document.getElementById('scanner-url-input')?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const totalThreats = scanHistory.filter(s => s.prediction === 'Phishing').length;

  const renderActiveView = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard scanHistory={scanHistory} addScanToHistory={addScanToHistory} clearScanHistory={clearScanHistory} onOpenExtension={() => navigateTo('extension')} />;
      case 'analytics':
        return <Analytics />;
      case 'pricing':
        return <Pricing onSelectPlan={(plan) => alert(`Gateway deployment inquiry initiated for: ${plan}. Contact security@phishshield.org to receive provisioned API keys.`)} />;
      case 'domain':
        return <CustomDomain />;
      case 'extension':
        return <ExtensionGuide onHome={() => navigateTo('dashboard')} />;
      case 'privacy':
        return <PrivacyPolicy />;
      case 'terms':
        return <Terms />;
      default:
        return <NotFound onHome={() => navigateTo('dashboard')} />;
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>

      {/* Shortcuts Command Palette Modal */}
      <ShortcutsModal isOpen={showShortcuts} onClose={() => setShowShortcuts(false)} />

      {/* Sovereign 3D Splash Screen */}
      {showSplash && (
        <SplashScreen onComplete={() => setShowSplash(false)} />
      )}

      {/* Executive Masthead */}
      <header style={{
        background: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
      }}>
        <div style={{
          maxWidth: 1240,
          margin: '0 auto',
          padding: '0 24px',
          height: 62,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 16,
        }}>

          {/* Publication-Grade Typographic Mark */}
          <a
            href="/"
            onClick={(e) => { e.preventDefault(); navigateTo('dashboard'); }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              textDecoration: 'none',
              flexShrink: 0,
            }}
          >
            <div style={{
              width: 34,
              height: 34,
              border: '1.5px solid var(--accent)',
              borderRadius: 'var(--radius-sm)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: 'var(--accent-subtle)',
            }}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
            </div>
            <div>
              <div style={{
                fontSize: 18,
                fontFamily: 'var(--font-sans)',
                fontWeight: 800,
                color: 'var(--text-ink)',
                lineHeight: 1.1,
                letterSpacing: '-0.025em',
              }}>
                PhishShield
              </div>
              <div style={{
                fontSize: 10,
                color: 'var(--text-muted)',
                letterSpacing: '0.05em',
                textTransform: 'uppercase',
                fontWeight: 600,
                lineHeight: 1,
                marginTop: 2,
              }}>
                URL Threat Intelligence
              </div>
            </div>
          </a>

          {/* Desktop Tab Navigation */}
          <nav className="hide-mobile" style={{ display: 'flex', gap: 4 }}>
            <button
              className={`nav-tab-link${activeTab === 'dashboard' ? ' active' : ''}`}
              onClick={() => navigateTo('dashboard')}
            >
              Diagnostic Scanner
            </button>
            <button
              className={`nav-tab-link${activeTab === 'analytics' ? ' active' : ''}`}
              onClick={() => navigateTo('analytics')}
            >
              Research and Benchmarks
            </button>
            <button
              className={`nav-tab-link${activeTab === 'pricing' ? ' active' : ''}`}
              onClick={() => navigateTo('pricing')}
            >
              Deployment and Pricing
            </button>
            <button
              className={`nav-tab-link${activeTab === 'domain' ? ' active' : ''}`}
              onClick={() => navigateTo('domain')}
            >
              Custom Domain
            </button>
            <button
              className={`nav-tab-link${activeTab === 'extension' ? ' active' : ''}`}
              onClick={() => navigateTo('extension')}
            >
              Browser Extension
            </button>
            <button
              className={`nav-tab-link${activeTab === 'privacy' ? ' active' : ''}`}
              onClick={() => navigateTo('privacy')}
            >
              Privacy Policy
            </button>
            <button
              className={`nav-tab-link${activeTab === 'terms' ? ' active' : ''}`}
              onClick={() => navigateTo('terms')}
            >
              Terms
            </button>
          </nav>

          {/* Controls: Theme Switcher & Operational Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>

            {/* Theme Toggle Button (Light Mode / Dark Mode) */}
            <button
              type="button"
              onClick={toggleTheme}
              className="btn btn-secondary"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 7,
                padding: '6px 12px',
                fontSize: 11.5,
                fontFamily: 'var(--font-mono)',
                border: '1px solid var(--border-strong)',
                borderRadius: 'var(--radius-sm)',
                letterSpacing: '0.04em',
                background: 'var(--bg-surface)',
                color: 'var(--text-ink)',
                cursor: 'pointer',
              }}
              title={`Toggle ${theme === 'light' ? 'Dark' : 'Light'} Mode [T]`}
              aria-label={`Toggle ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
            >
              {theme === 'light' ? (
                <>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                  </svg>
                  <span>DARK</span>
                </>
              ) : (
                <>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="5" />
                    <line x1="12" y1="1" x2="12" y2="3" />
                    <line x1="12" y1="21" x2="12" y2="23" />
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                    <line x1="1" y1="12" x2="3" y2="12" />
                    <line x1="21" y1="12" x2="23" y2="12" />
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
                  </svg>
                  <span>LIGHT</span>
                </>
              )}
            </button>

            {/* Operational Status Dot */}
            <div className="hide-mobile" style={{
              display: 'flex',
              alignItems: 'center',
              gap: 7,
              fontSize: 12,
              color: 'var(--text-muted)',
              padding: '5px 11px',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-subtle)',
            }}>
              <span className="heartbeat-dot" />
              <span>Online</span>
            </div>

            {/* Mobile Navigation Trigger */}
            <button
              className="hamburger-btn show-mobile"
              onClick={() => setMobileMenuOpen(prev => !prev)}
              aria-label="Toggle navigation drawer"
            >
              <span />
              <span />
              <span />
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="mobile-nav-panel">
            <button
              className={`nav-tab-link${activeTab === 'dashboard' ? ' active' : ''}`}
              onClick={() => navigateTo('dashboard')}
            >
              Diagnostic Scanner
            </button>
            <button
              className={`nav-tab-link${activeTab === 'analytics' ? ' active' : ''}`}
              onClick={() => navigateTo('analytics')}
            >
              Research and Benchmarks
            </button>
            <button
              className={`nav-tab-link${activeTab === 'pricing' ? ' active' : ''}`}
              onClick={() => navigateTo('pricing')}
            >
              Deployment and Pricing
            </button>
            <button
              className={`nav-tab-link${activeTab === 'domain' ? ' active' : ''}`}
              onClick={() => navigateTo('domain')}
            >
              Custom Domain
            </button>
            <button
              className={`nav-tab-link${activeTab === 'extension' ? ' active' : ''}`}
              onClick={() => navigateTo('extension')}
            >
              Browser Extension
            </button>
            <button
              className={`nav-tab-link${activeTab === 'privacy' ? ' active' : ''}`}
              onClick={() => navigateTo('privacy')}
            >
              Privacy Policy
            </button>
            <button
              className={`nav-tab-link${activeTab === 'terms' ? ' active' : ''}`}
              onClick={() => navigateTo('terms')}
            >
              Terms
            </button>
            <div style={{ padding: '8px 12px', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Color Mode:</span>
              <button
                type="button"
                onClick={toggleTheme}
                className="btn btn-secondary"
                style={{ fontSize: 11, padding: '4px 10px' }}
              >
                Switch to {theme === 'light' ? 'Dark' : 'Light'}
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Workspace with Animated Tab Transition */}
      <main style={{
        flex: 1,
        maxWidth: 1240,
        width: '100%',
        margin: '0 auto',
        padding: '36px 24px',
      }}>
        <div key={activeTab} className="tab-pane-transition">
          {renderActiveView()}
        </div>
      </main>

      {/* Production-Grade Developer Footer */}
      <footer style={{
        background: 'var(--bg-surface)',
        borderTop: '1px solid var(--border-subtle)',
        padding: '48px 24px 28px 24px',
        marginTop: 'auto',
      }}>
        <div style={{
          maxWidth: 1240,
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 36,
        }}>
          {/* Top Section: Brand Statement + 3 Organized Category Columns */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'minmax(240px, 1.4fr) repeat(3, minmax(140px, 1fr))',
            gap: 36,
          }} className="footer-grid">

            {/* Column 1: Identity & Technical Scope */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{
                  width: 28,
                  height: 28,
                  border: '1.5px solid var(--accent)',
                  borderRadius: 'var(--radius-xs)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: 'var(--accent-subtle)',
                }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <span style={{ fontSize: 16, fontWeight: 800, color: 'var(--text-ink)', letterSpacing: '-0.02em' }}>
                  PhishShield
                </span>
              </div>
              <p style={{ fontSize: 13, color: 'var(--text-muted)', lineHeight: 1.6, maxWidth: 320 }}>
                Open-source URL threat intelligence runtime combining 41 lexical heuristics and headless DOM inspection with Tree SHAP explainability.
              </p>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 11.5, fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                <span className="heartbeat-dot" style={{ width: 6, height: 6 }} />
                <span>Runtime: 127.0.0.1:8000</span>
              </div>
            </div>

            {/* Column 2: Diagnostic & Research */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-ink)', marginBottom: 4 }}>
                Diagnostic Engine
              </div>
              <a href="#scanner" onClick={(e) => { e.preventDefault(); navigateTo('dashboard'); }} className="footer-link">
                Heuristic Scanner
              </a>
              <a href="#analytics" onClick={(e) => { e.preventDefault(); navigateTo('analytics'); }} className="footer-link">
                Benchmark Metrics
              </a>
              <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="footer-link">
                OpenAPI Explorer
              </a>
              <a href="http://localhost:8000/health" target="_blank" rel="noreferrer" className="footer-link">
                Health Check API
              </a>
            </div>

            {/* Column 3: Infrastructure & Deployment */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-ink)', marginBottom: 4 }}>
                Infrastructure
              </div>
              <a href="#pricing" onClick={(e) => { e.preventDefault(); navigateTo('pricing'); }} className="footer-link">
                Deployment Plans
              </a>
              <a href="#domain" onClick={(e) => { e.preventDefault(); navigateTo('domain'); }} className="footer-link">
                Custom Domain Setup
              </a>
              <a href="#extension" onClick={(e) => { e.preventDefault(); navigateTo('extension'); }} className="footer-link">
                Browser Extension (MV3)
              </a>
              <button
                type="button"
                onClick={() => setShowShortcuts(true)}
                className="footer-link"
                style={{ background: 'none', border: 'none', padding: 0, textAlign: 'left', cursor: 'pointer', font: 'inherit' }}
              >
                Keyboard Shortcuts [?]
              </button>
              <button
                type="button"
                onClick={() => setShowSplash(true)}
                className="footer-link"
                style={{ background: 'none', border: 'none', padding: 0, textAlign: 'left', cursor: 'pointer', font: 'inherit' }}
              >
                Replay 3D Splash
              </button>
            </div>

            {/* Column 4: Governance & Legal */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-ink)', marginBottom: 4 }}>
                Legal & Security
              </div>
              <a href="#privacy" onClick={(e) => { e.preventDefault(); navigateTo('privacy'); }} className="footer-link">
                Privacy Policy (No Cookies)
              </a>
              <a href="#terms" onClick={(e) => { e.preventDefault(); navigateTo('terms'); }} className="footer-link">
                Terms and Conditions
              </a>
              <a href="mailto:sanhithreddy5131@gmail.com" className="footer-link">
                sanhithreddy5131@gmail.com
              </a>
              <a href="tel:9381681832" className="footer-link">
                +91 9381681832
              </a>
            </div>

          </div>

          {/* Bottom Bar: Academic Attribution & License */}
          <div style={{
            borderTop: '1px solid var(--border-subtle)',
            paddingTop: 18,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 16,
            fontSize: 12,
            color: 'var(--text-muted)',
          }}>
            <div>
              Classifiers evaluated across 235,795 URLs from the PhiUSIIL dataset. MIT Academic License.
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
              <span>Build 2.4.1</span>
              <span>&copy; {new Date().getFullYear()} PhishShield Platform</span>
            </div>
          </div>
        </div>
      </footer>

    </div>
  );
}

export default App;
