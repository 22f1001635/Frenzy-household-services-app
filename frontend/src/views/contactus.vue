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
          <div id="maintext">
            <br>
            <h1>Let's Talk</h1>
            <h5>Have some big idea or brand to develop and need help? Then reach out we'd love to hear about your project  and provide help</h5>
            <br>
            <br>
            <h3>Email</h3>
            <p></p>
            <a href=""><h6>support@frenzy.com</h6></a>
            <br>
            <br>
            <h3>Socials</h3>
            <br>
            <a href="#"><h6>Twitter</h6></a>
            <a href="#"><h6>Instagram</h6></a>
            <a href="#"><h6>Facebook</h6></a>
            <br>
          </div>
          <div id="form-contact">
            <form>
              <div class="form-group pb-3 pt-3">
                <label for="exampleFormControlInput1">Name</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Your name here">
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlInput1">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlSelect1">Query select</label>
                <select class="form-control" id="exampleFormControlSelect1">
                <optgroup label="Select Query Type">
                  <option selected disabled hidden>Select Query Type</option>
                  <option>General Query</option>
                  <option>Complaint</option>
                  <option>Report Fradulant Activity</option>
                </optgroup>
                </select>
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlTextarea1">Message</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="5" placeholder="Provide necessary details for the project such as budget,type of service,etc."></textarea>
              </div>
              <div class="form-group">
                <div class="d-grid gap-2 col-6 mx-auto pt-2">
                  <button type="submit" class="btn btn-primary btn-block ">Submit & Connect</button>
                </div>
              </div>
            </form>
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
