<script setup>
import "@/assets/styles/main.css"
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
        <div>
          <div id="maintext" style=" width: 30%;"><h2 style="color: coral;">Frenzy: Your Home, Our Priority</h2><br><h5>At Frenzy, we're revolutionizing how you manage household services. Born from the frustration of juggling multiple service providers, we've created a one-stop solution for all your home needs.</h5><br><h5 style="padding-bottom: 28%;">We connect you with vetted professionals for tasks ranging from cleaning to pest control. Our user-friendly app offers convenience, quality assurance, flexible scheduling, and transparent pricing. Founded by industry experts, Frenzy has quickly become the preferred choice for homeowners and renters seeking efficient home management. We're dedicated to continuous improvement and expansion, aiming to make household tasks effortless for everyone. Join Frenzy today and focus on what truly matters in your life.</h5></div>
          <div id="frenzyabt">
            <img src="@/assets/images/frenzy.png" draggable="false">
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
</body>
</template>
