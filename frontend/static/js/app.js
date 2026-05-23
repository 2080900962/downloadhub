let currentMethod = 'head';

function showError(message) {
    const toast = document.getElementById('errorToast');
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function tryExample(url) {
    document.getElementById('urlInput').value = url;
    document.getElementById('emptyState').style.display = 'none';
    startSearch('head');
}

async function startSearch(method = 'head') {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) {
        showError('请输入下载链接');
        return;
    }

    currentMethod = method;
    document.getElementById('searchBtn').disabled = true;
    document.getElementById('rangeBtn').disabled = true;
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('loadingText').textContent = '正在搜索替代源...';

    setTimeout(() => {
        document.getElementById('loadingText').textContent = '正在并发测速...';
    }, 1000);

    try {
        const resp = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, method })
        });

        if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}`);
        }

        const data = await resp.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        displayResults(data);
    } catch (err) {
        showError('搜索失败：' + err.message);
        document.getElementById('emptyState').style.display = 'block';
    } finally {
        document.getElementById('searchBtn').disabled = false;
        document.getElementById('rangeBtn').disabled = false;
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResults(data) {
    const container = document.getElementById('results');

    if (!data.results || data.results.length === 0) {
        document.getElementById('emptyState').style.display = 'block';
        return;
    }

    container.innerHTML = `
        <h3>📦 ${data.filename}</h3>
        <div style="color: rgba(255,255,255,0.5); font-size: 13px; margin-bottom: 20px;">
            找到 ${data.total} 个源 · ${data.available} 个可用 · 耗时 ${data.elapsed}
        </div>
    `;

    data.results.forEach((item, idx) => {
        const isFastest = idx === 0 && item.available;
        const methodBadge = item.method ? `<span class="badge" style="background: rgba(0,212,255,0.15); color: #00d4ff; border: 1px solid rgba(0,212,255,0.3);">${item.method}</span>` : '';

        const html = `
            <div class="result-item ${isFastest ? 'fastest' : ''}">
                ${isFastest ? '<span class="fastest-badge">⚡ 推荐最快源</span>' : ''}
                <div class="url">${item.url}</div>
                <div class="meta">
                    <span class="badge ${item.available ? 'badge-success' : 'badge-error'}">
                        ${item.available ? '✓ 可用' : '✗ 不可用'}
                    </span>
                    ${methodBadge}
                    <span class="speed">响应: ${item.speed}</span>
                    <span>大小: ${item.size}</span>
                    <span>来源: ${item.source}</span>
                </div>
            </div>
        `;
        container.innerHTML += html;
    });

    container.style.display = 'block';
}

document.getElementById('urlInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startSearch('head');
});

async function loadFeaturedSoftware() {
    try {
        const res = await fetch('/api/software');
        const software = await res.json();
        const featured = software.filter(s => s.featured);

        document.getElementById('featuredSoftware').innerHTML = featured.map(s => `
            <div class="software-card" onclick="location.href='/software/${s.id}'">
                <div class="card-header">
                    <span class="logo">${s.logo}</span>
                    ${s.trending ? '<span class="trending-badge">🔥 热门</span>' : ''}
                </div>
                <h3>${s.name}</h3>
                <p class="version">v${s.version}</p>
                <p class="description">${s.description}</p>
                <div class="card-footer">
                    <div class="tags">
                        ${s.tags.slice(0, 2).map(t => `<span class="tag">${t}</span>`).join('')}
                    </div>
                    ${s.downloads ? `<span class="downloads">↓ ${s.downloads}</span>` : ''}
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error('Failed to load software:', e);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('emptyState').style.display = 'block';
    loadFeaturedSoftware();
});
