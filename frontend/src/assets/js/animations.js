document.addEventListener('DOMContentLoaded', function() {
  // Section Toggle Functionality (from address.vue)
  window.showSection = function(sectionId) {
      // Hide all sections first
      const savedAddressSection = document.getElementById('savedAddressSection');
      const newAddressSection = document.getElementById('newAddressSection');
      const userContent = document.getElementById('user-content');
  
      if (savedAddressSection) savedAddressSection.style.display = 'none';
      if (newAddressSection) newAddressSection.style.display = 'none';
      
      // Show the selected section
      if (sectionId === 'textarea' && userContent) {
          userContent.style.display = 'block';
      } else {
          const targetSection = document.getElementById(sectionId);
          if (targetSection) {
              targetSection.style.display = 'inline';
              if (userContent) userContent.style.display = 'none';
          }
      }
  };

  // Profile Form Toggle Functionality (from profile.vue)
  window.showForm = function(formId) {
      // Hide all forms first
      const forms = document.querySelectorAll('.pform');
      forms.forEach(form => form.style.display = 'none');
      
      const userContent = document.getElementById('user-content');
      
      if (formId === 'textarea') {
          // If 'textarea' is passed, show user-content and hide forms
          if (userContent) userContent.style.display = 'block';
      } else {
          // For any other form, hide user-content and show the requested form
          if (userContent) userContent.style.display = 'none';
          const targetForm = document.getElementById(formId);
          if (targetForm) targetForm.style.display = 'block';
      }
  };

  // Countdown Timer Functionality (from confirmorder.vue)
  function initCountdownTimer() {
      const secsElements = document.querySelectorAll("#secs");
      if (!secsElements.length) return;
  
      secsElements.forEach(secsElement => {
          let seconds = 3;
          let elapsed;
  
          function redirect() {
              // Updated to use a relative path or specific route
              window.location.href = '/dashboard'; // Adjust this to your actual dashboard route
          }
  
          function updateSecs() {
              secsElement.innerHTML = seconds;
              seconds--;
              if (seconds === -1) {
                  clearInterval(elapsed);
                  redirect();
              }
          }
  
          elapsed = setInterval(updateSecs, 1000);
      });
  }
  window.addEventListener('vue-component-countdown', () => {
    initCountdownTimer();
  });

  // Star Rating Functionality (from review.vue)
  function setupStarRating() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    
    console.log(stars, ratingInput); // Debugging line

    if (!stars.length || !ratingInput) return;

    function highlightStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }
    
    function setRating(rating) {
        ratingInput.value = rating;
        highlightStars(rating);
    }

    stars.forEach((star, index) => {
        star.addEventListener('mouseover', () => {
            highlightStars(index + 1);
        });
    
        star.addEventListener('mouseout', () => {
            highlightStars(parseInt(ratingInput.value));
        });
    
        star.addEventListener('click', () => {
            setRating(index + 1);
        });
    });
}

  // Listen for the custom event and run the setup
  window.addEventListener('vue-component-starsystem', () => {
      setupStarRating();
  });

  // Scroll Arrows for Wishlist and Previous Items (from profile.vue)
  function setupScrollArrows(containerClass) {
    const container = document.querySelector(`.${containerClass}`);
    if (!container) return;

    const prevBtn = container.parentElement.querySelector('#prev-btn');
    const nextBtn = container.parentElement.querySelector('#next-btn');
    
    if (!prevBtn || !nextBtn) return;

    // Ensure buttons are always visible
    prevBtn.style.display = 'block';
    nextBtn.style.display = 'block';

    function updateArrowVisibility() {
        const isAtStart = container.scrollLeft === 0;
        const isAtEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth;
        
        // Adjust opacity based on scroll position
        prevBtn.style.opacity = isAtStart ? '0.33' : '1';
        nextBtn.style.opacity = isAtEnd ? '0.33' : '1';
    }
    
    // Initial check
    updateArrowVisibility();
    
    // Scroll amount for each click (350px)
    const scrollAmount = 350;
    
    // Add click handlers for navigation
    nextBtn.addEventListener('click', () => {
        container.scrollLeft += scrollAmount;
        setTimeout(updateArrowVisibility, 100);
    });
    
    prevBtn.addEventListener('click', () => {
        container.scrollLeft -= scrollAmount;
        setTimeout(updateArrowVisibility, 100);
    });
    
    // Update arrow visibility on scroll
    container.addEventListener('scroll', updateArrowVisibility);
    
    // Update arrow visibility on window resize
    window.addEventListener('resize', updateArrowVisibility);
}

  // Setup arrows for both wishlist and previous items containers
  window.addEventListener('vue-component-itemwrap', () => {
      setupScrollArrows('wishlist-items-wrapper');
      setupScrollArrows('previous-items-wrapper');
  });

  // Search Functionality (from profile.vue)
  function setupSearchFunctionality() {
      const searchInput = document.getElementById('searchInput');
      const searchModal = document.getElementById('searchModal');
      
      if (!searchInput || !searchModal) return;

      searchInput.addEventListener('click', function(e) {
          searchModal.style.display = 'block';
          e.stopPropagation();
      });

      document.addEventListener('click', function(e) {
          if (!searchModal.contains(e.target) && e.target !== searchInput) {
              searchModal.style.display = 'none';
          }
      });

      searchModal.addEventListener('click', function(e) {
          e.stopPropagation();
      });

      document.querySelectorAll('.search-item').forEach(item => {
          item.addEventListener('click', function() {
              searchInput.value = this.textContent.trim();
              searchModal.style.display = 'none';
          });
      });
  }
  window.addEventListener('vue-component-search', () => {
    setupSearchFunctionality();
  });
});