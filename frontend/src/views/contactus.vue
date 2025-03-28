<script setup>
import "@/assets/styles/main.css"
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
        <div>
          <div id="maintext">
            <br>
            <h1>Let's Talk</h1>
            <h5>Have some big idea or brand to develop and need help? Then reach out we'd love to hear about your project  and provide help</h5>
            <br>
            <br>
            <h3>Email</h3>
            <a href="mailto:support@frenzy.com"><h6 style="padding-top: 0.5vw;">support@frenzy.com</h6></a>
            <br>
            <h3>Socials</h3>
            <br>
            <a href="https://twitter.com/frenzy" target="_blank"><h6>Twitter</h6></a>
            <a href="https://instagram.com/frenzy" target="_blank"><h6>Instagram</h6></a>
            <a href="https://facebook.com/frenzy" target="_blank"><h6>Facebook</h6></a>
            <br>
          </div>
          <div id="form-contact">
            <form>
              <div class="form-group pb-3 pt-3">
                <label for="exampleFormControlInput1">Name</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Your name here">
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlInput1">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlSelect1">Query Type</label>
                <select class="form-control" id="exampleFormControlSelect1">
                <optgroup label="Select Query Type">
                  <option selected disabled hidden>Select Query Type</option>
                  <option>General Query</option>
                  <option>Complaint</option>
                  <option>Report Fradulant Activity</option>
                </optgroup>
                </select>
              </div>
              <div class="form-group pb-3">
                <label for="exampleFormControlTextarea1">Message</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="5" placeholder="Please provide necessary details as without them you will get a request termination and will need to re-request using right information in order to get any action"></textarea>
              </div>
              <div class="form-group d-flex gap-2">
                <div class="d-grid gap-2 col-6 mx-auto pt-2">
                  <button type="submit" class="btn btn-primary btn-block ">Submit & Connect</button>
                </div>
                <div class="d-grid gap-2 col-6 mx-auto pt-2">
                  <button class="btn btn-warning btn-block ">Check Status</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </main>
</body>
</template>
