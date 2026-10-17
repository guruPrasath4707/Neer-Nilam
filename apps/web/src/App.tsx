import entityRecord from "../../../data/entities/NN-SITE-BRIHADISVARA-THANJAVUR.json";
import historicalStateRecord from "../../../data/historical-states/NN-GAP-BRIHADISVARA-001.json";
import scenePackFixture from "../../../data/scene-packs/BRH-001-GAP-FIXTURE.json";
import { gapExplanation, isGapScenePack, parseScenePack } from "./scenePack";
import "./styles.css";

interface SiteEntity {
  id: string;
  canonical_name: string;
  verification_status: string;
  rights_status: string;
}

interface HistoricalState {
  id: string;
  label: string;
  verification_status: string;
  uncertainty?: { code?: string; message?: string };
}

const entity = entityRecord as SiteEntity;
const historicalState = historicalStateRecord as HistoricalState;
const scenePack = parseScenePack(scenePackFixture as unknown);
const isGap = isGapScenePack(scenePack);

function App() {
  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="wordmark" href="#main" aria-label="Neer-Nilam home">
          <span className="wordmark-mark" aria-hidden="true">N</span>
          <span>
            <strong>NEER-NILAM</strong>
            <small>Digital heritage research</small>
          </span>
        </a>
        <div className="header-meta">
          <span className="header-dot" aria-hidden="true" />
          <span>Evidence-first prototype</span>
        </div>
      </header>

      <main id="main" className="main-content">
        <div className="breadcrumb">PILOT AREA <span aria-hidden="true">/</span> THANJAVUR <span aria-hidden="true">/</span> RECORD VIEW</div>

        <section className="intro-section" aria-labelledby="site-title">
          <p className="eyebrow">SITE RECORD · {entity.id}</p>
          <h1 id="site-title">{entity.canonical_name}</h1>
          <p className="intro-copy">
            A source-aware view of historical place, time, evidence and uncertainty.
            This first client is deliberately connected to the repository's current scene-pack fixture.
          </p>
        </section>

        <section
          className={isGap ? "state-panel state-panel-gap" : "state-panel"}
          aria-labelledby="state-title"
          role="status"
        >
          <div className="state-panel-heading">
            <span className="state-symbol" aria-hidden="true">{isGap ? "!" : "i"}</span>
            <div>
              <p className="eyebrow">CURRENT RESOLUTION</p>
              <h2 id="state-title">{isGap ? "No supported reconstruction" : "Scene-pack state available"}</h2>
            </div>
          </div>
          <p className="state-copy">{gapExplanation(scenePack)}</p>
          <div className="state-tags">
            <span className="status-pill">{scenePack.state_kind}</span>
            <span className="neutral-pill">Historical geometry not loaded</span>
          </div>
        </section>

        <div className="record-grid">
          <section className="record-panel" aria-labelledby="evidence-title">
            <div className="panel-heading">
              <span className="section-index">01</span>
              <h2 id="evidence-title">Evidence record</h2>
            </div>
            <p className="panel-copy">
              Evidence references attached to this scene pack are shown here. Empty lists are reported as gaps, not filled with guessed content.
            </p>
            {scenePack.evidence_refs && scenePack.evidence_refs.length > 0 ? (
              <ul className="reference-list">
                {scenePack.evidence_refs.map((reference) => <li key={reference}>{reference}</li>)}
              </ul>
            ) : (
              <p className="empty-state">No evidence references are linked in this fixture.</p>
            )}
            <dl className="metadata-list">
              <div>
                <dt>Entity review status</dt>
                <dd>{entity.verification_status}</dd>
              </div>
              <div>
                <dt>Entity rights status</dt>
                <dd>{entity.rights_status}</dd>
              </div>
              <div>
                <dt>Historical state</dt>
                <dd>{historicalState.label}</dd>
              </div>
            </dl>
          </section>

          <section className="record-panel" aria-labelledby="scene-title">
            <div className="panel-heading">
              <span className="section-index">02</span>
              <h2 id="scene-title">Scene-pack metadata</h2>
            </div>
            <dl className="metadata-list">
              <div>
                <dt>Scene ID</dt>
                <dd className="breakable">{scenePack.scene_id}</dd>
              </div>
              <div>
                <dt>Resolved state ID</dt>
                <dd className="breakable">{scenePack.resolved_state_id ?? "None"}</dd>
              </div>
              <div>
                <dt>Requested interval</dt>
                <dd>
                  {scenePack.requested_interval.from ?? "Not specified"}
                  {" — "}
                  {scenePack.requested_interval.to ?? "Not specified"}
                </dd>
              </div>
              <div>
                <dt>Linked assets</dt>
                <dd>{scenePack.asset_refs?.length ?? 0}</dd>
              </div>
              <div>
                <dt>Declared data gaps</dt>
                <dd>{scenePack.data_gaps.length}</dd>
              </div>
            </dl>
            <div className="note-line">
              The viewer will only receive historical geometry when a reviewed scene pack and eligible assets are available.
            </div>
          </section>
        </div>

        <section className="next-gate" aria-labelledby="next-gate-title">
          <p className="eyebrow">NEXT REVIEW GATE</p>
          <h2 id="next-gate-title">Evidence before visualization</h2>
          <p>
            Source verification, rights review, and an explicitly supported time interval must be resolved before a historical scene is presented as fact.
          </p>
        </section>
      </main>

      <footer className="site-footer">
        <span>NEER-NILAM · SOFTWARE FOUNDATION</span>
        <a href="https://github.com/guruPrasath4707/Neer-Nilam" target="_blank" rel="noreferrer">
          Repository <span aria-hidden="true">↗</span>
        </a>
      </footer>
    </div>
  );
}

export default App;
