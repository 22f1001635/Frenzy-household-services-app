<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Add Service</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="service">
                <form>
                  <div class="mb-1">
                      <label for="serviceName" class="form-label">Service Name:</label>
                      <input type="text" class="form-control" id="serviceName" required>
                  </div>
                  <div class="mb-1">
                      <label for="description" class="form-label">Description:</label>
                      <textarea class="form-control" id="description" rows="2" required></textarea>
                  </div>
                  <div class="mb-1">
                      <label for="reqTime" class="form-label">Time required:</label>
                      <input type="number" class="form-control" id="reqTime" min="10" step="5" max="180" required placeholder="??">
                  </div>
                  <div class="mb-1">
                      <label for="basePrice" class="form-label">Base Price:</label>
                      <input type="number" class="form-control" id="basePrice" min="10" required placeholder="₹">
                  </div>
                  <div class="mb-2">
                      <label for="serviceLocations" class="form-label">Service Pincodes:</label>
                      <input type="number" class="form-control" id="serviceLocations" placeholder="Enter Pincodes">
                    </div>
                  <div class="d-flex gap-4 py-2" style="margin-left: 5.75vw;">
                      <button type="submit" class="btn btn-success">Add</button>
                      <button type="button" class="btn btn-warning">Cancel</button>
                  </div>
              </form>
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
