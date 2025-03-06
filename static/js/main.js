/**
 * ArabiChat - Main JavaScript functionality
 */

// Provider model definitions
const providerModels = {
    openai: [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o"
    ],
    anthropic: [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ],
    mistral: [
        "mistral-tiny",
        "mistral-small",
        "mistral-medium",
        "mistral-large-latest"
    ],
    openrouter: [
        "openai/gpt-3.5-turbo",
        "openai/gpt-4",
        "openai/gpt-4-turbo",
        "anthropic/claude-3-opus-20240229",
        "anthropic/claude-3-sonnet-20240229",
        "anthropic/claude-3-haiku-20240307",
        "mistral/mistral-small-latest",
        "mistral/mistral-medium-latest",
        "mistral/mistral-large-latest"
    ]
};

// Default settings
const defaultLLMSettings = {
    enabled: false,
    provider: "openai",
    model: "gpt-3.5-turbo",
    apiKey: ""
};

// Get LLM settings from localStorage
function getLLMSettings() {
    const savedSettings = localStorage.getItem('llmSettings');
    if (savedSettings) {
        try {
            return JSON.parse(savedSettings);
        } catch (e) {
            console.error("Error parsing LLM settings:", e);
            return { ...defaultLLMSettings };
        }
    }
    return { ...defaultLLMSettings };
}

// Save LLM settings to localStorage
function saveLLMSettings(settings) {
    localStorage.setItem('llmSettings', JSON.stringify(settings));
}

// Populate model dropdown based on selected provider
function populateModelDropdown(provider) {
    const modelSelect = $('#llmModel');
    modelSelect.empty();
    
    // First try to get models from server
    $.ajax({
        url: '/llm-models',
        type: 'GET',
        success: function(response) {
            if (response.status === 'success' && response.models && response.models[provider]) {
                const models = response.models[provider];
                models.forEach(model => {
                    modelSelect.append($('<option>', {
                        value: model,
                        text: model
                    }));
                });
                
                // Select first model as default or previously selected model if available
                const settings = getLLMSettings();
                if (settings.provider === provider && models.includes(settings.model)) {
                    modelSelect.val(settings.model);
                }
            } else {
                // Fall back to local models if server doesn't respond properly
                useLocalModels(provider, modelSelect);
            }
        },
        error: function() {
            // Fall back to local models
            useLocalModels(provider, modelSelect);
        }
    });
}

// Use local model definitions as fallback
function useLocalModels(provider, modelSelect) {
    const models = providerModels[provider] || [];
    models.forEach(model => {
        modelSelect.append($('<option>', {
            value: model,
            text: model
        }));
    });
    
    // Select first model as default or previously selected model if available
    const settings = getLLMSettings();
    if (settings.provider === provider && models.includes(settings.model)) {
        modelSelect.val(settings.model);
    }
}

// Initialize LLM settings UI
function initLLMSettings() {
    const settings = getLLMSettings();
    
    // Set initial values
    $('#enableLLMFallback').prop('checked', settings.enabled);
    $('#llmProvider').val(settings.provider);
    $('#llmApiKey').val(settings.apiKey);
    
    // Populate models dropdown
    populateModelDropdown(settings.provider);
    
    // Update UI state based on settings
    updateLLMUIState(settings);
    
    // Provider change handler
    $('#llmProvider').on('change', function() {
        const provider = $(this).val();
        populateModelDropdown(provider);
    });
    
    // Save settings button
    $('#saveLLMSettings').on('click', function() {
        const newSettings = {
            enabled: $('#enableLLMFallback').is(':checked'),
            provider: $('#llmProvider').val(),
            model: $('#llmModel').val(),
            apiKey: $('#llmApiKey').val()
        };
        
        saveLLMSettings(newSettings);
        updateLLMUIState(newSettings);
        
        // Show success toast
        showToast('Settings saved successfully', 'success');
        
        // Close the settings panel
        $('#llmSettingsCollapse').collapse('hide');
    });
    
    // Reset button
    $('#resetLLMSettings').on('click', function() {
        if (confirm('Are you sure you want to reset all AI settings to defaults? This will clear your API key.')) {
            saveLLMSettings({ ...defaultLLMSettings });
            
            // Update form values
            $('#enableLLMFallback').prop('checked', defaultLLMSettings.enabled);
            $('#llmProvider').val(defaultLLMSettings.provider);
            $('#llmApiKey').val('');
            
            // Update models
            populateModelDropdown(defaultLLMSettings.provider);
            
            // Update UI state
            updateLLMUIState(defaultLLMSettings);
            
            showToast('Settings reset to defaults', 'info');
        }
    });
    
    // Toggle API key visibility
    $('#toggleApiKeyVisibility').on('click', function() {
        const apiKeyInput = $('#llmApiKey');
        const type = apiKeyInput.attr('type');
        
        apiKeyInput.attr('type', type === 'password' ? 'text' : 'password');
        $(this).find('i').toggleClass('fa-eye fa-eye-slash');
    });
    
    // Convert using AI button
    $('#convert-ai-btn').on('click', function() {
        convertTextUsingAI();
    });
}

// Update UI state based on settings
function updateLLMUIState(settings) {
    // Enable/disable Convert Using AI button
    const hasApiKey = settings.apiKey.trim() !== '';
    const isEnabled = settings.enabled;
    
    if (isEnabled && hasApiKey) {
        $('#convert-ai-btn').prop('disabled', false);
        $('#ai-cost-warning').removeClass('d-none');
    } else {
        $('#convert-ai-btn').prop('disabled', true);
        $('#ai-cost-warning').addClass('d-none');
    }
}

// Convert text using AI
function convertTextUsingAI() {
    const inputText = $('#input-text').val();
    const settings = getLLMSettings();
    const dialect = $('#dialect').val();
    
    if (!inputText.trim()) {
        $('#status-message').html('<span class="text-warning">Please enter some text to convert</span>');
        return;
    }
    
    if (!settings.enabled || !settings.apiKey) {
        $('#status-message').html('<span class="text-danger">AI integration is not enabled or missing API key</span>');
        return;
    }
    
    // Show loading state
    $('#convert-ai-btn').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...');
    $('#convert-ai-btn').prop('disabled', true);
    
    // Send conversion request
    $.ajax({
        url: '/convert-ai',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            text: inputText,
            dialect: dialect,
            provider: settings.provider,
            model: settings.model,
            api_key: settings.apiKey
        }),
        success: function(response) {
            if (response.status === 'success') {
                // Show output
                $('#empty-result-notice').hide();
                $('#output-container').show();
                $('#output-text').val(response.result);
                
                // Handle Arabic script output if available
                if (response.arabic_script) {
                    $('#arabic-script-notice').hide();
                    $('#arabic-script-container').show();
                    $('#arabic-script-text').val(response.arabic_script);
                } else {
                    $('#arabic-script-notice').show();
                    $('#arabic-script-container').hide();
                }
                
                $('#status-message').html('<span class="text-success">AI conversion completed successfully</span>');
            } else {
                $('#status-message').html('<span class="text-danger">Error: ' + response.message + '</span>');
            }
        },
        error: function(xhr) {
            let errorMsg = 'An error occurred during AI conversion';
            if (xhr.responseJSON && xhr.responseJSON.message) {
                errorMsg = xhr.responseJSON.message;
            }
            $('#status-message').html('<span class="text-danger">Error: ' + errorMsg + '</span>');
        },
        complete: function() {
            // Reset button state
            $('#convert-ai-btn').html('<i class="fas fa-robot"></i> Convert Using AI');
            $('#convert-ai-btn').prop('disabled', false);
        }
    });
}

// Helper function to show toast notifications
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    if ($('#toast-container').length === 0) {
        $('body').append('<div id="toast-container" class="toast-container position-fixed bottom-0 end-0 p-3"></div>');
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';
    
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center ${bgClass} text-white border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    // Add toast to container
    $('#toast-container').append(toastHtml);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    // Remove toast after it's hidden
    $(toastElement).on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

// Execute when the DOM is fully loaded
$(document).ready(function() {
    // Initialize LLM settings if the UI is present
    if ($('#llm-settings-card').length > 0) {
        initLLMSettings();
    }
});
