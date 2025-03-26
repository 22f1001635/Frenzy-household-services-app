<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute();
const savedAddresses = ref([]);
const showNewAddress = ref(false);
const selectedAddressId = ref(null);
const selectedDate = ref('');
const selectedTime = ref('');
const timeSlots = ref(['9:00 AM', '11:00 AM', '1:00 PM', '3:00 PM', '5:00 PM']);
const isCartFlow = computed(() => route.query.source === 'cart');

const formData = ref({
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    pincode: '',
    phone_number: '',
    is_default: false
});

// Compute min date (today) and max date (30 days from now)
const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

const maxDate = computed(() => {
  const futureDate = new Date();
  futureDate.setDate(futureDate.getDate() + 30);
  return futureDate.toISOString().split('T')[0];
});

// Check if selected date is valid (at least 2 hours from now)
const isValidDate = computed(() => {
  if (!selectedDate.value || !selectedTime.value) return false;
  
  const now = new Date();
  const selectedDateTime = new Date(`${selectedDate.value}T${convertTo24Hour(selectedTime.value)}`);
  
  // Minimum 2 hours in the future
  const minDateTime = new Date(now.getTime() + 2 * 60 * 60 * 1000);
  
  return selectedDateTime >= minDateTime;
});

// Helper to convert time to 24-hour format
const convertTo24Hour = (timeStr) => {
  const [time, modifier] = timeStr.split(' ');
  let [hours, minutes] = time.split(':');
  
  if (modifier === 'PM' && hours !== '12') {
    hours = parseInt(hours, 10) + 12;
  }
  
  return `${hours}:${minutes}:00`;
};

// Fetch addresses on component mount
onMounted(async () => {
    await store.dispatch('fetchUser');
    const user = store.state.user;
    
    if (!user) {
        router.push('/signin');
        return;
    }
    
    if (user.role === 'professional') {
        router.push('/profile');
        return;
    }

    try {
        const response = await axios.get('/api/addresses', { withCredentials: true });
        savedAddresses.value = response.data;
    } catch (error) {
        console.error('Error fetching addresses:', error);
        alert('Failed to load addresses. Please try again.');
    }
});

const toggleSection = () => {
    showNewAddress.value = !showNewAddress.value;
};

const submitAddress = async () => {
    try {
        const response = await axios.post('/api/addresses', formData.value, { withCredentials: true });
        if (response.status === 201) {
            savedAddresses.value.push(response.data.address);
            toggleSection();
            formData.value = { address_line1: '', address_line2: '', city: '', state: '', pincode: '', phone_number: '', is_default: false };
            alert('Address saved successfully!');
        }
    } catch (error) {
        console.error('Error saving address:', error);
        alert('Error saving address. Please try again.');
    }
};

const handleAddressSelection = (addressId) => {
    selectedAddressId.value = addressId;
};

const proceedToPayment = () => {
    if (!selectedAddressId.value) {
        alert('Please select an address');
        return;
    }
    
    if (!selectedDate.value || !selectedTime.value) {
        alert('Please select a date and time slot');
        return;
    }
    
    if (!isValidDate.value) {
        alert('Please select a time slot at least 2 hours from now');
        return;
    }
    
    // Prepare query parameters
    const queryParams = {
      serviceId: route.query.serviceId,
      quantity: route.query.quantity,
      source: route.query.source,
      addressId: selectedAddressId.value,
      serviceDate: selectedDate.value,
      serviceTime: selectedTime.value
    };
    
    // Explicitly include serviceId and quantity for buy now flow
    if (isCartFlow.value === false) { // If source is 'buy_now'
        console.log('Adding serviceId:', route.query.serviceId);
        queryParams.serviceId = route.query.serviceId;
        queryParams.quantity = route.query.quantity;
    }
    
    router.push({
        path: '/payment',
        query: queryParams
    });
};
</script>

<template>
<body style="font-family: 'Poppins';">
<main style="padding-top:2.75%;">
  <div id="forms" style="padding-top: 4%;">
    <div id="back">
      <a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left"></i></a>
      <p class="text-dark" id="head">Select Address</p>
    </div>
    <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
      <div class="mainform3">
        <div class="address">
          <!-- Saved Addresses Section -->
          <div id="savedAddressSection" v-if="!showNewAddress">
            <div class="saved" style="padding-top: 0.5vw;">
              <h6 class="opacity-50">Saved Addresses</h6>
              <div class="address-items">
                <template v-if="savedAddresses.length > 0">
                  <div v-for="addr in savedAddresses" :key="addr.id" class="opacity-100">
                    <label class="d-block">
                      <input 
                        type="radio" 
                        name="saved-address" 
                        :value="addr.id" 
                        @change="handleAddressSelection(addr.id)"
                      >
                      {{ addr.address_line1 }}, {{ addr.city }}, {{ addr.state }} {{ addr.pincode }} ({{ addr.phone_number }})
                    </label>
                    <hr>
                  </div>
                </template>
                <p v-else class="opacity-75">
                  No saved addresses. Please add a new address.
                </p>
              </div>
            </div>
            <a href="#" @click="toggleSection">+ Add a new address</a>
          </div>

          <!-- New Address Section -->
          <div id="newAddressSection" v-else>
            <div class="new" style="padding-top: 0.5vw;">
              <p>Add a new address</p>
              <form @submit.prevent="submitAddress">
                <div class="container">
                  <div class="row">
                    <div class="col-md-6 mb-2">
                      <input v-model="formData.address_line1" 
                             type="text" 
                             class="form-control" 
                             placeholder="House/Apartment" 
                             required>
                    </div>
                    <div class="col-md-6 mb-2">
                      <input v-model="formData.address_line2" 
                             type="text" 
                             class="form-control" 
                             placeholder="Area/Street">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-3 mb-2">
                      <input v-model="formData.city" 
                             type="text" 
                             class="form-control" 
                             placeholder="City" 
                             required>
                    </div>
                    <div class="col-md-3 mb-2">
                      <input v-model="formData.state" 
                             type="text" 
                             class="form-control" 
                             placeholder="State" 
                             required>
                    </div>
                    <div class="col-md-2 mb-2">
                      <input v-model="formData.pincode" 
                             type="text" 
                             class="form-control" 
                             placeholder="Pincode" 
                             required>
                    </div>
                    <div class="col-md-3 mb-2">
                      <input v-model="formData.phone_number" 
                             type="tel" 
                             class="form-control" 
                             placeholder="Phone Number" 
                             required>
                    </div>
                  </div>
                  <div class="d-flex align-items-center mt-0">
                    <div class="form-check">
                      <input v-model="formData.is_default" 
                            type="checkbox" 
                            class="form-check-input">
                      <label class="form-check-label">Set as Default</label>
                    </div>
                    <div class="ms-auto">
                      <button type="submit" class="btn btn-success">Save Address</button>
                      <button type="button" class="btn btn-secondary ms-2" @click="toggleSection">Cancel</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <a href="#" @click="toggleSection">Select Saved Address</a>
          </div>

          <hr>

          <!-- Date and Time Picker -->
          <div class="date-slot">
            <label for="service-date" class="opacity-100"><h5>Service Date</h5></label><br>
            <div id="datepicker">
              <input 
                type="date" 
                name="service-date" 
                v-model="selectedDate"
                :min="minDate"
                :max="maxDate"
                required
              >
            </div>
          </div>
          <div class="time-slot" v-if="selectedDate">
            <h5>Select Service Slot</h5>
            <label v-for="slot in timeSlots" :key="slot">
              <input 
                type="radio" 
                name="slot" 
                :value="slot"
                v-model="selectedTime"
                required
              >
              {{ slot }}
            </label>
          </div>
          <button type="button" class="btn btn-dark" @click="proceedToPayment">
            <i class="fa-duotone fa-solid fa-arrow-right"></i> Proceed to Pay
          </button>
        </div>
      </div>
    </div>
  </div>
</main>
</body>
</template>

<style scoped>
.alert-warning {
  margin: 15px 0;
  padding: 10px;
  border-radius: 5px;
}

.time-slot label {
  display: inline-block;
  margin-right: 15px;
  margin-bottom: 5px;
}
</style>