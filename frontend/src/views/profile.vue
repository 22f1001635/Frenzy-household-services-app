<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/statistics.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
          <div id="graph4">
            <div class="outline">
                <div id="change-password" class="mt-5 pform" style="display: none;">
                  <p>Change Password</p>
                    <form>
                        <div class="mb-3 pt-4">
                            <label for="current-password" class="form-label">Current Password</label>
                            <input type="password" class="form-control" id="current-password" required>
                        </div>
                        <div class="mb-3">
                            <label for="new-password" class="form-label">New Password</label>
                            <input type="password" class="form-control" id="new-password" required>
                        </div>
                        <div class="mb-3">
                            <label for="confirm-password" class="form-label">Confirm Password</label>
                            <input type="password" class="form-control" id="confirm-password" required>
                        </div>
                        <div class="d-flex gap-4">
                        <button type="submit" class="btn btn-success" onclick="showForm('textarea')">Submit</button>
                        <button type="submit" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
                      </div>
                    </form>
                </div>
                <div id="user-prof" class="mt-5 pform" style="display: none;">
                    <p>Service Professional Registration</p>
                    <form>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" disabled>
                        </div>
                        <div class="mb-3">
                            <label for="service-name" class="form-label">Service Name</label>
                            <select class="form-select" id="service-name" required>
                                <option value="">Select available services</option>
                                <option value="service1">Service 1</option>
                                <option value="service2">Service 2</option>
                                <option value="service3">Service 3</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="experience" class="form-label">Experience (in yrs)</label>
                            <input type="number" class="form-control" id="experience" required>
                        </div>
                        <div class="form-group">
                          <label for="address">Address</label>
                          <div class="row">
                              <div class="col-md-12">
                                  <input type="text" class="form-control" id="house-no" placeholder="House No., Apartment, Housing">
                              </div>
                          </div>
                          <div class="row mt-3">
                              <div class="col-md-6">
                                  <input type="text" class="form-control" id="area-street-village" placeholder="Area/Street/Village">
                              </div>
                              <div class="col-md-6">
                                  <input type="text" class="form-control" id="landmark" placeholder="Landmark">
                              </div>
                          </div>
                          <div class="row mt-3">
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="city" placeholder="City">
                              </div>
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="state" placeholder="State">
                              </div>
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="pincode" placeholder="Pincode">
                              </div>
                          </div>
                      </div>
                      <div class="d-flex gap-4">
                        <button type="submit" class="btn btn-primary" onclick="showForm('textarea')">Submit</button>
                        <button type="submit" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
                      </div>
                    </form>
                </div>
                <div id="user-content">
                  <p id="header-wishlist">From Your Wishlist</p>
                  <div id="wishlist-container">
                    <button id="prev-btn" class="nav-arrow" style="display: none;">
                      <i class="fa-solid fa-chevron-left"></i>
                    </button>
                    <div class="wishlist-items-wrapper d-flex gap-3">
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                    </div>
                    <button id="next-btn" class="nav-arrow">
                      <i class="fa-solid fa-chevron-right"></i>
                    </button>
                  </div>
                  <p id="header-previous" style="padding-top: 0vw;">Previously Ordered</p>
                  <div id="previous-container">
                    <button id="prev-btn" class="nav-arrow" style="display: none;">
                      <i class="fa-solid fa-chevron-left"></i>
                    </button>
                    <div class="previous-items-wrapper d-flex gap-3">
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                      <div id="previous-item">
                        <div id="previous-item-image">

                        </div>
                        <p id="item-name">Saksham Sirohi Ji</p>
                        <div class="d-flex gap-4 px-4">
                        <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                        <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                        </div>
                      </div>
                    </div>
                    <button id="next-btn" class="nav-arrow">
                      <i class="fa-solid fa-chevron-right"></i>
                    </button>
                  </div>
                </div>
            </div>
        </div>
        <div id="graph5">
          <div id="prof">
            <div id="pic"><img src="../assets/images/profile.png" draggable="false"><button class="btn btn-warning" style="border-radius: 50%;" onclick="showForm('change-password')"><i class="fa-solid fa-key"></i></button></div>
            <p>Name</p>
            <p id="ori">{Name}</p><hr>
            <p>Email</p>
            <p id="ori">{Email}</p><hr>
            <p>Address</p>
            <p id="ori">{hufdsnhfn fnisd nhfn df nndshnfsunanf nasenfnnsdhif njasn fi}</p><hr>
            <p>User-Type</p>
            <p id="ori">{User-Type}</p><hr>
            <div class="px-4"><button type="button" class="btn btn-warning" onclick="showForm('user-prof')"><p id="ori">Are you a service professional?</p></button></div>
          </div>
        </div>
    </main>
    <!--
    <script>
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
  </script>
  -->
</body>
</template>
