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
  // Handle cases where time might be undefined or empty
  if (!timeStr) {
    console.error('Time string is undefined or empty')
    return '00:00:00'
  }

  try {
    const [time, modifier] = timeStr.split(' ')
    let [hours, minutes] = time.split(':')
    
    // Convert to string with leading zero if needed
    hours = String(hours)
    
    if (modifier === 'PM' && hours !== '12') {
      hours = String(parseInt(hours, 10) + 12)
    } else if (modifier === 'AM' && hours === '12') {
      hours = '00'
    }
    
    // Pad hours and ensure minutes are present
    return `${hours.padStart(2, '0')}:${minutes || '00'}:00`
  } catch (error) {
    console.error('Error formatting time:', error)
    return '00:00:00'
  }
}

const completeOrder = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    // Safely handle potentially undefined route query values
    const serviceDate = route.query.serviceDate || ''
    const serviceTime = route.query.serviceTime || ''
    const addressId = route.query.addressId
    const source = route.query.source
    const serviceId = route.query.serviceId
    const quantity = route.query.quantity || 1

    // Validate required fields
    if (!addressId) {
      throw new Error('Address ID is required')
    }

    // Format scheduled date and time
    const formattedTime = formatTimeTo24Hour(serviceTime)
    const scheduledDateTime = `${serviceDate}T${formattedTime}`
    
    // Prepare debug information
    debugInfo.value = `Creating service request with:\n`
    debugInfo.value += `- Address ID: ${addressId}\n`
    debugInfo.value += `- Scheduled: ${scheduledDateTime}\n`
    
    // Prepare request payload
    const requestPayload = {
      addressId: addressId,
      scheduledDate: scheduledDateTime,
      orderType: source === 'cart' ? 'cart' : 'buy_now'
    }

    // Add serviceId and quantity for buy now flow
    if (source !== 'cart') {
      // Explicitly check for serviceId
      if (!serviceId) {
        throw new Error('Service ID is required for buy now flow')
      }
      requestPayload.serviceId = serviceId
      requestPayload.quantity = Number(quantity)
    }

    // Create service request
    const response = await axios.post('/api/service-requests', requestPayload)

    debugInfo.value += `\nService request(s) created successfully!\n`
    debugInfo.value += `Request IDs: ${response.data.requests.join(', ')}`
    
    // Redirect to confirmation page
    router.push({
      path: '/confirmorder',
      query: {
        status: 'success',
        type: source === 'cart' ? 'cart' : 'service'
      }
    })
  } catch (error) {
    console.error('Order creation failed:', error)
    
    // More detailed error handling
    if (error.response) {
      // The request was made and the server responded with a status code
      errorMessage.value = error.response.data.error || 'Failed to create service request'
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage.value = 'No response received from server'
    } else {
      // Something happened in setting up the request
      errorMessage.value = error.message || 'Failed to create service request'
    }
    
    debugInfo.value += `\nError: ${errorMessage.value}`
  } finally {
    isLoading.value = false
  }
}
onMounted(() => {
  console.log('Received query params:', route.query);

  // Determine required parameters based on source
  const requiredParams = route.query.source === 'cart' 
    ? ['addressId', 'serviceDate', 'serviceTime', 'source']
    : ['addressId', 'serviceDate', 'serviceTime', 'source', 'serviceId', 'quantity'];
  
  const missingParams = requiredParams.filter(param => !route.query[param]);
  
  if (missingParams.length > 0) {
    errorMessage.value = `Missing required parameters: ${missingParams.join(', ')}`;
  }
});
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
                :disabled="isLoading || !!errorMessage"
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