<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Your Wishlist</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
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
</body>
</template>
