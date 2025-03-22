<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();
const savedAddresses = ref([]);
const showNewAddress = ref(false);
const selectedAddressId = ref(null);
const formData = ref({
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    pincode: '',
    phone_number: '', // Added phone_number
    is_default: false
});

// Fetch addresses on component mount
onMounted(async () => {
    await store.dispatch('fetchUser');
    const user = store.state.user;
    
    if (!user) {
        router.push('/signin');
        return;
    }
    
    // Redirect professionals to their profile
    if (user.role === 'professional') {
        router.push('/profile');
        return;
    }

    // Fetch saved addresses for the user
    try {
        const response = await axios.get('/api/addresses', { withCredentials: true });
        savedAddresses.value = response.data;
    } catch (error) {
        console.error('Error fetching addresses:', error);
        alert('Failed to load addresses. Please try again.');
    }
});

// Toggle between saved addresses and new address form
const toggleSection = () => {
    showNewAddress.value = !showNewAddress.value;
};

// Submit a new address
const submitAddress = async () => {
    try {
        const response = await axios.post('/api/addresses', formData.value, { withCredentials: true });
        if (response.status === 201) {
            savedAddresses.value.push(response.data);
            toggleSection();
            formData.value = { address_line1: '', address_line2: '', city: '', state: '', pincode: '', phone_number: '', is_default: false };
            alert('Address saved successfully!');
        }
    } catch (error) {
        console.error('Error saving address:', error);
        alert('Error saving address. Please try again.');
    }
};

// Handle address selection for payment
const handleAddressSelection = (addressId) => {
    selectedAddressId.value = addressId;
};

// Proceed to payment with the selected address
const proceedToPayment = () => {
    if (!selectedAddressId.value) {
        alert('Please select an address');
        return;
    }
    router.push(`/payment?addressId=${selectedAddressId.value}`);
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
            <div id="datepicker"><input type="date" name="service-date"></div>
          </div>
          <div class="time-slot">
            <h5>Select Service Slot</h5>
            <label>
              <input type="radio" name="slot">
              9:00 AM
            </label>
            <label>
              <input type="radio" name="slot">
              11:00 AM
            </label>
            <label>
              <input type="radio" name="slot">
              1:00 PM
            </label>
            <label>
              <input type="radio" name="slot">
              3:00 PM
            </label>
            <label>
              <input type="radio" name="slot">
              5:00 PM
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
