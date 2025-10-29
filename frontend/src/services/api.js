export async function ragQuery(question, k = 3) {
  const resp = await fetch(`http://localhost:8000/api/rag/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, k })
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.detail || `RAG query failed with ${resp.status}`);
  }
  return resp.json();
}
