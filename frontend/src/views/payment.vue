<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"

const router = useRouter()
const route = useRoute()
const debugInfo = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const formatTimeTo24Hour = (timeStr) => {
  const [time, modifier] = timeStr.split(' ')
  let [hours, minutes] = time.split(':')
  
  if (modifier === 'PM' && hours !== '12') {
    hours = parseInt(hours, 10) + 12
  } else if (modifier === 'AM' && hours === '12') {
    hours = '00'
  }
  
  return `${hours}:${minutes}:00`
}

const completeOrder = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const formattedTime = formatTimeTo24Hour(route.query.serviceTime)
    const scheduledDateTime = `${route.query.serviceDate}T${formattedTime}`
    
    debugInfo.value = `Creating service request with:\n`
    debugInfo.value += `- Address ID: ${route.query.addressId}\n`
    debugInfo.value += `- Scheduled: ${scheduledDateTime}\n`
    
    if (route.query.source === 'cart') {
      debugInfo.value += '- Order type: Cart checkout\n'
    } else {
      debugInfo.value += `- Service ID: ${route.query.serviceId}\n`
      debugInfo.value += `- Quantity: ${route.query.quantity}\n`
    }

    // Create service request
    const response = await axios.post('/api/service-requests', {
      addressId: route.query.addressId,
      scheduledDate: scheduledDateTime,
      orderType: route.query.source === 'cart' ? 'cart' : 'buy_now'
    })

    debugInfo.value += `\nService request created successfully!\n`
    debugInfo.value += `Request IDs: ${response.data.requests.join(', ')}`
    
    // Redirect to confirmation page
    router.push({
      path: '/confirmorder',
      query: {
        status: 'success',
        type: route.query.source === 'cart' ? 'cart' : 'service'
      }
    })
  } catch (error) {
    console.error('Order creation failed:', error)
    errorMessage.value = error.response?.data?.message || 'Failed to create service request'
    debugInfo.value += `\nError: ${errorMessage.value}`
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%;">
      <div id="back">
        <a href="javascript:window.history.back()">
          <i class="fa-solid fa-circle-left" style="font-size:250%;"></i>
        </a>
        <p class="text-dark" id="head">Order Confirmation</p>
      </div>
      <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
        <div class="cards">
          <div class="saved">
            <p id="meth">Order Summary</p>
            <div class="card-items">
              <p>No payment required - demo mode</p>
              <p>Click below to confirm your order</p>
              <hr>
              <button 
                class="btn btn-success" 
                @click="completeOrder"
                :disabled="isLoading"
              >
                <span v-if="isLoading">
                  <i class="fas fa-spinner fa-spin"></i> Processing...
                </span>
                <span v-else>
                  <i class="fas fa-check"></i> Confirm Order
                </span>
              </button>
            </div>
          </div>
          
          <div class="mt-4 p-3 bg-light border rounded" v-if="debugInfo">
            <h5>Debug Information</h5>
            <pre style="white-space: pre-wrap; word-wrap: break-word;">{{ debugInfo }}</pre>
          </div>
          
          <div v-if="errorMessage" class="alert alert-danger mt-3">
            <i class="fas fa-exclamation-triangle"></i> {{ errorMessage }}
            <div v-if="errorMessage.includes('isoformat')" class="mt-2">
              <small>Note: Please ensure the time format is correct (HH:MM AM/PM)</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</body>
</template>

<style scoped>
pre {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  font-size: 0.9rem;
}

.alert {
  padding: 10px 15px;
  border-radius: 5px;
  margin-top: 15px;
}

.btn-success {
  padding: 10px 20px;
  font-size: 1.1rem;
}
</style>