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
          <div id="maintext"><h1>Home Services</h1><h3>at your doorstep!</h3></div>
          <div id="products">
            <div class="d-flex">
            <div id="womenspa"></div>
            <div id="menmassage"></div>
            <div id="acappliance"></div></div>
            <div id="pestcontrol"></div>
            <div id="carpenter"></div>
            <div id="painting"></div>
            <div id="cleaning"></div>
          </div>
          <div id="images">
            <div id="carouselExampleAutoplaying" class="carousel slide-fade" data-bs-ride="carousel" data-bs-interval="2250" data-bs-wrap="true" data-bs-touch="false" data-bs-pause="false">
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <img src="../assets/images/barber.svg" draggable="false" style="width: 92.5%;">
                </div>
                <div class="carousel-item">
                  <img src="../assets/images/chef.svg" draggable="false" style="width: 75%;">
                </div>
                <div class="carousel-item">
                  <img src="../assets/images/engineer.svg" draggable="false" style="width: 80%;">
                </div>
              </div>
            </div>
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
