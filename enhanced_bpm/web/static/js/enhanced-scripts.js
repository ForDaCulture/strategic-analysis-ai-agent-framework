/**
 * BPM Principles Explorer - Enhanced Scripts
 * This file contains all the JavaScript functionality for the enhanced UI
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Scroll to Top Button
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                scrollTopBtn.style.display = 'flex';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });

        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        // Check for saved theme preference or prefer-color-scheme
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.documentElement.setAttribute('data-theme', 'dark');
            darkModeToggle.checked = true;
        }
        
        darkModeToggle.addEventListener('change', function() {
            if (this.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Search Functionality
    const searchForm = document.getElementById('searchForm');
    const searchResults = document.getElementById('searchResults');
    const resultsContent = document.getElementById('resultsContent');
    const searchStats = document.getElementById('searchStats');
    const clearSearch = document.getElementById('clearSearch');
    const bpmContent = document.getElementById('bpmContent');

    if (searchForm && searchResults && resultsContent && bpmContent) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const searchTerm = document.getElementById('searchTerm').value.trim();
            const queryType = document.getElementById('queryType').value;
            
            if (searchTerm.length < 2) {
                showNotification('Please enter at least 2 characters to search', 'warning');
                return;
            }
            
            // Show loading state
            resultsContent.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"></div><p class="mt-3">Searching...</p></div>';
            searchResults.style.display = 'block';
            bpmContent.style.display = 'none';
            
            // Simulate search delay (replace with actual AJAX call)
            setTimeout(function() {
                // Make AJAX request to search endpoint
                fetch(`/search?term=${encodeURIComponent(searchTerm)}&type=${queryType}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.results.length > 0) {
                            displaySearchResults(data.results, searchTerm);
                            searchStats.textContent = `Found ${data.results.length} results for "${searchTerm}"`;
                        } else {
                            resultsContent.innerHTML = `<div class="text-center py-5">
                                <i class="bi bi-search" style="font-size: 3rem; color: var(--gray-400);"></i>
                                <h4 class="mt-3">No results found</h4>
                                <p class="text-muted">Try different keywords or browse the categories below</p>
                                <div class="mt-4">
                                    <a href="#core_principles" class="btn btn-outline-primary m-1">Core Principles</a>
                                    <a href="#methodologies" class="btn btn-outline-primary m-1">Methodologies</a>
                                    <a href="#frameworks" class="btn btn-outline-primary m-1">Frameworks</a>
                                    <a href="#maturity_models" class="btn btn-outline-primary m-1">Maturity Models</a>
                                </div>
                            </div>`;
                            searchStats.textContent = `No results found for "${searchTerm}"`;
                        }
                    })
                    .catch(error => {
                        console.error('Search error:', error);
                        resultsContent.innerHTML = '<div class="alert alert-danger">An error occurred while searching. Please try again.</div>';
                    });
            }, 500);
        });
        
        if (clearSearch) {
            clearSearch.addEventListener('click', function() {
                document.getElementById('searchTerm').value = '';
                searchResults.style.display = 'none';
                bpmContent.style.display = 'block';
            });
        }
    }

    // File Upload Functionality
    const fileInput = document.getElementById('file');
    const uploadArea = document.getElementById('uploadArea');
    const fileName = document.getElementById('fileName');

    if (fileInput && uploadArea) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });

        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', function() {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileName(fileInput.files[0].name);
            }
        });

        fileInput.addEventListener('change', function() {
            if (fileInput.files.length) {
                updateFileName(fileInput.files[0].name);
            }
        });

        function updateFileName(name) {
            fileName.textContent = name;
            uploadArea.querySelector('.upload-icon').classList.remove('bi-cloud-arrow-up');
            uploadArea.querySelector('.upload-icon').classList.add('bi-file-earmark-check');
            uploadArea.querySelector('.upload-text').textContent = 'File selected';
        }
    }

    // Batch File Upload Functionality
    const filesInput = document.getElementById('files');
    const batchUploadArea = document.getElementById('batchUploadArea');
    const fileList = document.getElementById('fileList');

    if (filesInput && batchUploadArea && fileList) {
        batchUploadArea.addEventListener('click', function() {
            filesInput.click();
        });

        batchUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            batchUploadArea.classList.add('dragover');
        });

        batchUploadArea.addEventListener('dragleave', function() {
            batchUploadArea.classList.remove('dragover');
        });

        batchUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            batchUploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                filesInput.files = e.dataTransfer.files;
                updateFileList();
            }
        });

        filesInput.addEventListener('change', function() {
            updateFileList();
        });

        function updateFileList() {
            fileList.innerHTML = '';
            
            if (filesInput.files.length) {
                batchUploadArea.querySelector('.upload-text').textContent = `${filesInput.files.length} files selected`;
                
                for (let i = 0; i < filesInput.files.length; i++) {
                    const file = filesInput.files[i];
                    const fileItem = document.createElement('div');
                    fileItem.className = 'card mb-2';
                    fileItem.innerHTML = `
                        <div class="card-body py-2 px-3">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <i class="bi bi-file-earmark me-2"></i>
                                    <span>${file.name}</span>
                                </div>
                                <span class="badge bg-secondary">${formatFileSize(file.size)}</span>
                            </div>
                        </div>
                    `;
                    fileList.appendChild(fileItem);
                }
            } else {
                batchUploadArea.querySelector('.upload-text').textContent = 'Drag & drop multiple files here or click to browse';
            }
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }
    }

    // Export Button Functionality
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            const filename = this.getAttribute('data-file');
            if (!filename) return;
            
            // Show loading notification
            showNotification('Preparing export...', 'info');
            
            // Simulate export delay (replace with actual AJAX call)
            setTimeout(function() {
                // Make AJAX request to export endpoint
                fetch(`/export?filename=${encodeURIComponent(filename)}`)
                    .then(response => response.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        showNotification('Export completed successfully!', 'success');
                    })
                    .catch(error => {
                        console.error('Export error:', error);
                        showNotification('An error occurred during export. Please try again.', 'danger');
                    });
            }, 1000);
        });
    }

    // Print Button Functionality
    const printBtn = document.getElementById('printBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }

    // Notification System
    function showNotification(message, type = 'info') {
        const notificationContainer = document.getElementById('notificationContainer');
        
        if (!notificationContainer) {
            // Create notification container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'notificationContainer';
            container.className = 'position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1050';
            document.body.appendChild(container);
        }
        
        const notification = document.createElement('div');
        notification.className = `toast align-items-center text-white bg-${type} border-0`;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'assertive');
        notification.setAttribute('aria-atomic', 'true');
        
        notification.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        document.getElementById('notificationContainer').appendChild(notification);
        
        const toast = new bootstrap.Toast(notification, {
            autohide: true,
            delay: 5000
        });
        
        toast.show();
        
        // Remove notification from DOM after it's hidden
        notification.addEventListener('hidden.bs.toast', function() {
            notification.remove();
        });
    }

    // Display Search Results
    function displaySearchResults(results, searchTerm) {
        resultsContent.innerHTML = '';
        
        // Group results by category
        const groupedResults = {};
        
        results.forEach(result => {
            if (!groupedResults[result.category]) {
                groupedResults[result.category] = [];
            }
            groupedResults[result.category].push(result);
        });
        
        // Create results HTML
        for (const category in groupedResults) {
            const categoryResults = groupedResults[category];
            
            const categorySection = document.createElement('div');
            categorySection.className = 'mb-4';
            
            categorySection.innerHTML = `
                <h4 class="mb-3">${formatCategoryName(category)} (${categoryResults.length})</h4>
                <div class="row" id="${category}_results"></div>
            `;
            
            resultsContent.appendChild(categorySection);
            
            const resultsContainer = document.getElementById(`${category}_results`);
            
            categoryResults.forEach(result => {
                const resultCard = document.createElement('div');
                resultCard.className = 'col-md-6 mb-3';
                
                // Highlight search term in content
                const highlightedContent = highlightSearchTerm(result.content, searchTerm);
                
                resultCard.innerHTML = `
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="mb-0">${result.title}</h5>
                            <span class="badge bg-primary">${formatCategoryName(result.subcategory)}</span>
                        </div>
                        <div class="card-body">
                            <p>${highlightedContent}</p>
                            <a href="#${result.id}" class="btn btn-sm btn-primary" id="view_${result.id}">View Details</a>
                        </div>
                    </div>
                `;
                
                resultsContainer.appendChild(resultCard);
                
                // Add click event to view button
                document.getElementById(`view_${result.id}`).addEventListener('click', function() {
                    searchResults.style.display = 'none';
                    bpmContent.style.display = 'block';
                    
                    // Scroll to the result item
                    const targetElement = document.getElementById(result.id);
                    if (targetElement) {
                        setTimeout(() => {
                            window.scrollTo({
                                top: targetElement.offsetTop - 70,
                                behavior: 'smooth'
                            });
                            
                            // Highlight the target element
                            targetElement.classList.add('highlight-result');
                            setTimeout(() => {
                                targetElement.classList.remove('highlight-result');
                            }, 3000);
                        }, 100);
                    }
                });
            });
        }
    }

    // Format category name (convert snake_case to Title Case)
    function formatCategoryName(category) {
        return category
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    // Highlight search term in content
    function highlightSearchTerm(content, searchTerm) {
        if (!searchTerm) return content;
        
        const regex = new RegExp(`(${escapeRegExp(searchTerm)})`, 'gi');
        return content.replace(regex, '<mark>$1</mark>');
    }

    // Escape special characters in search term for regex
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // Initialize any charts if they exist
    initializeCharts();
});

// Initialize Charts
function initializeCharts() {
    // This function will be called to initialize any charts on the page
    // The actual chart initialization is in the specific page scripts
    // This is just a placeholder for any common chart functionality
}

// Mobile Navigation Adjustments
window.addEventListener('resize', function() {
    adjustMobileNavigation();
});

function adjustMobileNavigation() {
    const windowWidth = window.innerWidth;
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (windowWidth < 992 && navbarCollapse) {
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    document.querySelector('.navbar-toggler').click();
                }
            });
        });
    }
}

// Call once on load
adjustMobileNavigation();