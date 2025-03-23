<script setup>
import { ref, onMounted, computed } from "vue";
import { useStore } from 'vuex';
import axios from 'axios';

const store = useStore();

import "@/assets/styles/main.css"
import "@/assets/styles/statistics.css"

onMounted(() => {
    window.dispatchEvent(new CustomEvent('vue-component-itemwrap'));
    window.dispatchEvent(new CustomEvent('vue-component-search'));

    // Fetch pending professional applications if the user is an admin
    if (store.state.user?.role === 'admin') {
        fetchPendingApplications();
    }
});

const currentPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const handleChangePassword = async (event) => {
  event.preventDefault();
  
  try {
    const response = await fetch('/api/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Send cookies
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

const isUploading = ref(false);
const profilePictureUrl = computed(() => store.getters.userImage);

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
            const response = await axios.post('/api/upload-profile-picture', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                withCredentials: true
            });

            // Update user in store
            await store.dispatch('fetchUser');
            alert('Profile picture updated successfully!');
        } catch (error) {
            console.error('Upload error:', error);
            alert('Error updating profile picture. Please try again.');
        } finally {
            isUploading.value = false;
            event.target.value = ''; // Reset input
        }
    };
};

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

// Fetch active services on component mount
onMounted(async () => {
  try {
    const response = await fetch('/api/services/active');
    if (!response.ok) {
      throw new Error('Failed to fetch services');
    }
    const data = await response.json();
    servicesList.value = data;
    console.log('Services fetched:', data); 
  } catch (error) {
    console.error('Error fetching services:', error);
    alert('Failed to load services. Please try again later.');
  }
});

// File handling function
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
  const maxSize = 20 * 1024 * 1024; // 20MB in bytes
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
  
  // Form validation - check all required fields
  if (!selectedServiceId.value || !experience.value || !phoneNumber.value || !pincode.value) {
    alert('Please fill all required fields');
    return;
  }
  
  // Validate experience is a number
  if (isNaN(parseInt(experience.value))) {
    alert('Experience must be a valid number');
    return;
  }
  
  // Validate phone number has proper format
  if (phoneNumber.value.length < 10 || phoneNumber.value.length > 13) {
    alert('Please enter a valid phone number (10-13 digits)');
  }

  try {
    // Use FormData instead of JSON for file uploads
    const formData = new FormData();
    formData.append('service_id', selectedServiceId.value);
    formData.append('experience', experience.value);
    formData.append('phone_number', phoneNumber.value);
    formData.append('address_line1', addressLine1.value);
    formData.append('address_line2', addressLine2.value);
    formData.append('city', city.value);
    formData.append('state', state.value);
    formData.append('pincode', pincode.value);
    
    // Append file if selected
    if (documentFile.value) {
      formData.append('document', documentFile.value);
    }
    
    console.log('Sending professional registration data with document');
    
    const response = await fetch('/api/register-professional', {
      method: 'POST',
      credentials: 'include',
      body: formData
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert('Registration submitted! Awaiting verification.');
      await store.dispatch('fetchUser'); // Refresh user data
      document.getElementById('user-prof').style.display = 'none';
      
      // Reset form fields
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
      
      // Reset file input field
      document.getElementById('document').value = '';
    } else {
      alert(`Registration failed: ${data.message || 'Unknown error'}`);
      console.error('Server response:', data);
      document.getElementById('document').value = '';
    }
  } catch (error) {
    console.error('Error during professional registration:', error);
    alert('Registration error. Please try again.');
  }
};

// Admin-specific functionality
const blockEmail = ref('');
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

// Professional status
const professionalStatus = computed(() => {
  const status = store.state.user?.verification_status || 'not_applied';
  return status.charAt(0).toUpperCase() + status.slice(1);
});

// Professional Applications Management
const professionalApplications = ref([]);

// Fetch pending professional applications
const fetchPendingApplications = async () => {
  try {
    const response = await fetch('/api/pending-professionals');
    if (!response.ok) throw new Error('Failed to fetch applications');
    professionalApplications.value = await response.json();
  } catch (error) {
    console.error('Error fetching applications:', error);
    alert('Failed to load applications');
  }
};

// Handle document viewing
const handleViewDocument = (documentUrl) => {
  window.open(`http://localhost:5000/documents/${documentUrl}`, '_blank');
};

// Handle application approval
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

// Handle application rejection
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
          <div v-if="store.state.user?.role === 'admin'" style="padding-top: 9vw;">
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
              <div class="wishlist-items-wrapper d-flex gap-3">
                <div v-for="app in professionalApplications" :key="app.id" class="application-card">
                  <div class="application-details">
                    <p><strong>Username:</strong> {{ app.username }}</p>
                    <p><strong>Experience:</strong> {{ app.experience }} years</p>
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

          <!-- User View -->
          <div v-else>
            <p id="header-wishlist">Active Orders</p>
            <div id="wishlist-container">
              <button id="prev-btn" class="nav-arrow" style="display: none;">
                <i class="fa-solid fa-chevron-left"></i>
              </button>
              <div class="wishlist-items-wrapper d-flex gap-3">
                <div id="wishlist-item">
                  <div id="wishlist-item-image"></div>
                  <p id="item-name">Saksham Sirohi Ji</p>
                  <div class="d-flex gap-4 px-3">
                    <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                    <button type="button" class="btn btn-danger"><i class="fa-duotone fa-solid fa-trash-can fa-lg"></i></button>
                  </div>
                </div>
              </div>
              <button id="next-btn" class="nav-arrow">
                <i class="fa-solid fa-chevron-right"></i>
              </button>
            </div>
            <p id="header-previous" style="padding-top: 0vw;">Previously Ordered</p>
            <div id="previous-container">
              <button id="prev-btn" class="nav-arrow" style="display: none;">
                <i class="fa-solid fa-chevron-left"></i>
              </button>
              <div class="previous-items-wrapper d-flex gap-3">
                <div id="previous-item">
                  <div id="previous-item-image"></div>
                  <p id="item-name">Saksham Sirohi Ji</p>
                  <div class="d-flex gap-4 px-3">
                    <button type="button" class="btn btn-warning"><i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i></button>
                    <button type="button" class="btn btn-secondary"><i class="fa-duotone fa-solid fa-pencil fa-lg"></i></button>
                  </div>
                </div>
              </div>
              <button id="next-btn" class="nav-arrow">
                <i class="fa-solid fa-chevron-right"></i>
              </button>
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
          <button v-else-if="store.state.user?.role === 'professional'" type="button" class="btn btn-sm btn-success" onclick="showForm('user-prof')">Professional Dashboard</button>
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.application-details {
  flex-grow: 1;
  margin-right: 2rem;
}

.application-details p {
  margin: 0.5rem 0;
}
</style>