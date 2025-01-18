<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%; padding-bottom: 7%;">
        <div id="box" class="bg-light text-dark" style="padding: 1vw;">
            <div class="mainform">
              <div class="cart">
                <!--
                <div class="order-confirm">
                  <i class="fa-regular fa-circle-check fa-beat" style="color: #00ff00; font-size: 6vw;"></i>
                  <h3>Payment Successfully Completed for {{Service Name}} with ID-{{61651165151}} for {{AssignedDate}}</h3>
                  <h4>Service Professional will be assigned for your visit shortly</h4>
                  <h6> You will be redirected to dashboard in <span id="secs">3</span> seconds.</h6>
                </div>
                -->
                <div class="order-confirm">
                  <i class="fa-regular fa-circle-xmark fa-beat-fade" style="color: #ff8080; font-size: 6vw;"></i>
                  <h3>Payment for {Service Name} for {AssignedDate} has failed</h3>
                  <h5>Any amount if deducted from your account will be refunded shortly, for any problems <a href="">contact us</a></h5>
                  <h6> You will be redirected to dashboard in <span id="secs">3</span> seconds.</h6>
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
      var seconds = 3; // seconds HTML
      var elapsed; // variable clearInterval()
      function redirect() {
          document.location.href = './home.html';
      }
      function updateSecs() {
          document.getElementById("secs").innerHTML = seconds;
          seconds--;
          if (seconds == -1) {
              clearInterval(elapsed);
              redirect();
          }
      }
      function countdownTimer() {
          elapsed = setInterval(function () {
              updateSecs()
          }, 1000);
      }
      countdownTimer();
      </script>
      -->
</body>
</template>
