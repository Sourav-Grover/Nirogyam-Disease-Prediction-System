document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const manualSymptomsTextarea = document.getElementById('manual-symptoms');
    
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            const tabId = this.getAttribute('data-tab');
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Symptom search functionality
    const searchInput = document.getElementById('symptom-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchValue = this.value.toLowerCase();
            
            checkboxes.forEach(checkbox => {
                const label = checkbox.nextElementSibling;
                const symptomText = label.textContent.toLowerCase();
                
                if (symptomText.includes(searchValue)) {
                    checkbox.parentNode.style.display = 'flex';
                } else {
                    checkbox.parentNode.style.display = 'none';
                }
            });
        });
    }
    
    // Tag click functionality for common symptoms
    const symptomTags = document.querySelectorAll('.tag');
    if (symptomTags.length > 0 && manualSymptomsTextarea) {
        symptomTags.forEach(tag => {
            tag.addEventListener('click', function() {
                const symptom = this.textContent;
                const currentText = manualSymptomsTextarea.value.trim();
                
                if (currentText === '') {
                    manualSymptomsTextarea.value = symptom;
                } else if (!currentText.split(',').map(s => s.trim()).includes(symptom)) {
                    manualSymptomsTextarea.value = currentText + ', ' + symptom;
                }
            });
        });
    }
    
    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const activeTab = document.querySelector('.tab-pane.active');
            
            if (activeTab.id === 'checkbox-tab') {
                const checked = document.querySelectorAll('input[type="checkbox"]:checked');
                if (checked.length === 0) {
                    alert('Please select at least one symptom');
                    return;
                }
            } else if (activeTab.id === 'manual-tab') {
                if (!manualSymptomsTextarea.value.trim()) {
                    alert('Please enter at least one symptom');
                    return;
                }
            }
            
            form.submit();
        });
    }
    
    // Select All and Clear All buttons
    const selectAllBtn = document.getElementById('select-all');
    const clearAllBtn = document.getElementById('clear-all');
    
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            // Only select visible checkboxes (in case search is active)
            checkboxes.forEach(checkbox => {
                if (checkbox.parentNode.style.display !== 'none') {
                    checkbox.checked = true;
                }
            });
        });
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        });
    }
    
    // Add animation to confidence bar on result page
    const confidenceFill = document.querySelector('.confidence-fill');
    if (confidenceFill) {
        const targetWidth = confidenceFill.style.width;
        confidenceFill.style.width = '0%';
        
        setTimeout(function() {
            confidenceFill.style.transition = 'width 1s ease-in-out';
            confidenceFill.style.width = targetWidth;
        }, 100);
    }
}); 