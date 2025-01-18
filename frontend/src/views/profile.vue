<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/statistics.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <nav class="navbar fixed-top navbar-expand-xl bg-body-tertiary">
        <div class="container-fluid py-2" id="nav2">
          <a class="navbar-brand" href="#">Frenzy</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <div id="bars"><i class="fa-solid fa-bars"></i></div>
            <div id="x-mark"><i class="fa-solid fa-xmark"></i></div>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" href="#">Services</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">About</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Contact Us</a>
              </li>
            </ul>
            <!--needs to be tested later upon linking-->
            <div class="find">
            <div class="search-container me-2">
              <input class="form-control" type="search" placeholder="Search" id="searchInput">
              <div class="search-modal" id="searchModal">
                  <div class="p-3">
                      <h6 class="mb-3">Search Results</h6>
                      <div class="search-results">
                          <div class="search-item">
                              Sample Result 1
                          </div>
                      </div>
                  </div>
              </div>
            </div>
            </div>
            <div id="shopping" style="padding-left: 3vw;"><a href=""><i class="fa-solid fa-cart-shopping" draggable="false"></i></a></div>
            <div id="user"><a href=""><i class="fa-solid fa-user" draggable="false"></i>{{SignIn/Up}}</a></div>
          </div>
        </div>
      </nav>
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
    <footer class="d-flex flex-wrap justify-content-between py-3 px-3 border-top fixed-bottom bg-body-tertiary">
        <div class="col-md-4 d-flex align-items-center">
          <a href="#" class="mb-3 me-2 mb-md-0 text-muted text-decoration-none lh-1">
            Frenzy
          </a>
          <span class="text-muted">© 2024 Frenzy, Inc</span>
        </div>
        <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-x-twitter"></i></a></li>
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-facebook"></i></a></li>
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-square-instagram"></i></a></li>
        </ul>
    </footer>
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
