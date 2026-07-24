let businesses = [];
let map;
let markerLayer;

async function initializeMap() {
  if (!window.L) {
    document.getElementById('map').innerHTML = '<div class="empty">Map library unavailable. The table still works.</div>';
    return;
  }
  let tileUrl = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  try {
    const configResponse = await fetch('/api/runtime-config');
    if (configResponse.ok) {
      const config = await configResponse.json();
      if (config.tile_url) tileUrl = config.tile_url;
    }
  } catch (_) {
    // Keep the documented OpenStreetMap default when runtime configuration is unavailable.
  }
  map = L.map('map').setView([52.3676, 4.9041], 11);
  L.tileLayer(tileUrl, {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  markerLayer = L.layerGroup().addTo(map);
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#039;', '"': '&quot;'
  })[character]);
}

function safeUrl(value) {
  if (!value) return '';
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch (_) {
    return '';
  }
}

function setLoading(active, label = 'Ready') {
  const button = document.querySelector('#searchForm button[type="submit"]');
  button.disabled = active;
  button.textContent = active ? 'Searching…' : 'Run search';
  document.getElementById('statusBadge').textContent = label;
}

function setMessage(text, error = false) {
  const element = document.getElementById('message');
  element.textContent = text;
  element.classList.toggle('error', error);
}

function updateMetrics() {
  const total = businesses.length;
  const percent = count => total ? `${Math.round((count / total) * 100)}%` : '0%';
  document.getElementById('metricRecords').textContent = total;
  document.getElementById('metricPhone').textContent = percent(businesses.filter(item => item.phone).length);
  document.getElementById('metricWebsite').textContent = percent(businesses.filter(item => item.website).length);
  const average = total ? Math.round(businesses.reduce((sum, item) => sum + item.quality_score, 0) / total) : 0;
  document.getElementById('metricQuality').textContent = average;
}

function renderTable() {
  const body = document.getElementById('resultsBody');
  if (!businesses.length) {
    body.innerHTML = '<tr><td colspan="7" class="empty">No records found.</td></tr>';
    return;
  }
  body.innerHTML = businesses.map(item => {
    const website = safeUrl(item.website);
    const sourceUrl = safeUrl(item.source_url);
    const contact = [
      item.phone ? `<div>${escapeHtml(item.phone)}</div>` : '',
      item.email ? `<div><a href="mailto:${escapeHtml(item.email)}">${escapeHtml(item.email)}</a></div>` : '',
      website ? `<div><a href="${escapeHtml(website)}" target="_blank" rel="noreferrer">Website</a></div>` : ''
    ].join('');
    const rating = item.rating == null ? '—' : `${escapeHtml(item.rating)} <span class="subtle">(${escapeHtml(item.review_count ?? 0)})</span>`;
    const source = sourceUrl
      ? `<a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noreferrer">${escapeHtml(item.source)}</a>`
      : escapeHtml(item.source);
    return `<tr>
      <td><div class="business-name">${escapeHtml(item.name)}</div><div class="subtle">${escapeHtml(item.city)}</div></td>
      <td>${escapeHtml(item.category || '—')}</td>
      <td>${escapeHtml(item.address || '—')}</td>
      <td>${contact || '—'}</td>
      <td>${rating}</td>
      <td><span class="quality">${escapeHtml(item.quality_score)}</span></td>
      <td>${source}</td>
    </tr>`;
  }).join('');
}

function renderMap() {
  if (!map || !markerLayer) return;
  markerLayer.clearLayers();
  const points = [];
  businesses.forEach(item => {
    if (typeof item.latitude !== 'number' || typeof item.longitude !== 'number') return;
    const marker = L.marker([item.latitude, item.longitude]);
    marker.bindPopup(`<strong>${escapeHtml(item.name)}</strong><br>${escapeHtml(item.category)}<br>${escapeHtml(item.address)}`);
    marker.addTo(markerLayer);
    points.push([item.latitude, item.longitude]);
  });
  if (points.length === 1) map.setView(points[0], 14);
  if (points.length > 1) map.fitBounds(points, { padding: [28, 28] });
}

function refreshView() {
  updateMetrics();
  renderTable();
  renderMap();
  const enabled = businesses.length > 0;
  document.getElementById('downloadCsv').disabled = !enabled;
  document.getElementById('downloadJson').disabled = !enabled;
}

async function readError(response) {
  try {
    const data = await response.json();
    return data.detail || JSON.stringify(data);
  } catch (_) {
    return `${response.status} ${response.statusText}`;
  }
}

document.getElementById('searchForm').addEventListener('submit', async event => {
  event.preventDefault();
  setLoading(true, 'Working');
  setMessage('Contacting the selected provider…');
  const payload = {
    provider: document.getElementById('provider').value,
    query: document.getElementById('query').value,
    city: document.getElementById('city').value,
    radius_m: Number(document.getElementById('radius').value),
    limit: Number(document.getElementById('limit').value),
    language: 'en',
    deduplicate: document.getElementById('deduplicate').checked
  };
  try {
    const response = await fetch('/api/search', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(await readError(response));
    const data = await response.json();
    businesses = data.businesses;
    refreshView();
    const warning = data.meta.warnings.length ? ` ${data.meta.warnings.join(' ')}` : '';
    const cache = data.meta.cache_hit
      ? ` Served from ${data.meta.cache_stale ? 'stale ' : ''}cache (${data.meta.cache_age_seconds ?? 0}s old).`
      : '';
    setMessage(`Returned ${data.meta.returned} records; removed ${data.meta.duplicates_removed} duplicate(s).${cache}${warning}`);
    setLoading(false, 'Complete');
  } catch (error) {
    businesses = [];
    refreshView();
    setMessage(error.message, true);
    setLoading(false, 'Error');
  }
});

document.getElementById('downloadCsv').addEventListener('click', async () => {
  const response = await fetch('/api/export/csv', {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({businesses})
  });
  if (!response.ok) return setMessage(await readError(response), true);
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url; link.download = 'geobusiness-results.csv'; link.click();
  URL.revokeObjectURL(url);
});

document.getElementById('downloadJson').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(businesses, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url; link.download = 'geobusiness-results.json'; link.click();
  URL.revokeObjectURL(url);
});

document.getElementById('analyzeButton').addEventListener('click', async () => {
  if (!businesses.length) return setMessage('Search for businesses before running analysis.', true);
  const output = document.getElementById('analysisOutput');
  output.textContent = 'Analyzing…';
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        businesses,
        instruction: document.getElementById('analysisInstruction').value
      })
    });
    if (!response.ok) throw new Error(await readError(response));
    const data = await response.json();
    output.textContent = `${data.text}\n\nProvider: ${data.provider} · Model: ${data.model}`;
  } catch (error) {
    output.textContent = error.message;
  }
});

initializeMap();
document.getElementById('searchForm').requestSubmit();
