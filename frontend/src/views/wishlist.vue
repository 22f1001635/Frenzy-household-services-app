<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Your Wishlist</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform">
              <div class="cart">
                <div class="cart-member">
                    <div class="cart-memeber-photo"></div>
                    <h3 style="margin: 2.75vw;">byuoigy</h3>
                    <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                    <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                </div>
                <div class="cart-member">
                  <div class="cart-memeber-photo"></div>
                  <h3 style="margin: 2.75vw;">byuoigy</h3>
                  <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                  <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
              </div>
              <div class="cart-member">
                <div class="cart-memeber-photo"></div>
                <h3 style="margin: 2.75vw;">byuoigy</h3>
                <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
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
