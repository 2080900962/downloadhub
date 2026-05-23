async function testAndDownload(url, mirrors) {
    const mirrorDiv = document.getElementById('mirrorResults');
    mirrorDiv.innerHTML = '<div class="spinner"></div><p>正在测速...</p>';

    const alternatives = [url, ...mirrors];

    const res = await fetch('/api/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    });

    const data = await res.json();

    mirrorDiv.innerHTML = data.results.map(r => `
        <div class="platform-item">
            <div>
                <div class="platform-name">${r.source}</div>
                <div style="font-size:0.9rem;color:#666">${r.speed} · ${r.size}</div>
            </div>
            <button class="download-btn" onclick="window.open('${r.url}')" ${!r.available ? 'disabled' : ''}>
                ${r.available ? '下载' : '不可用'}
            </button>
        </div>
    `).join('');
}
