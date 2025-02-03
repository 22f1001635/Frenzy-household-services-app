
<template>
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
          <div class="find">
            <div class="search-container me-2">
              <input class="form-control" type="search" placeholder="Search" id="searchInput">
              <div class="search-modal" id="searchModal">
                <div class="p-2">
                  <div class="search-results">
                    <div class="search-item">
                      Sample Result 1
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div id="shopping" style="padding-left: 3vw;">
            <a href=""><i class="fa-solid fa-cart-shopping" draggable="false"></i></a>
          </div>
          <div id="user">
            <a href=""><i class="fa-solid fa-user" draggable="false"></i>{ SignInUp }</a>
          </div>
        </div>
      </div>
    </nav>
  </template>
