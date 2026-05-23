let allSoftware = [];

async function loadSoftware() {
    const res = await fetch('/api/software');
    allSoftware = await res.json();
    renderSoftware(allSoftware);
}

function renderSoftware(list) {
    const grid = document.getElementById('softwareGrid');
    grid.innerHTML = list.map(s => `
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
}

document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;
        const filtered = cat === 'all' ? allSoftware : allSoftware.filter(s => s.category === cat);
        renderSoftware(filtered);
    });
});

document.getElementById('searchInput').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = allSoftware.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.tags.some(t => t.toLowerCase().includes(q)) ||
        s.description.toLowerCase().includes(q)
    );
    renderSoftware(filtered);
});

loadSoftware();
