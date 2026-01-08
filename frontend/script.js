/**
 * Weather Alert App - Frontend JavaScript
 * Handles API calls, DOM manipulation, and user interactions
 */

// Configuration
// const API_BASE_URL = 'http://34.236.170.49:5000';
const API_BASE_URL = '/api';
const RECENT_CITIES_KEY = 'weatherApp_recentCities';
const MAX_RECENT_CITIES = 5;

// DOM Elements
const cityInput = document.getElementById('cityInput');
const weatherBtn = document.getElementById('weatherBtn');
const forecastBtn = document.getElementById('forecastBtn');
const loader = document.getElementById('loader');
const errorMessage = document.getElementById('errorMessage');
const weatherDisplay = document.getElementById('weatherDisplay');
const forecastSection = document.getElementById('forecastSection');
const alertBanner = document.getElementById('alertBanner');
const recentCities = document.getElementById('recentCities');
const cityChips = document.getElementById('cityChips');
const autocompleteDropdown = document.getElementById('autocompleteDropdown');

// State
let currentCity = '';
let selectedAutocompleteIndex = -1;
let currentAutocompleteSuggestions = [];

/**
 * Initialize the application
 */
function init() {
    // Load recent cities from localStorage
    loadRecentCities();
    
    // Event listeners
    weatherBtn.addEventListener('click', handleWeatherRequest);
    forecastBtn.addEventListener('click', handleForecastRequest);
    
    // Autocomplete listeners
    cityInput.addEventListener('input', handleAutocomplete);
    cityInput.addEventListener('focus', handleAutocomplete);
    
    // Keyboard navigation for autocomplete
    cityInput.addEventListener('keydown', handleAutocompleteKeyboard);
    
    // Allow Enter key to trigger weather search
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && selectedAutocompleteIndex === -1) {
            handleWeatherRequest();
        }
    });
    
    // Close autocomplete when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.autocomplete-wrapper')) {
            hideAutocomplete();
        }
    });
}

/**
 * Handle current weather request
 */
// async function handleWeatherRequest() {
//     const city = cityInput.value.trim();
    
//     if (!city) {
//         showError('Please enter a city name');
//         return;
//     }
    
//     currentCity = city;
    
//     // Show loading state
//     showLoading();
//     hideError();
//     hideWeather();
//     hideForecast();
    
//     try {
//         const response = await fetch(`${API_BASE_URL}/weather?city=${encodeURIComponent(city)}`);
//         const data = await response.json();
        
//         if (!response.ok) {
//             throw new Error(data.error || 'Failed to fetch weather data');
//         }
        
//         // Save to recent cities
//         saveRecentCity(city);
        
//         // Display weather
//         displayWeather(data);
        
//     } catch (error) {
//         showError(error.message);
//     } finally {
//         hideLoading();
//     }
// }

// UPDATED ASYNC FUNCTION TO FETCH BOTH CURRENT WEATHER 
async function handleWeatherRequest() {
    const city = cityInput.value.trim();

    if (!city) {
        showError('Please enter a city name');
        return;
    }

    currentCity = city;

    // Show loading state
    showLoading();
    hideError();
    hideWeather();
    hideForecast();

    try {
        const response = await fetch(`${API_BASE_URL}/weather?city=${encodeURIComponent(city)}`);

        if (!response.ok) {
            // Try to extract error message from response
            let errMsg = `Failed to fetch weather data (status: ${response.status})`;
            try {
                const errData = await response.json();
                if (errData.error) errMsg = errData.error;
            } catch (e) {
                // response not JSON, keep default message
            }
            throw new Error(errMsg);
        }

        // Parse JSON after confirming response is OK
        const data = await response.json();

        // Save to recent cities
        saveRecentCity(city);

        // Display weather
        displayWeather(data);

    } catch (error) {
        // Network errors or thrown errors
        showError(`❌ ${error.message}`);
    } finally {
        hideLoading();
    }
}



/**
 * Handle forecast request
 */
async function handleForecastRequest() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    currentCity = city;
    
    // Show loading state
    showLoading();
    hideError();
    hideWeather();
    hideForecast();
    
    try {
        const response = await fetch(`${API_BASE_URL}/forecast?city=${encodeURIComponent(city)}`);


        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch forecast data');
        }
        
        // Save to recent cities
        saveRecentCity(city);
        
        // Display current weather and forecast
        displayWeather(data.current);
        displayForecast(data.forecast);
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Display current weather data
 */
function displayWeather(data) {
    // Update city name
    document.getElementById('cityName').textContent = `${data.city}, ${data.country}`;
    
    // Update timestamp
    const timestamp = new Date(data.timestamp).toLocaleString();
    document.getElementById('timestamp').textContent = `Updated: ${timestamp}`;
    
    // Update temperature
    document.getElementById('temperature').textContent = `${data.temperature}°C`;
    
    // Update weather icon
    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    document.getElementById('weatherIcon').src = iconUrl;
    document.getElementById('weatherIcon').alt = data.condition;
    
    // Update condition
    document.getElementById('condition').textContent = data.description;
    
    // Update details
    document.getElementById('feelsLike').textContent = `${data.feels_like}°C`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    document.getElementById('pressure').textContent = `${data.pressure} hPa`;
    
    // Show/hide alert banner
    if (data.alert) {
        alertBanner.textContent = `⚠️ ${data.alert}`;
        alertBanner.classList.add('active');
        
        // Set alert type class
        if (data.alert.includes('High')) {
            alertBanner.classList.add('high-temp');
            alertBanner.classList.remove('low-temp');
        } else {
            alertBanner.classList.add('low-temp');
            alertBanner.classList.remove('high-temp');
        }
    } else {
        alertBanner.classList.remove('active');
    }
    
    // Show weather display
    weatherDisplay.classList.add('active');
}

/**
 * Display 5-day forecast
 */
function displayForecast(forecastData) {
    const forecastGrid = document.getElementById('forecastGrid');
    forecastGrid.innerHTML = '';
    
    forecastData.forEach(day => {
        const card = document.createElement('div');
        card.className = 'forecast-card';
        
        const iconUrl = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;
        
        card.innerHTML = `
            <div class="forecast-day">${day.day_name}</div>
            <div class="forecast-date">${formatDate(day.date)}</div>
            <img src="${iconUrl}" alt="${day.condition}">
            <div class="forecast-condition">${day.condition}</div>
            <div class="forecast-temps">
                <span class="temp-max">↑ ${day.max_temp}°</span>
                <span class="temp-min">↓ ${day.min_temp}°</span>
            </div>
        `;
        
        forecastGrid.appendChild(card);
    });
    
    forecastSection.classList.add('active');
}

/**
 * Format date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

/**
 * Save city to recent searches
 */
function saveRecentCity(city) {
    let cities = getRecentCities();
    
    // Remove city if already exists (to add it to front)
    cities = cities.filter(c => c.toLowerCase() !== city.toLowerCase());
    
    // Add to front
    cities.unshift(city);
    
    // Keep only MAX_RECENT_CITIES
    cities = cities.slice(0, MAX_RECENT_CITIES);
    
    // Save to localStorage
    localStorage.setItem(RECENT_CITIES_KEY, JSON.stringify(cities));
    
    // Update UI
    displayRecentCities();
}

/**
 * Get recent cities from localStorage
 */
function getRecentCities() {
    const stored = localStorage.getItem(RECENT_CITIES_KEY);
    return stored ? JSON.parse(stored) : [];
}

/**
 * Load and display recent cities
 */
function loadRecentCities() {
    displayRecentCities();
}

/**
 * Display recent cities as clickable chips
 */
function displayRecentCities() {
    const cities = getRecentCities();
    cityChips.innerHTML = '';
    
    if (cities.length === 0) {
        cityChips.innerHTML = '<span style="color: var(--text-secondary); font-size: 0.9rem;">No recent searches</span>';
        return;
    }
    
    cities.forEach(city => {
        const chip = document.createElement('div');
        chip.className = 'city-chip';
        chip.textContent = city;
        chip.addEventListener('click', () => {
            cityInput.value = city;
            handleWeatherRequest();
        });
        cityChips.appendChild(chip);
    });
}

/**
 * Show loading state
 */
function showLoading() {
    loader.classList.add('active');
    weatherBtn.disabled = true;
    forecastBtn.disabled = true;
}

/**
 * Hide loading state
 */
function hideLoading() {
    loader.classList.remove('active');
    weatherBtn.disabled = false;
    forecastBtn.disabled = false;
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = `❌ ${message}`;
    errorMessage.classList.add('active');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.classList.remove('active');
}

/**
 * Hide weather display
 */
function hideWeather() {
    weatherDisplay.classList.remove('active');
}

/**
 * Hide forecast display
 */
function hideForecast() {
    forecastSection.classList.remove('active');
}

/**
 * Handle autocomplete input
 */
function handleAutocomplete(e) {
    const query = cityInput.value.trim().toLowerCase();
    
    if (query.length === 0) {
        hideAutocomplete();
        return;
    }
    
    // Filter cities that match the query
    const suggestions = POPULAR_CITIES.filter(city => 
        city.name.toLowerCase().includes(query) ||
        city.country.toLowerCase().includes(query)
    ).slice(0, 8); // Limit to 8 suggestions
    
    currentAutocompleteSuggestions = suggestions;
    selectedAutocompleteIndex = -1;
    
    if (suggestions.length > 0) {
        displayAutocompleteSuggestions(suggestions);
    } else {
        displayNoResults();
    }
}

/**
 * Display autocomplete suggestions
 */
function displayAutocompleteSuggestions(suggestions) {
    autocompleteDropdown.innerHTML = '';
    
    suggestions.forEach((city, index) => {
        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.dataset.index = index;
        
        item.innerHTML = `
            <span class="city-name">${highlightMatch(city.name, cityInput.value)}</span>
            <span class="country-name">${city.country}</span>
        `;
        
        item.addEventListener('click', () => {
            selectCity(city.name);
        });
        
        autocompleteDropdown.appendChild(item);
    });
    
    autocompleteDropdown.classList.add('active');
}

/**
 * Display no results message
 */
function displayNoResults() {
    autocompleteDropdown.innerHTML = '<div class="autocomplete-no-results">No cities found. Try a different search.</div>';
    autocompleteDropdown.classList.add('active');
}

/**
 * Highlight matching text
 */
function highlightMatch(text, query) {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<strong>$1</strong>');
}

/**
 * Handle keyboard navigation in autocomplete
 */
function handleAutocompleteKeyboard(e) {
    const items = autocompleteDropdown.querySelectorAll('.autocomplete-item');
    
    if (items.length === 0) return;
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedAutocompleteIndex = Math.min(selectedAutocompleteIndex + 1, items.length - 1);
        updateAutocompleteSelection(items);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedAutocompleteIndex = Math.max(selectedAutocompleteIndex - 1, -1);
        updateAutocompleteSelection(items);
    } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedAutocompleteIndex >= 0) {
            const selectedCity = currentAutocompleteSuggestions[selectedAutocompleteIndex];
            selectCity(selectedCity.name);
        } else {
            handleWeatherRequest();
        }
    } else if (e.key === 'Escape') {
        hideAutocomplete();
        cityInput.blur();
    }
}

/**
 * Update autocomplete selection highlighting
 */
function updateAutocompleteSelection(items) {
    items.forEach((item, index) => {
        if (index === selectedAutocompleteIndex) {
            item.classList.add('selected');
            item.scrollIntoView({ block: 'nearest' });
        } else {
            item.classList.remove('selected');
        }
    });
}

/**
 * Select a city from autocomplete
 */
function selectCity(cityName) {
    cityInput.value = cityName;
    hideAutocomplete();
    handleWeatherRequest();
}

/**
 * Hide autocomplete dropdown
 */
function hideAutocomplete() {
    autocompleteDropdown.classList.remove('active');
    selectedAutocompleteIndex = -1;
    currentAutocompleteSuggestions = [];
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
