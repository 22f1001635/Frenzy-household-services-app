<script setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from 'vuex';
import axios from 'axios';
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

// Profile Picture Upload
const isUploading = ref(false);
const profilePictureUrl = computed(() => store.getters.userImage);

// Password Change
const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

// Professional Registration
const servicesList = ref([]);
const selectedServiceId = ref('');
const experience = ref('');
const phoneNumber = ref('');
const addressLine1 = ref('');
const addressLine2 = ref('');
const city = ref('');
const state = ref('');
const pincode = ref('');
const documentFile = ref(null);
const documentError = ref('');

// Admin Functionality
const blockEmail = ref('');
const professionalApplications = ref([]);
const worstPerformers = ref([]);

// Request Management
const currentRequests = ref([]);
const completedRequests = ref([]);
const wishlistItems = ref([]);

// Request Editing
const editingRequestId = ref(null);
const newDate = ref('');
const newQuantity = ref(1);
const timeSlots = ref(['9:00 AM', '11:00 AM', '1:00 PM', '3:00 PM', '5:00 PM']);
const selectedTime = ref('');

// Professional Status
const professionalStatus = computed(() => {
  const status = store.state.user?.verification_status || 'not_applied';
  return status.charAt(0).toUpperCase() + status.slice(1);
});

onMounted(async () => {
  window.dispatchEvent(new CustomEvent('vue-component-itemwrap'));
  window.dispatchEvent(new CustomEvent('vue-component-search'));

  // Fetch role-specific data
  if (store.state.user?.role === 'admin') {
    await fetchPendingApplications();
    await fetchWorstPerformers();
  } else if (store.state.user?.role === 'professional') {
    await fetchProfessionalRequests();
  } else if (store.state.user?.role === 'user') {
    await fetchUserRequests();
    await fetchWishlist();
  }

  // Fetch active services for professional registration
  try {
    const response = await fetch('/api/services/active');
    if (response.ok) {
      servicesList.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching services:', error);
  }
});

// ========== Profile Picture Handling ==========
const handleImageClick = () => {
  const requirements = `Profile Picture Requirements:
- JPG/JPEG/PNG format
- Max file size: 5MB
- Square aspect ratio (1:1)`;
  alert(requirements);
  document.getElementById('profile-upload').click();
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Validate file type
  const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
  if (!validTypes.includes(file.type)) {
    alert('Invalid file type. Please upload JPG, JPEG or PNG.');
    return;
  }

  // Validate file size
  if (file.size > 5 * 1024 * 1024) {
    alert('File size exceeds 5MB limit.');
    return;
  }

  // Validate aspect ratio
  const img = new Image();
  img.src = URL.createObjectURL(file);
  img.onload = async () => {
    if (img.width !== img.height) {
      alert('Image must have 1:1 aspect ratio.');
      return;
    }

    // Proceed with upload
    isUploading.value = true;
    const formData = new FormData();
    formData.append('profile_picture', file);

    try {
      await axios.post('/api/upload-profile-picture', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true
      });
      await store.dispatch('fetchUser');
      alert('Profile picture updated successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error updating profile picture. Please try again.');
    } finally {
      isUploading.value = false;
      event.target.value = '';
    }
  };
};

// ========== Password Change ==========
const handleChangePassword = async (event) => {
  event.preventDefault();
  
  try {
    const response = await fetch('/api/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        current_password: currentPassword.value,
        new_password: newPassword.value,
        confirm_password: confirmPassword.value
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert('Password changed successfully');
      document.getElementById('change-password').style.display = 'none';
    } else {
      alert(data.message || 'Error changing password');
    }
    currentPassword.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
  } catch (error) {
    console.error('Error:', error);
    alert('Error changing password. Please try again.');
  }
};

// ========== Professional Registration ==========
const handleFileChange = (event) => {
  const file = event.target.files[0];
  documentError.value = '';
  
  if (!file) {
    documentFile.value = null;
    return;
  }
  
  // Validate file type
  if (!file.type.includes('pdf')) {
    documentError.value = 'Only PDF files are allowed';
    event.target.value = '';
    documentFile.value = null;
    return;
  }
  
  // Validate file size (20MB)
  const maxSize = 20 * 1024 * 1024;
  if (file.size > maxSize) {
    documentError.value = 'File size exceeds 20MB limit';
    event.target.value = '';
    documentFile.value = null;
    return;
  }
  
  documentFile.value = file;
};

const handleProfessionalRegistration = async (event) => {
  event.preventDefault();
  
  // Form validation
  if (!selectedServiceId.value || !experience.value || !phoneNumber.value || !pincode.value) {
    alert('Please fill all required fields');
    return;
  }
  
  if (isNaN(parseInt(experience.value))) {
    alert('Experience must be a valid number');
    return;
  }

  if (phoneNumber.value.length < 10 || phoneNumber.value.length > 13) {
    alert('Please enter a valid phone number (10-13 digits)');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('service_id', selectedServiceId.value);
    formData.append('experience', experience.value);
    formData.append('phone_number', phoneNumber.value);
    formData.append('address_line1', addressLine1.value);
    formData.append('address_line2', addressLine2.value);
    formData.append('city', city.value);
    formData.append('state', state.value);
    formData.append('pincode', pincode.value);
    
    if (documentFile.value) {
      formData.append('document', documentFile.value);
    }
    
    const response = await fetch('/api/register-professional', {
      method: 'POST',
      credentials: 'include',
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert('Registration submitted! Awaiting verification.');
      await store.dispatch('fetchUser');
      document.getElementById('user-prof').style.display = 'none';
      
      // Reset form
      selectedServiceId.value = '';
      experience.value = '';
      phoneNumber.value = '';
      addressLine1.value = '';
      addressLine2.value = '';
      city.value = '';
      state.value = '';
      pincode.value = '';
      documentFile.value = null;
      documentError.value = '';
      document.getElementById('document').value = '';
    } else {
      alert(`Registration failed: ${data.message || 'Unknown error'}`);
      document.getElementById('document').value = '';
    }
  } catch (error) {
    console.error('Registration error:', error);
    alert('Registration error. Please try again.');
  }
};

// ========== Admin Functions ==========
const fetchPendingApplications = async () => {
  try {
    const response = await fetch('/api/pending-professionals');
    if (response.ok) {
      professionalApplications.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching applications:', error);
    alert('Failed to load applications');
  }
};

const fetchWorstPerformers = async () => {
  try {
    const response = await fetch('/api/professionals/worst-performing');
    if (response.ok) {
      worstPerformers.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching performers:', error);
  }
};

const handleViewDocument = (documentUrl) => {
  window.open(`/documents/${documentUrl}`, '_blank');
};

const handleAccept = async (applicationId) => {
  try {
    const response = await fetch(`/api/update-professional-status/${applicationId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'verified' })
    });
    
    if (response.ok) {
      professionalApplications.value = professionalApplications.value.filter(app => app.id !== applicationId);
      alert('Application approved');
    }
  } catch (error) {
    console.error('Approval error:', error);
    alert('Error approving application');
  }
};

const handleReject = async (applicationId) => {
  try {
    const response = await fetch(`/api/update-professional-status/${applicationId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'rejected' })
    });
    
    if (response.ok) {
      professionalApplications.value = professionalApplications.value.filter(app => app.id !== applicationId);
      alert('Application rejected');
    }
  } catch (error) {
    console.error('Rejection error:', error);
    alert('Error rejecting application');
  }
};

const handleBlockUser = async (event) => {
  event.preventDefault();
  if (!blockEmail.value) return;

  try {
    const response = await fetch('/api/block-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: blockEmail.value })
    });

    const data = await response.json();
    if (response.ok) {
      alert(`User ${data.is_blocked ? 'blocked' : 'unblocked'} successfully`);
      blockEmail.value = '';
      document.getElementById('user-prof').style.display = 'none';
    } else {
      alert(data.message || 'Error updating user status');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Error processing request');
  }
};

// ========== Request Management ==========
const fetchProfessionalRequests = async () => {
  try {
    const [currentRes, completedRes] = await Promise.all([
      fetch('/api/professional/accepted-requests'),
      fetch('/api/professional/completed-requests')
    ]);
    currentRequests.value = await currentRes.json();
    completedRequests.value = await completedRes.json();
  } catch (error) {
    console.error('Error fetching professional requests:', error);
  }
};

const fetchUserRequests = async () => {
  try {
    const [currentRes, completedRes] = await Promise.all([
      fetch('/api/user/current-requests'),
      fetch('/api/user/completed-requests')
    ]);
    currentRequests.value = await currentRes.json();
    completedRequests.value = await completedRes.json();
  } catch (error) {
    console.error('Error fetching user requests:', error);
  }
};

const fetchWishlist = async () => {
  try {
    const response = await fetch('/api/service-actions/wishlist');
    if (response.ok) {
      wishlistItems.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching wishlist:', error);
  }
};

const handleUnassign = async (requestId) => {
  try {
    const response = await fetch(`/api/service-requests/${requestId}/unassign`, {
      method: 'PATCH'
    });
    if (response.ok) {
      currentRequests.value = currentRequests.value.filter(req => req.id !== requestId);
      alert('Request unassigned successfully');
    }
  } catch (error) {
    console.error('Unassign error:', error);
    alert('Error unassigning request');
  }
};

const handleCancelRequest = async (requestId) => {
  try {
    const response = await fetch(`/api/service-requests/${requestId}/cancel`, {
      method: 'PATCH'
    });
    if (response.ok) {
      currentRequests.value = currentRequests.value.filter(req => req.id !== requestId);
      alert('Request cancelled successfully');
    }
  } catch (error) {
    console.error('Cancel error:', error);
    alert('Error cancelling request');
  }
};

const handleCompleteRequest = async (requestId) => {
  const request = currentRequests.value.find(req => req.id === requestId);
  if (!request) {
    alert('Request not found.');
    return;
  }
  if (!request.professional_id) {
    alert('Cannot complete request without an assigned professional.');
    return;
  }
  try {
    const response = await fetch(`/api/service-requests/${requestId}/complete`, {
      method: 'PATCH'
    });
    if (response.ok) {
      router.push(`/review?request_id=${requestId}`);
    }
  } catch (error) {
    console.error('Completion error:', error);
    alert('Error completing request');
  }
};

// ========== Request Editing ==========
const openEditForm = (request) => {
  editingRequestId.value = request.id;
  const dateObj = new Date(request.scheduled_date);
  
  // Extract date and time
  newDate.value = dateObj.toISOString().slice(0, 10);
  selectedTime.value = dateObj.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit', 
    hour12: true 
  }).toUpperCase();
  
  newQuantity.value = request.quantity;
};

const cancelEdit = () => {
  editingRequestId.value = null;
};

const convertTo24Hour = (timeStr) => {
  const [time, modifier] = timeStr.split(' ');
  let [hours, minutes] = time.split(':');
  
  if (modifier === 'PM') {
    hours = hours === '12' ? '12' : String(parseInt(hours, 10) + 12);
  } else if (modifier === 'AM' && hours === '12') {
    hours = '00';
  }
  
  return `${hours.padStart(2, '0')}:${minutes}:00`;
};

const saveRequestChanges = async (requestId) => {
  try {
    // Combine date and time
    const combinedDateTime = `${newDate.value}T${convertTo24Hour(selectedTime.value)}`;
    
    const response = await fetch(`/api/service-requests/${requestId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        scheduled_date: combinedDateTime,
        quantity: newQuantity.value
      })
    });

    if (response.ok) {
      const updatedRequest = await response.json();
      const index = currentRequests.value.findIndex(req => req.id === requestId);
      if (index !== -1) {
        currentRequests.value.splice(index, 1, updatedRequest);
      }
      editingRequestId.value = null;
      alert('Request updated successfully');
    } else {
      const errorData = await response.json();
      alert(errorData.error || 'Failed to update request');
    }
  } catch (error) {
    console.error('Error updating request:', error);
    alert('Failed to update request');
  }
};

const removeFromWishlist = async (itemId) => {
  try {
    await axios.delete(`/api/service-actions/${itemId}`, {
      withCredentials: true
    });
    wishlistItems.value = wishlistItems.value.filter(item => item.id !== itemId);
  } catch (error) {
    console.error('Error removing item:', error);
    alert('Failed to remove item');
  }
};

const addToCart = async (serviceId) => {
  try {
    const response = await axios.post('/api/service-actions', {
      service_id: serviceId,
      action_type: 'cart',
      quantity: 1
    }, {
      withCredentials: true
    });
    alert('Item moved to cart!');
  } catch (error) {
    if (error.response?.data?.error_type === 'duplicate') {
      alert('This item is already in your cart');
    } else {
      console.error('Error moving to cart:', error);
      alert(error.response?.data?.message || 'Failed to move to cart');
    }
  }
};
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="graph4">
      <div class="outline">
        <div id="change-password" class="mt-5 pform" style="display: none;">
          <p>Change Password</p>
          <form @submit="handleChangePassword">
            <div class="mb-3 pt-4">
              <label for="current-password" class="form-label">Current Password</label>
              <input type="password" class="form-control" id="current-password" required v-model="currentPassword">
            </div>
            <div class="mb-3">
              <label for="new-password" class="form-label">New Password</label>
              <input type="password" class="form-control" id="new-password" required 
                    minlength="8" 
                    title="Password must be at least 8 characters long" v-model="newPassword">
            </div>
            <div class="mb-3">
              <label for="confirm-password" class="form-label">Confirm Password</label>
              <input type="password" class="form-control" id="confirm-password" required v-model="confirmPassword">
            </div>
            <div class="d-flex gap-4">
              <button type="submit" class="btn btn-success">Submit</button>
              <button type="button" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Role-based user-prof content -->
        <div id="user-prof" class="mt-3 pform" style="display: none;">
          <!-- Admin View -->
          <div v-if="store.state.user?.role === 'admin'" style="padding-top: 1vw;">
            <p style="padding-left: 2vw;">Revoke Account Access</p>
            <form @submit.prevent="handleBlockUser">
              <div class="mb-2">
                <label for="block-email" class="form-label">User Email</label>
                <input type="email" class="form-control" id="block-email" v-model="blockEmail" required>
              </div>
              <div class="d-flex" style="padding-right: 4vw;">
                <button type="submit" class="btn btn-danger">Block/Unblock</button>
                <button type="button" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
              </div>
            </form>

            <div class="mt-3">
              <p class="fw-bold">Worst Performing Professionals</p>
              <div v-if="worstPerformers.length > 0" class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Professional</th>
                      <th>Service</th>
                      <th>Rating</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="pro in worstPerformers" :key="pro.id">
                      <td>{{ pro.username }}</td>
                      <td>{{ pro.service_name }}</td>
                      <td :class="{ 'text-danger': pro.rating < 3 }">
                        {{ pro.rating.toFixed(1) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-muted">
                No performance data available
              </div>
            </div>
          </div>

          <!-- Professional View -->
          <div v-else-if="store.state.user?.role === 'professional'">
            <p>Professional Status: {{ professionalStatus }}</p>
            <div class="alert alert-success" v-if="store.state.user?.verification_status === 'verified'">
              Your account is verified and active
            </div>
            <div class="alert alert-warning" v-else>
              Verification pending. You can accept bookings once verified.
            </div>
          </div>

          <!-- User View (Registration Form) -->
          <div v-else>
            <p>Service Professional Registration</p>
            <form @submit="handleProfessionalRegistration">
              <div class="mb-2">
                <label for="service-name" class="form-label">Service Name</label>
                <select class="form-select" id="service-name" v-model="selectedServiceId" required>
                  <option value="" disabled>Select available services</option>
                  <option v-for="service in servicesList" :key="service.id" :value="service.id">
                    {{ service.name }}
                  </option>
                </select>
              </div>
              <div class="mb-2">
                <label for="experience" class="form-label">Experience (in yrs)</label>
                <input type="number" class="form-control" id="experience" v-model="experience" max="40" required>
              </div>
              <div class="mb-2">
                <label for="phone-number" class="form-label">Phone Number</label>
                <input type="tel" class="form-control" id="phone-number" v-model="phoneNumber" minlength="10" maxlength="13" required>
              </div>
              <div class="mb-2">
                <label for="document" class="form-label">Upload verification documents (PDF)</label>
                <input type="file" class="form-control" id="document" accept=".pdf" @change="handleFileChange">
                <div v-if="documentError" class="text-danger small mt-1">{{ documentError }}</div>
              </div>
              <div class="form-group">
                <label for="address">Address</label>
                <div class="row">
                  <div class="col-md-12">
                    <input type="text" class="form-control" id="address-line1" v-model="addressLine1" placeholder="House/Apartment" required>
                  </div>
                </div>
                <div class="row mt-2">
                  <div class="col-md-12">
                    <input type="text" class="form-control" id="address-line2" v-model="addressLine2" placeholder="Area/Street">
                  </div>
                </div>
                <div class="row mt-2">
                  <div class="col-md-4">
                    <input type="text" class="form-control" id="city" v-model="city" placeholder="City" required>
                  </div>
                  <div class="col-md-4">
                    <input type="text" class="form-control" id="state" v-model="state" placeholder="State" required>
                  </div>
                  <div class="col-md-4">
                    <input type="text" class="form-control" id="pincode" v-model="pincode" placeholder="Pincode" required>
                  </div>
                </div>
              </div>
              <div class="d-flex gap-4">
                <button type="submit" class="btn btn-primary">Submit</button>
                <button type="button" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
              </div>
            </form>
          </div>
        </div>

        <!-- User Content Section -->
        <div id="user-content">
          <!-- Admin View -->
          <div v-if="store.state.user?.role === 'admin'">
            <p id="header-wishlist">Professional Applications</p>
            <div id="wishlist-container">
              <div v-if="professionalApplications.length === 0" style="width: 75vw; margin-left: 30%;">
                <p style="color: black; opacity: 0.70;">No pending professional applications</p>
              </div>
              <div class="wishlist-items-wrapper d-flex gap-3">
                <div class="pro-wrap" style="width: 52.5vw;">
                <div v-for="app in professionalApplications" :key="app.id" class="application-card">
                  <div class="application-details">
                    <p><strong>Username:</strong> {{ app.username }}</p>
                    <p><strong>Experience:</strong> {{ app.experience }} years</p>
                    <p><strong>Pincode:</strong> {{ app.pincode }}</p>
                    <p><strong>Service:</strong> {{ app.service_name }}</p>
                  </div>
                  <div class="d-flex gap-2 px-3">
                    <button @click="handleViewDocument(app.document_url)" class="btn btn-info">
                      <i class="fa-solid fa-file"></i>
                    </button>
                    <button @click="handleAccept(app.id)" class="btn btn-success">
                      <i class="fa-solid fa-check"></i>
                    </button>
                    <button @click="handleReject(app.id)" class="btn btn-danger">
                      <i class="fa-solid fa-xmark"></i>
                    </button>
                  </div>
                </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="store.state.user?.role === 'professional'">
            <p id="header-wishlist">Current Requests</p>
            <div id="wishlist-container" class="d-flex flex-row overflow-auto gap-3">
              <div v-if="currentRequests.length === 0" class="text-center w-100">
                <p class="text-black text-opacity-70">No active service requests</p>
              </div>
              <div class="wishlist-items-wrapper d-flex">
                <div class="pro-wrap d-flex gap-3">
                  <div v-for="request in currentRequests" :key="request.id" class="application-card" style="width: 25vw;">
                    <div class="application-details">
                      <p><strong>Service:</strong> {{ request.service_name }}</p>
                      <p><strong>Scheduled:</strong> {{ new Date(request.scheduled_date).toLocaleDateString() }}</p>
                      <p><strong>Address:</strong> {{ request.user_address }}</p>
                    </div>
                    <div class="d-flex gap-2 px-3 py-1" style="margin-left: 7.5vw;">
                      <button @click="handleUnassign(request.id)" class="btn btn-sm btn-danger">
                        <i class="fa-solid fa-xmark"></i> Cancel
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <p id="header-previous" style="padding-top: 0vw;">Completed Requests</p>
            <div id="previous-container">
              <div class="previous-items-wrapper d-flex gap-3 py-4 pt-1">
                <div v-for="request in completedRequests" :key="request.id" class="application-card">
                  <div class="application-details">
                    <p><strong>Service:</strong> {{ request.service_name }}</p>
                    <p><strong>Rating:</strong> {{ request.rating || 'Not rated' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- User View -->
          <div v-if="store.state.user?.role === 'user'">
            <div v-if="currentRequests.length > 0">
              <p id="header-wishlist">Current Requests</p>
              <div id="wishlist-container" style="padding-bottom: 1vw;">
                <div class="wishlist-items-wrapper d-flex gap-3">
                  <div v-for="request in currentRequests" :key="request.id" class="application-card">
                    <div class="application-details">
                      <p><strong>Service:</strong> {{ request.service_name }}</p>
                      <template v-if="editingRequestId === request.id">
                        <div class="mb-2">
                          <label class="form-label">New Date:</label>
                          <input type="date" v-model="newDate" class="form-control">
                        </div>
                        <div class="row">
                        <div class="mb-2 col-md-6">
                          <label class="form-label">Time Slot:</label>
                          <select v-model="selectedTime" class="form-control">
                            <option v-for="slot in timeSlots" :key="slot" :value="slot">{{ slot }}</option>
                          </select>
                        </div>
                        <div class="mb-2 col-md-6">
                          <label class="form-label">Quantity:</label>
                          <input type="number" v-model="newQuantity" min="1" class="form-control">
                        </div>
                      </div>
                      </template>
                      <template v-else>
                        <p><strong>Scheduled:</strong> {{ new Date(request.scheduled_date).toLocaleString() }}</p>
                        <p><strong>Quantity:</strong> {{ request.quantity }}</p>
                      </template>
                    </div>
                    <div class="d-flex gap-2 px-3">
                      <template v-if="editingRequestId === request.id">
                        <button @click="saveRequestChanges(request.id)" class="btn btn-success btn-sm">
                          <i class="fa-solid fa-check"></i> Save
                        </button>
                        <button @click="cancelEdit" class="btn btn-secondary btn-sm">
                          <i class="fa-solid fa-times"></i> Cancel
                        </button>
                      </template>
                      <template v-else>
                        <button @click="openEditForm(request)" class="btn btn-info btn-sm">
                          <i class="fa-solid fa-pen"></i> Edit
                        </button>
                        <button @click="handleCancelRequest(request.id)" class="btn btn-danger btn-sm">
                          <i class="fa-solid fa-xmark"></i> Cancel
                        </button>
                        <button @click="handleCompleteRequest(request.id)" class="btn btn-success btn-sm">
                          <i class="fa-solid fa-check"></i> Complete
                        </button>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else>
              <p id="header-wishlist">From Your Wishlist</p>
              <div id="wishlist-container">
                <div class="wishlist-items-wrapper d-flex gap-3">
                  <div v-for="item in wishlistItems" :key="item.id" id="wishlist-item">
                    <div id="wishlist-item-image"><img :src="`http://localhost:5000/service_images/${item.service.image_file}`" style="width: 5.5vw; height: 5.5vw;"></div>
                    <p id="item-name">{{ item.service.name }}</p>
                    <div class="d-flex gap-4 px-3">
                      <button type="button" class="btn btn-warning" @click="addToCart(item.service.id)"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                      <button type="button" class="btn btn-danger" @click="removeFromWishlist(item.id)"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <p id="header-previous" style="padding-top: 0vw;">Previously Ordered</p>
            <div id="previous-container">
              <div class="previous-items-wrapper d-flex gap-3">
                <div v-for="request in completedRequests" :key="request.id" class="application-card">
                  <div class="application-details">
                    <p><strong>Service:</strong> {{ request.service_name }}</p>
                    <p><strong>Rating:</strong> {{ request.rating || 'Not reviewed' }}</p>
                  </div>
                  <div class="d-flex gap-2 px-3">
                    <button v-if="request.rating" @click="router.push(`/review?request_id=${request.id}`)" class="btn btn-secondary">
                      <i class="fa-solid fa-pen"></i> Edit Review
                    </button>
                    <button v-else @click="router.push(`/review?request_id=${request.id}`)" class="btn btn-primary">
                      <i class="fa-solid fa-star"></i> Add Review
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="graph5">
      <div id="prof">
        <div id="pic">
          <img :src="profilePictureUrl" @click="handleImageClick" draggable="false" style="cursor: pointer;">
          <input type="file" id="profile-upload" hidden accept="image/jpeg, image/png, image/jpg" @change="handleFileUpload">
          <div v-if="isUploading" class="upload-overlay">Uploading...</div>
          <button class="btn btn-warning" style="border-radius: 50%;" onclick="showForm('change-password')"><i class="fa-solid fa-key"></i></button></div>
        <div id="ori"><div id="name">{{ store.state.user?.username }}</div></div>
        <p>Email</p>
        <p id="ori">{{ store.state.user?.email }}</p><hr>
        <p>Address</p>
          <p id="ori" v-if="store.state.user?.address">
            {{ store.state.user.address.address_line1 }},
            {{ store.state.user.address.address_line2 }},
            {{ store.state.user.address.city }}, 
            {{ store.state.user.address.state }},
            {{ store.state.user.address.pincode }}
          </p>
          <p v-else id="ori">No address provided</p><hr>
          <p>Contact Number</p>
          <p id="ori">{{ store.state.user?.phone_number || 'N/A' }}</p><hr>
        <p>User Type</p>
        <p id="ori">{{ store.state.user?.role }}</p><hr>
        <div class="px-4 pt-2">
          <button v-if="store.state.user?.role === 'admin'" type="button" class="btn btn-sm btn-danger px-5" onclick="showForm('user-prof')">Block/Unblock Account</button>
          <button v-else-if="store.state.user?.role === 'user'" type="button" class="btn btn-sm btn-warning" onclick="showForm('user-prof')"><p id="ori">Are you a service professional?</p></button></div>
      </div>
    </div>
  </main>
</body>
</template>

<style scoped>
.upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.application-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1rem;
  margin: 1rem 0;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.application-details {
  color: black;
  opacity: 0.75;
  flex-grow: 1;
  margin-right: 2rem;
}

.application-details p {
  margin: 0.5rem 0;
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
  cursor: pointer;
}

.text-danger {
  color: #dc3545 !important;
  font-weight: 500;
}

#previous-container{
  height: unset;
}
</style>