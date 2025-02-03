<script setup>
import "@/assets/styles/main.css"
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
        <div>
          <div id="maintext"><h1>Home Services</h1><h3>at your doorstep!</h3></div>
          <div id="products">
            <div class="d-flex">
            <div id="womenspa"></div>
            <div id="menmassage"></div>
            <div id="acappliance"></div></div>
            <div id="pestcontrol"></div>
            <div id="carpenter"></div>
            <div id="painting"></div>
            <div id="cleaning"></div>
          </div>
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
