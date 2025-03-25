<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
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
      <div class="d-flex">
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
          <div class="detailer">
            <div class="container mt-4">
              <!-- UPI Payment -->
              <div class="row justify-content-center g-3 d-none" id="upi-payment">
                <div class="col-md-4">
                  <label for="upi-id" class="form-label">Enter UPI ID</label>
                  <input type="text" id="upi-id" class="form-control" placeholder="Enter UPI ID">
                </div>
              </div>

              <!-- Wallet Payment -->
              <div class="row justify-content-center g-3 d-none" id="wallet-payment">
                <div class="col-md-4">
                  <label for="wallet-id" class="form-label">Enter Wallet ID</label>
                  <input type="text" id="wallet-id" class="form-control" placeholder="Enter Wallet ID">
                </div>
              </div>

              <!-- Card Payment -->
              <div class="row justify-content-center g-3 pt-4" id="card-payment">
                <div class="col-md-4">
                  <label for="card-number" class="form-label">Enter Card Number</label>
                  <input type="text" id="card-number" class="form-control" placeholder="Enter Card Number">
                </div>

                <div class="col-md-3">
                  <label for="expiry-date" class="form-label">Enter Expiry Date</label>
                  <input type="text" id="expiry-date" class="form-control" placeholder="MM/YY">
                </div>

                <div class="col-md-2">
                  <label for="cvv" class="form-label">Enter CVV</label>
                  <input type="text" id="cvv" class="form-control" placeholder="CVV">
                </div>
              </div>

              <!-- Complete Order Button -->
              <div class="d-flex justify-content-center mt-4">
                <button class="btn btn-success">Complete Order</button>
              </div>
            </div>
          </div></div>
    </div>
  </div>
</div>
</main>
</body>
</template>
