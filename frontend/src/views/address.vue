<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
<main>
  <div id="forms" style="padding-top: 4%;">
    <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left"></i></a><p class="text-dark" id="head">Select Address</p></div>
      <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
        <div class="mainform">
          <div class="address">
            <div id="savedAddressSection" >
            <div class="saved" style="padding-top: 0.5vw;">
              <h5>Saved Addresses</h5>
              <div class="address-items">
                <label>
                  <input type="radio" name="saved-address">
                  123 Main St, Anytown, AT 12345
                </label>
                <hr>
                <label>
                  <input type="radio" name="saved-address">
                  123 Main St, Anytown, AT 12345
                </label>
                <hr>
                <label>
                  <input type="radio" name="saved-address">
                  123 Main St, Anytown, AT 12345
                </label>
                <hr>
              </div>
            </div>
            <a href="#" onclick="showSection('newAddressSection'); return false;">+ Add a new address</a></div>
            <div id="newAddressSection" style="display: none;">
            <div class="new" style="padding-top: 0.5vw;">
              <p>Add a new address</p>
              <form>
                <div class="container">
                  <div class="row">
                    <div class="col-md-5 mb-2">
                      <input type="text" class="form-control" id="inputAddress" placeholder="House No., Apartment, Housing">
                    </div>
                    <div class="col-md-5 mb-2">
                      <input type="text" class="form-control" id="inputArea" placeholder="Area/Street/Village">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-4 mb-2">
                      <input type="text" class="form-control" id="inputLandmark" placeholder="Landmark">
                    </div>
                    <div class="col-sm-6 col-md-2 mb-2">
                      <input type="text" class="form-control" id="inputCity" placeholder="City">
                    </div>
                    <div class="col-sm-6 col-md-2 mb-2">
                      <input type="text" class="form-control" id="inputState" placeholder="State">
                    </div>
                    <div class="col-sm-6 col-md-2 mb-2">
                      <input type="text" class="form-control" id="inputPincode" placeholder="Pincode">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-12">
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="gridCheck">
                        <label class="form-check-label" for="gridCheck">
                          Set as Default Address
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </form>              
            </div>
            <a href="#" onclick="showSection('savedAddressSection'); return false;">Select Saved Address</a></div>
            <hr>
            <div class="date-slot">
              <label for="service-date"><h5>Service Date</h5></label><br>
              <div id="datepicker"><input type="date" name="service-date"></div>
            </div>
            <div class="time-slot">
              <h5>Select Service Slot</h5>
              <label>
                <input type="radio" name="slot">
                9:00 AM
              </label>
              <label>
                <input type="radio" name="slot">
                11:00 AM
              </label>
              <label>
                <input type="radio" name="slot">
                1:00 PM
              </label>
              <label>
                <input type="radio" name="slot">
                3:00 PM
              </label>
              <label>
                <input type="radio" name="slot">
                5:00 PM
              </label>
            </div>
            <button type="button" class="btn btn-dark"><i class="fa-duotone fa-solid fa-arrow-right "></i> Proceed to Pay</button>
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
    <!--
    <script>
      function showSection(sectionId) {
          // Hide all sections first
          document.getElementById('savedAddressSection').style.display = 'none';
          document.getElementById('newAddressSection').style.display = 'none';
          
          // Show the selected section
          document.getElementById(sectionId).style.display = 'inline';
      }
      </script>
      -->
</body>
</template>
