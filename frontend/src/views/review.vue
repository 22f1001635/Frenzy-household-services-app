<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Service Remarks</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform">
              <div class="cart">
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-lg-8">
                            <div class="form-container">
                                <p class="text-center request-id mb-4">Request ID:{xxx-xxx}</p>
                                <form>
                                    <div class="row mb-3">
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Service Name</label>
                                            <input type="text" class="form-control" disabled placeholder="{}">
                                        </div>
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Description</label>
                                            <input type="text" class="form-control" disabled placeholder="{}">
                                        </div>
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Date</label>
                                            <input type="date" class="form-control" disabled placeholder="{}">
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Professional ID</label>
                                            <input type="text" class="form-control" disabled placeholder="{}">
                                        </div>
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Professional Name</label>
                                            <input type="text" class="form-control" disabled placeholder="{}">
                                        </div>
                                        <div class="col-md-4 mb-2">
                                            <label class="form-label">Contact No.</label>
                                            <input type="tel" class="form-control" disabled placeholder="{}">
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label d-block">Service Rating (5 being the best):</label>
                                        <div class="star-rating">
                                            <input type="hidden" id="rating" name="rating" value="0" required>
                                            <div class="stars">
                                              <i class="star fa-solid fa-star" data-value="1"></i>
                                              <i class="star fa-solid fa-star" data-value="2"></i>
                                              <i class="star fa-solid fa-star" data-value="3"></i>
                                              <i class="star fa-solid fa-star" data-value="4"></i>
                                              <i class="star fa-solid fa-star" data-value="5"></i>
                                            </div>
                                            <div class="invalid-feedback">Please select a rating.</div>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Remarks (if any):</label>
                                        <textarea class="form-control" rows="4"></textarea>
                                    </div>
                                    <div class="d-flex gap-3 justify-content-center py-2">
                                        <button type="submit" class="btn btn-success">Submit</button>
                                        <button type="button" class="btn btn-secondary">Close</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
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
    <!--
    <script>
        const stars = document.querySelectorAll('.star');
        const ratingInput = document.getElementById('rating');
        
        stars.forEach((star, index) => {
          star.addEventListener('mouseover', () => {
            highlightStars(index + 1);
          });
        
          star.addEventListener('mouseout', () => {
            highlightStars(parseInt(ratingInput.value));
          });
        
          star.addEventListener('click', () => {
            setRating(index + 1);
          });
        });
        
        function highlightStars(rating) {
          stars.forEach((star, index) => {
            if (index < rating) {
              star.classList.add('active');
            } else {
              star.classList.remove('active');
            }
          });
        }
        
        function setRating(rating) {
          ratingInput.value = rating;
          highlightStars(rating);
        }
        </script>
        -->
</body>
</template>
