document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle search form submission
    const searchForm = document.getElementById('searchForm');
    const searchResults = document.getElementById('searchResults');
    const resultsContent = document.getElementById('resultsContent');
    const bpmContent = document.getElementById('bpmContent');
    const clearSearchBtn = document.getElementById('clearSearch');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(searchForm);
            
            // Don't search if search term is empty
            if (!formData.get('search_term').trim()) {
                return;
            }
            
            fetch('/query', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Show search results and hide main content
                searchResults.style.display = 'block';
                bpmContent.style.display = 'none';
                
                // Clear previous results
                resultsContent.innerHTML = '';
                
                // Check if we have results
                if (Object.keys(data).length === 0) {
                    resultsContent.innerHTML = '<div class="alert alert-info">No results found.</div>';
                    return;
                }
                
                // Process and display results
                for (const section in data) {
                    const sectionTitle = formatSectionTitle(section);
                    const sectionDiv = document.createElement('div');
                    sectionDiv.className = 'mb-4';
                    sectionDiv.innerHTML = `<h3>${sectionTitle}</h3>`;
                    
                    // Create appropriate display for each section
                    if (Array.isArray(data[section])) {
                        const itemsDiv = document.createElement('div');
                        itemsDiv.className = 'row';
                        
                        data[section].forEach(item => {
                            const itemDiv = createResultCard(item, section);
                            itemsDiv.appendChild(itemDiv);
                        });
                        
                        sectionDiv.appendChild(itemsDiv);
                    }
                    
                    resultsContent.appendChild(sectionDiv);
                }
                
                // Highlight search terms
                highlightSearchTerms(formData.get('search_term').trim());
            })
            .catch(error => {
                console.error('Error:', error);
                resultsContent.innerHTML = '<div class="alert alert-danger">An error occurred while searching.</div>';
            });
        });
    }
    
    // Clear search results
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function() {
            searchResults.style.display = 'none';
            bpmContent.style.display = 'block';
            resultsContent.innerHTML = '';
            searchForm.reset();
        });
    }
    
    // Format section title from snake_case to Title Case
    function formatSectionTitle(section) {
        return section
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    
    // Create a card for a search result item
    function createResultCard(item, section) {
        const colDiv = document.createElement('div');
        colDiv.className = 'col-md-6 mb-4';
        
        let cardContent = '';
        let cardHeaderClass = '';
        
        // Set card header color based on section
        switch(section) {
            case 'core_principles':
                cardHeaderClass = 'bg-primary text-white';
                break;
            case 'methodologies':
                cardHeaderClass = 'bg-success text-white';
                break;
            case 'frameworks':
                cardHeaderClass = 'bg-info text-white';
                break;
            case 'maturity_models':
                cardHeaderClass = 'bg-warning text-dark';
                break;
            case 'performance_metrics':
                cardHeaderClass = 'bg-secondary text-white';
                break;
            case 'implementation_best_practices':
                cardHeaderClass = 'bg-dark text-white';
                break;
            case 'common_challenges':
                cardHeaderClass = 'bg-danger text-white';
                break;
            case 'technology_enablers':
                cardHeaderClass = 'bg-primary text-white';
                break;
            default:
                cardHeaderClass = 'bg-light';
        }
        
        // Create card header based on item type
        let cardHeader = '';
        if (item.name) {
            cardHeader = item.name;
        } else if (item.challenge) {
            cardHeader = item.challenge;
        } else if (item.phase) {
            cardHeader = item.phase;
        } else if (item.category) {
            cardHeader = item.category;
        }
        
        // Create card body based on item type
        let cardBody = '';
        
        // Add description if available
        if (item.description) {
            cardBody += `<p>${item.description}</p>`;
        }
        
        // Add lists based on item properties
        const listProperties = [
            { key: 'benefits', title: 'Benefits' },
            { key: 'implementation_strategies', title: 'Implementation Strategies' },
            { key: 'key_concepts', title: 'Key Concepts' },
            { key: 'tools', title: 'Tools' },
            { key: 'steps', title: 'Steps' },
            { key: 'components', title: 'Components' },
            { key: 'capabilities', title: 'Capabilities' },
            { key: 'examples', title: 'Examples' },
            { key: 'mitigation_strategies', title: 'Mitigation Strategies' },
            { key: 'improvement_strategies', title: 'Improvement Strategies' },
            { key: 'practices', title: 'Practices' }
        ];
        
        listProperties.forEach(prop => {
            if (item[prop.key] && Array.isArray(item[prop.key]) && item[prop.key].length > 0) {
                cardBody += `<h5>${prop.title}:</h5><ul>`;
                item[prop.key].forEach(listItem => {
                    cardBody += `<li>${listItem}</li>`;
                });
                cardBody += `</ul>`;
            }
        });
        
        // Add calculation if available
        if (item.calculation) {
            cardBody += `<h5>Calculation:</h5><p><code>${item.calculation}</code></p>`;
        }
        
        // Add BPM application if available
        if (item.bpm_application) {
            cardBody += `<h5>BPM Application:</h5><p>${item.bpm_application}</p>`;
        }
        
        // Create the complete card
        colDiv.innerHTML = `
            <div class="card h-100">
                <div class="card-header ${cardHeaderClass}">
                    ${cardHeader}
                </div>
                <div class="card-body">
                    ${cardBody}
                </div>
            </div>
        `;
        
        return colDiv;
    }
    
    // Highlight search terms in the results
    function highlightSearchTerms(searchTerm) {
        if (!searchTerm) return;
        
        const searchTerms = searchTerm.toLowerCase().split(' ').filter(term => term.length > 2);
        if (searchTerms.length === 0) return;
        
        const resultsContainer = document.getElementById('resultsContent');
        const textNodes = getTextNodes(resultsContainer);
        
        textNodes.forEach(node => {
            const text = node.nodeValue;
            let highlightedText = text;
            let replaced = false;
            
            searchTerms.forEach(term => {
                const regex = new RegExp(`(${escapeRegExp(term)})`, 'gi');
                if (regex.test(highlightedText)) {
                    highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>');
                    replaced = true;
                }
            });
            
            if (replaced) {
                const span = document.createElement('span');
                span.innerHTML = highlightedText;
                node.parentNode.replaceChild(span, node);
            }
        });
    }
    
    // Get all text nodes in an element
    function getTextNodes(node) {
        const textNodes = [];
        
        function getNodes(node) {
            if (node.nodeType === 3) {
                textNodes.push(node);
            } else {
                const children = node.childNodes;
                for (let i = 0; i < children.length; i++) {
                    getNodes(children[i]);
                }
            }
        }
        
        getNodes(node);
        return textNodes;
    }
    
    // Escape special characters for regex
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
});