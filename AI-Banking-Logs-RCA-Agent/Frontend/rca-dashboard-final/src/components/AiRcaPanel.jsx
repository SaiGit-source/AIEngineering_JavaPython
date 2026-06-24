import { useEffect, useState } from "react";
import { analyzeRca } from "../api";
import Card from "./Card";

export default function AiRcaPanel({ selectedTrace }) {
  const traceQuestion = selectedTrace?.traceId
    ? `Why did ${selectedTrace.traceId} fail?`
    : "Why are payments failing?";

  const [question, setQuestion] = useState(traceQuestion);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setQuestion(traceQuestion);
  }, [traceQuestion]);

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const result = await analyzeRca(question);
      setAnalysis(result);
    } catch (err) {
      setError(err.message || "Failed to generate RCA");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title="AI RCA assistant" subtitle="Spring Boot → Pinecone RAG → ChatClient">
      <div className="ai-panel">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          rows={4}
          placeholder="Ask: Why did TRACE-10045 fail?"
        />

        <div className="button-row">
          <button onClick={handleAnalyze} disabled={loading || !question.trim()}>
            {loading ? "Analyzing..." : "Generate RCA"}
          </button>
        </div>

        {error && <div className="error-box">{error}</div>}

        {analysis && (
          <div className="rca-result">
            <div className="result-grid">
              <div>
                <label>Root cause</label>
                <p>{analysis.rootCause || analysis.answer || "Not available"}</p>
              </div>
              <div>
                <label>Impacted service</label>
                <p>{analysis.impactedService || "Unknown"}</p>
              </div>
              <div>
                <label>Symptom</label>
                <p>{analysis.symptom || "Not available"}</p>
              </div>
            </div>

            <div className="list-section">
              <label>Evidence used by AI</label>
              <ul>
                {(analysis.evidence || []).map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="list-section">
              <label>Suggested fix</label>
              <ul>
                {(analysis.suggestedFix || []).map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <details>
              <summary>Retrieved Pinecone evidence</summary>
              <pre>{JSON.stringify(analysis.retrievedEvidence || [], null, 2)}</pre>
            </details>
          </div>
        )}
      </div>
    </Card>
  );
}
