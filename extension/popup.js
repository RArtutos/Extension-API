// Popup Script
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const profileManager = document.getElementById('profile-manager');
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');

  // Check if user is logged in
  chrome.storage.local.get(['token'], function(result) {
    if (result.token) {
      showProfileManager();
      loadProfiles();
    } else {
      showLoginForm();
    }
  });

  loginBtn.addEventListener('click', async () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://localhost:3000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (data.token) {
        chrome.storage.local.set({ token: data.token }, function() {
          showProfileManager();
          loadProfiles();
        });
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  });

  logoutBtn.addEventListener('click', () => {
    chrome.storage.local.remove(['token'], function() {
      showLoginForm();
    });
  });

  function showLoginForm() {
    loginForm.classList.remove('hidden');
    profileManager.classList.add('hidden');
  }

  function showProfileManager() {
    loginForm.classList.add('hidden');
    profileManager.classList.remove('hidden');
  }

  async function loadProfiles() {
    try {
      const token = await new Promise(resolve => {
        chrome.storage.local.get(['token'], result => resolve(result.token));
      });

      const response = await fetch('http://localhost:3000/api/profiles', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const profiles = await response.json();
      const profilesList = document.getElementById('profiles-list');
      profilesList.innerHTML = profiles.map(profile => `
        <div class="profile-item">
          <span>${profile.name}</span>
          <button onclick="switchProfile(${profile.id})">Switch</button>
        </div>
      `).join('');
    } catch (error) {
      console.error('Failed to load profiles:', error);
    }
  }
});