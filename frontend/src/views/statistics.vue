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
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Services
                </a>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#">Beauty</a></li>
                  <li><a class="dropdown-item" href="#">Cleaning</a></li>
                  <li><a class="dropdown-item" href="#">Essentials</a></li>
                </ul>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">About</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Contact Us</a>
              </li>
            </ul>
            <!--needs to be tested later upon linking-->
            <form class="d-flex" role="search">
              <input class="form-control" type="search" placeholder="Search" aria-label="Search">
            </form>
            <div id="shopping"><a href=""><i class="fa-solid fa-cart-shopping" draggable="false"></i></a></div>
            <div id="user"><a href=""><i class="fa-solid fa-user" draggable="false"></i>{{SignIn/Up}}</a></div>
          </div>
        </div>
      </nav>
    <main>
        <div id="graph1">

        </div>
        <div id="graph2">

        </div>
        <div id="graph3">

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
