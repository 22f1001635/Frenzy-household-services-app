function showSection(sectionId) {
    // Hide all sections first
    document.getElementById('savedAddressSection').style.display = 'none';
    document.getElementById('newAddressSection').style.display = 'none';
    
    // Show the selected section
    document.getElementById(sectionId).style.display = 'inline';
}
var seconds = 3; // seconds HTML
      var elapsed; // variable clearInterval()
      function redirect() {
          document.location.href = './home.html';
      }
      function updateSecs() {
          document.getElementById("secs").innerHTML = seconds;
          seconds--;
          if (seconds == -1) {
              clearInterval(elapsed);
              redirect();
          }
      }
      function countdownTimer() {
          elapsed = setInterval(function () {
              updateSecs()
          }, 1000);
      }
      countdownTimer();
      function showForm(formId) {
        // Hide all forms first
        document.querySelectorAll('.pform').forEach(form => form.style.display = 'none');
        
        // Hide user-content when showing any form
        const userContent = document.getElementById('user-content');
        
        if (formId === 'textarea') {
            // If 'textarea' is passed, show user-content and hide forms
            userContent.style.display = 'block';
        } else {
            // For any other form, hide user-content and show the requested form
            userContent.style.display = 'none';
            document.getElementById(formId).style.display = 'block';
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const searchModal = document.getElementById('searchModal');
        
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

        // Function to setup scroll arrows for a container
        function setupScrollArrows(containerClass) {
            const container = document.querySelector(`.${containerClass}`);
            const prevBtn = container.parentElement.querySelector('#prev-btn');
            const nextBtn = container.parentElement.querySelector('#next-btn');
            
            function updateArrowVisibility() {
                const isAtStart = container.scrollLeft === 0;
                const isAtEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth;
                
                prevBtn.style.display = isAtStart ? 'none' : 'block';
                nextBtn.style.display = isAtEnd ? 'none' : 'block';
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
        setupScrollArrows('wishlist-items-wrapper');
        setupScrollArrows('previous-items-wrapper');
    });
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    
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

