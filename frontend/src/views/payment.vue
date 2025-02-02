<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
<main>
<div id="forms" style="padding-top: 4%;">
  <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Payment Methods</p></div>
  <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
    <div class="cards">
      <div class="saved">
                  <p id="meth">Saved Methods</p>
                  <div class="card-items">
                    <label>
                      <input type="radio" name="saved-cards">
                      UPI/4561239857@upi
                    </label>
                    <hr>
                    <label>
                      <input type="radio" name="saved-cards">
                      Mastercard/****5241
                    </label>
                    <hr>
                    <label>
                      <input type="radio" name="saved-cards">
                      AMEX/****4906
                    </label>
                    <hr>
                  </div>
      </div>
          <div class="method-glide">
              <br>
              <label>
                <input type="radio" name="saved-cards">
                UPI
              </label>
              <hr>
              <label>
                <input type="radio" name="saved-cards">
                Credit/Debit Card
              </label>
              <hr>
              <label>
                <input type="radio" name="saved-cards">
                COD
              </label>
              <hr>
              <label>
                <input type="radio" name="saved-cards">
                Internet Banking
              </label>
            </div>
    </div>
  </div>
</div>
</main>
</body>
</template>
