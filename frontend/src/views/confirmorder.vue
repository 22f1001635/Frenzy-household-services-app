<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"

const route = useRoute();
const router = useRouter();
const countdown = ref(3);

onMounted(() => {
  window.dispatchEvent(new CustomEvent('vue-component-countdown'));
  
  // Auto-redirect after 3 seconds
  const timer = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(timer);
      router.push('/dashboard');
    }
  }, 1000);
});
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%; padding-bottom: 7%;">
        <div id="box" class="bg-light text-dark" style="padding: 1vw;">
            <div class="mainform4">
              <div class="cart">
                <div v-if="route.query.status === 'success'" class="order-confirm">
                  <i class="fa-regular fa-circle-check fa-beat" style="color: #00ff00; font-size: 6vw;"></i>
                  <h3 v-if="route.query.type === 'cart'">Payment Successfully Completed for Your Order</h3>
                  <h3 v-else>Payment Successfully Completed for Your Service</h3>
                  <h4>Service Professional will be assigned for your visit shortly</h4>
                  <h6> You will be redirected to dashboard in <span id="secs">{{ countdown }}</span> seconds.</h6>
                </div>
                <div v-else class="order-confirm">
                  <i class="fa-regular fa-circle-xmark fa-beat-fade" style="color: #ff8080; font-size: 6vw;"></i>
                  <h3>Payment has failed</h3>
                  <h5>Any amount if deducted from your account will be refunded shortly, for any problems <a href="">contact us</a></h5>
                  <h6> You will be redirected to dashboard in <span id="secs">{{ countdown }}</span> seconds.</h6>
                </div>
              </div>
            </div>
        </div>
    </div>
    </main>
</body>
</template>