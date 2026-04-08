/**
 * HBnB - Scripts.js
 * Gère l'authentification, la liste des lieux, les détails et le logout.
 */

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');

  // --- ÉTAPE CRUCIALE : On vérifie l'auth sur TOUTES les pages ---
  checkAuthentication(); 

  // --- LOGIQUE PAGE LOGIN ---
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    // Si on est déjà loggé et qu'on essaie d'aller sur login.html, on renvoie à l'accueil
    if (token) {
        window.location.href = '/';
        return;
    }
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }

  // --- LOGIQUE PAGE INDEX ---
  const placesList = document.getElementById('places-list');
  if (placesList) {
    // On a déjà appelé checkAuthentication() plus haut, donc on gère juste le filtre ici
    setupPriceFilter();    
  }

  // --- LOGIQUE PAGE DETAILS (PLACE.HTML) ---
  const placeDetailsSection = document.getElementById('place-details'); 
  if (placeDetailsSection) {
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (placeId) {
      // Afficher le formulaire de review seulement si l'utilisateur est connecté
      if (token) {
        if (addReviewSection) addReviewSection.style.display = 'block';
      } else {
        if (addReviewSection) addReviewSection.style.display = 'none';
      }
      
      // Récupérer et afficher les détails du lieu
      fetchPlaceDetails(placeId, token);
    } else {
      // Redirection racine si aucun ID n'est fourni
      window.location.href = '/';
    }
  }

  // --- LOGIQUE ADD REVIEW PAGE ---
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
      const placeId = getPlaceIdFromURL();
      if (!token || !placeId) {
          alert("You must be logged in to add a review.");
          window.location.href = '/';
          return;
      }
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const reviewText = document.getElementById('review-text').value;
          const rating = document.getElementById('star-rating').value;
          await submitReview(token, placeId, reviewText, rating);
      });
  }
});

/* ============================================================
   TASK 1 : LOGIN & AUTHENTICATION
   ============================================================ */

async function loginUser(email, password) {
  try {
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      // Stockage du JWT dans les cookies
      document.cookie = `token=${data.access_token}; path=/; SameSite=Lax`;
      // Redirection vers la racine (Flask route '/')
      window.location.href = '/';
    } else {
      alert('Login failed: Invalid credentials');
    }
  } catch (error) {
    console.error('Login error:', error);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutBtn = document.getElementById('logout-button');
  
  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    if (logoutBtn) logoutBtn.style.display = 'none';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutBtn) {
        logoutBtn.style.display = 'block';
        logoutBtn.onclick = logoutUser;
    }
    fetchPlaces(token);
  }
}

function logoutUser() {
    // Supprime le cookie en mettant une date d'expiration passée
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    alert("You have been logged out.");
    window.location.href = '/';
}

/* ============================================================
   TASK 2 : PLACES LIST (INDEX)
   ============================================================ */

async function fetchPlaces(token) {
  try {
    const response = await fetch('/api/v1/places/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = ''; 

  places.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card';
    card.dataset.price = place.price;

    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    container.appendChild(card);
  });
}

function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.addEventListener('change', (e) => {
    const maxPrice = e.target.value;
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
      const price = parseFloat(card.dataset.price);
      card.style.display = (maxPrice === 'all' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
    });
  });
}

/* ============================================================
   TASK 3 : PLACE DETAILS (DYNAMIQUE)
   ============================================================ */

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      const container = document.getElementById('place-details');
      container.innerHTML = '<p>Error: Place not found.</p>';
    }
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

const amenityIcons = {
  "WiFi": "static/images/icon_wifi.png",
  "Bed": "static/images/icon_bed.png",
  "Bath": "static/images/icon_bath.png",
};

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  container.innerHTML = ''; 

  const detailsHTML = `
    <div class="place-info">
      <h1>${place.title}</h1>
      <p><strong>Host:</strong> ${place.owner ? (place.owner.first_name + ' ' + place.owner.last_name) : 'Unknown Host'}</p>
      
      <div class="price-tag">
        <span>Price per night: </span>
        <strong>$${place.price}</strong>
      </div>

      <p class="description"><strong>Description:</strong> ${place.description}</p>
    </div>

    <section id="amenities" class="details-section">
      <h3>Amenities</h3>
      <ul class="amenities-list" style="list-style: none; padding: 0;">
        ${place.amenities && place.amenities.length > 0 
          ? place.amenities.map(a => {
            const iconPath = amenityIcons[a.name] || "static/images/icon-default.png";
              return `
                <li style="display: flex; align-items: center; margin-bottom: 10px;">
                  <img src="${iconPath}" alt="${a.name}" style="width: 24px; height: 24px; margin-right: 10px;">
                  ${a.name}
                </li>`;
            }).join('') 
          : '<li>No amenities available.</li>'}
      </ul>
    </section>

    <section id="reviews" class="details-section">
      <h3>Reviews</h3>
      <div class="reviews-list">
        ${place.reviews && place.reviews.length > 0 
          ? place.reviews.map(r => `
            <div class="review-card">
              <p><strong>${r.user_name || 'Guest'}:</strong> ${r.text} (Rating: ${r.rating}/5)</p>
            </div>`).join('') 
          : '<p>No reviews yet for this place.</p>'}
      </div>
    </section>
  `;

  container.innerHTML = detailsHTML;

  const addReviewBtn = document.getElementById('add-review-button');
  if (addReviewBtn) {
    addReviewBtn.href = `add_review.html?id=${place.id}`;
  }
}

/* --- UTILITAIRES --- */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

/* ============================================================
   TASK 4 : ADD REVIEW LOGIC
   ============================================================ */

async function submitReview(token, placeId, text, rating) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.sub;

    try {
        const response = await fetch('/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                rating: parseInt(rating),
                user_id: userId,
                place_id: placeId
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.message || errorData.error || 'Check console'}`);
        }
    } catch (error) {
        console.error('Submission error:', error);
    }
}