<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Edit Service</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="service">
                <form class="pt-3">
                    <div class="form-group mb-3">
                      <label for="existingService">Select Existing Service:</label>
                      <select class="form-control" id="existingService" onchange="">
                        <option value="">A</option>
                        <!-- Options for existing services will be dynamically populated -->
                      </select>
                    </div>
                    <div class="form-group mb-3">
                      <label for="reqTime" class="form-label">Time required:</label>
                      <input type="number" class="form-control" id="reqTime" min="1" step="10" max="180" required placeholder="??">
                    </div>
                    <div class="form-group mb-3">
                      <label for="basePrice">Base Price:</label>
                      <input type="number" class="form-control" id="basePrice" placeholder="Enter base price">
                    </div>
                    <div class="form-group mb-3">
                      <label for="serviceLocations">Service Pincodes:</label>
                      <input type="number" class="form-control" id="serviceLocations" placeholder="Enter Pincodes">
                    </div>
                    <div class="d-flex py-2 gap-4 justify-content-center">
                    <button type="button" class="btn btn-success" onclick="">Update</button>
                    <button type="button" class="btn  btn-danger" onclick="">Delete</button>
                    <button type="button" class="btn  btn-secondary">Cancel</button>
                    </div>
                  </form>
              </div>
            </div>
        </div>
    </div>
    </main>
    <footer class="d-flex flex-wrap justify-content-between py-3 px-3 border-top fixed-bottom bg-body-tertiary">
        <div class="col-md-4 d-flex align-items-center">
          <a href="#" class="mb-2 me-2 mb-md-0 text-muted text-decoration-none lh-1">
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
