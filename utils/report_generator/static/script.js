function toggleAccordion(header) {
    var content = header.nextElementSibling;
    if (content.style.display === 'block') {
        content.style.display = 'none';
    } else {
        content.style.display = 'block';
    }
}

// Toggle Expand/Collapse All
let allExpanded = false;
document.getElementById('toggleAllBtn').onclick = function() {
    allExpanded = !allExpanded;
    document.querySelectorAll('.accordion-content').forEach(function(content) {
        content.style.display = allExpanded ? 'block' : 'none';
    });
    this.textContent = allExpanded ? 'Collapse All' : 'Expand All';
};


// Clipboard copy for json-view
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.copy-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const pre = btn.parentElement.querySelector('.json-view');
            if (pre) {
                const text = pre.textContent;
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(function() {
                        btn.textContent = '✅';
                        setTimeout(() => btn.textContent = '📋', 1200);
                    });
                } else {
                    // fallback for older browsers
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    btn.textContent = '✅';
                    setTimeout(() => btn.textContent = '📋', 1200);
                }
            }
        });
    });
});

// Filter/Search
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');

searchInput.addEventListener('input', filterAccordion);
statusFilter.addEventListener('change', filterAccordion);

function filterAccordion() {
    const keyword = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    document.querySelectorAll('.accordion-item').forEach(item => {
        const scenario = item.querySelector('.accordion-header span').textContent.toLowerCase();
        const itemStatus = item.getAttribute('data-status');
        let show = true;
        if (keyword && !scenario.includes(keyword)) show = false;
        if (status && itemStatus !== status) show = false;
        item.style.display = show ? '' : 'none';
    });
}
