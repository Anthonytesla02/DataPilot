// Global application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize DataTables if present
    if (typeof jQuery !== 'undefined' && jQuery.fn.DataTable) {
        $('#tablesTable').DataTable({
            pageLength: 25,
            responsive: true,
            order: [[0, 'asc']],
            language: {
                search: "Filter tables:",
                searchPlaceholder: "Type to filter..."
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
});

// Utility functions
function refreshTables() {
    // Add loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Refreshing...';
    button.disabled = true;
    
    // Reload the page after a short delay
    setTimeout(function() {
        window.location.reload();
    }, 500);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            showToast('Failed to copy to clipboard', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard!', 'success');
        } catch (err) {
            showToast('Failed to copy to clipboard', 'error');
        }
        document.body.removeChild(textArea);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toastHtml = `
        <div class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '1080';
        document.body.appendChild(toastContainer);
    }
    
    // Add toast to container
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Loading indicator utility
function showLoading(element, text = 'Loading...') {
    const originalContent = element.innerHTML;
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    element.disabled = true;
    
    return function hideLoading() {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Confirm dialog utility
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Format SQL query for display
function formatSQL(sql) {
    return sql
        .replace(/\bSELECT\b/gi, 'SELECT')
        .replace(/\bFROM\b/gi, '\nFROM')
        .replace(/\bWHERE\b/gi, '\nWHERE')
        .replace(/\bORDER BY\b/gi, '\nORDER BY')
        .replace(/\bGROUP BY\b/gi, '\nGROUP BY')
        .replace(/\bHAVING\b/gi, '\nHAVING')
        .replace(/\bLIMIT\b/gi, '\nLIMIT');
}

// Export data as file
function exportData(data, filename, type) {
    let content = '';
    let mimeType = '';
    
    switch(type) {
        case 'json':
            content = JSON.stringify(data, null, 2);
            mimeType = 'application/json';
            break;
        case 'csv':
            if (Array.isArray(data) && data.length > 0) {
                const headers = Object.keys(data[0]).join(',');
                const rows = data.map(row => 
                    Object.values(row).map(val => 
                        typeof val === 'string' && val.includes(',') ? `"${val}"` : val
                    ).join(',')
                ).join('\n');
                content = headers + '\n' + rows;
            }
            mimeType = 'text/csv';
            break;
        case 'txt':
            content = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
            mimeType = 'text/plain';
            break;
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Handle form submissions with loading states
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton && !form.hasAttribute('data-no-loading')) {
        const hideLoading = showLoading(submitButton, 'Processing...');
        
        // Re-enable button after 10 seconds as fallback
        setTimeout(hideLoading, 10000);
    }
});

// Handle AJAX errors globally
if (typeof jQuery !== 'undefined') {
    $(document).ajaxError(function(event, xhr, settings, thrownError) {
        if (xhr.status === 0) {
            showToast('Network error. Please check your connection.', 'danger');
        } else if (xhr.status >= 500) {
            showToast('Server error. Please try again later.', 'danger');
        } else if (xhr.status === 404) {
            showToast('Requested resource not found.', 'warning');
        } else {
            showToast(`Error: ${xhr.status} - ${thrownError}`, 'danger');
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+R or F5 to refresh tables (on index page)
    if ((e.ctrlKey && e.key === 'r') || e.key === 'F5') {
        if (window.location.pathname === '/') {
            e.preventDefault();
            refreshTables();
        }
    }
});

// Auto-resize textareas
document.querySelectorAll('textarea[data-auto-resize]').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});

// Table row click handlers
document.addEventListener('click', function(e) {
    if (e.target.closest('tr[data-href]')) {
        const row = e.target.closest('tr[data-href]');
        const href = row.getAttribute('data-href');
        if (href && !e.target.closest('a, button')) {
            window.location.href = href;
        }
    }
});

// Search input debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Apply debouncing to search inputs
document.querySelectorAll('input[type="search"]').forEach(input => {
    input.addEventListener('input', debounce(function() {
        // Auto-submit search forms after typing stops
        if (this.form && this.form.hasAttribute('data-auto-submit')) {
            this.form.submit();
        }
    }, 500));
});
