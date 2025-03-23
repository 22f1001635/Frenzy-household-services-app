<script setup>
import "@/assets/styles/main.css"
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
        <div>
          <div id="maintext"><p>Home Services</p><p id="sm">at your doorstep!</p></div>
          <div id="images">
            <div id="carouselExampleAutoplaying" class="carousel slide-fade" data-bs-ride="carousel" data-bs-interval="2250" data-bs-wrap="true" data-bs-touch="false" data-bs-pause="false">
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <img src="../assets/images/barber.svg" draggable="false" style="width: 92.5%;">
                </div>
                <div class="carousel-item">
                  <img src="../assets/images/chef.svg" draggable="false" style="width: 75%;">
                </div>
                <div class="carousel-item">
                  <img src="../assets/images/engineer.svg" draggable="false" style="width: 80%;">
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
</body>
</template>
