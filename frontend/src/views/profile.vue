<script setup>
import { ref,onMounted,computed } from "vue";
import { useStore } from 'vuex';
import axios from 'axios';

const store = useStore();

import "@/assets/styles/main.css"
import "@/assets/styles/statistics.css"
onMounted(() => {
    window.dispatchEvent(new CustomEvent('vue-component-itemwrap'));
    window.dispatchEvent(new CustomEvent('vue-component-search'));
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
                    <button type="button" class="btn btn-secondary"  @click="$router.go(-1)">Cancel</button>
                  </div>
                </form>
              </div>
                <div id="user-prof" class="mt-3 pform" style="display: none;">
                    <p>Service Professional Registration</p>
                    <form>
                        <div class="mb-2">
                            <label for="service-name" class="form-label">Service Name</label>
                            <select class="form-select" id="service-name" required>
                                <option value="">Select available services</option>
                                <option value="service1">Service 1</option>
                                <option value="service2">Service 2</option>
                                <option value="service3">Service 3</option>
                            </select>
                        </div>
                        <div class="mb-2">
                            <label for="experience" class="form-label">Experience (in yrs)</label>
                            <input type="number" class="form-control" id="experience" max="40" required>
                        </div>
                        <div class="mb-2">
                            <label for="file" class="form-label">Upload Documents File</label>
                            <input type="file" class="form-control" id="file" accept=".pdf">
                        </div>
                        <div class="mb-2">
                            <label for="mobile" class="form-label">Moblie Number</label>
                            <input type="number" class="form-control" id="mobile" required>
                        </div>
                        <div class="form-group">
                          <label for="address">Address</label>
                          <div class="row">
                              <div class="col-md-12">
                                  <input type="text" class="form-control" id="house-no" placeholder="House No., Apartment, Housing">
                              </div>
                          </div>
                          <div class="row mt-2">
                              <div class="col-md-6">
                                  <input type="text" class="form-control" id="area-street-village" placeholder="Area/Street/Village">
                              </div>
                              <div class="col-md-6">
                                  <input type="text" class="form-control" id="landmark" placeholder="Landmark">
                              </div>
                          </div>
                          <div class="row mt-2">
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="city" placeholder="City">
                              </div>
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="state" placeholder="State">
                              </div>
                              <div class="col-md-4">
                                  <input type="text" class="form-control" id="pincode" placeholder="Pincode">
                              </div>
                          </div>
                      </div>
                      <div class="d-flex gap-4">
                        <button type="submit" class="btn btn-primary" onclick="showForm('textarea')">Submit</button>
                        <button type="submit" class="btn btn-secondary" onclick="showForm('textarea')">Cancel</button>
                      </div>
                    </form>
                </div>
                <div id="user-content">
                  <p id="header-wishlist">From Your Wishlist</p>
                  <div id="wishlist-container">
                    <button id="prev-btn" class="nav-arrow" style="display: none;">
                      <i class="fa-solid fa-chevron-left"></i>
                    </button>
                    <div class="wishlist-items-wrapper d-flex gap-3">
                      <div id="wishlist-item">
                        <div id="wishlist-item-image">

                        </div>
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
                        <div id="previous-item-image">

                        </div>
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
        <div id="graph5">
          <div id="prof">
            <div id="pic"> <img :src="profilePictureUrl" @click="handleImageClick" draggable="false" style="cursor: pointer;">
            <input type="file" id="profile-upload" hidden accept="image/jpeg, image/png, image/jpg" @change="handleFileUpload">
            <div v-if="isUploading" class="upload-overlay">Uploading...</div>
            <button class="btn btn-warning" style="border-radius: 50%;" onclick="showForm('change-password')"><i class="fa-solid fa-key"></i></button></div>
            <div id="ori"><div id="name">{{ store.state.user?.username }}</div></div>
            <p>Email</p>
            <p id="ori">{{ store.state.user?.email }}</p><hr>
            <p>Address</p>
            <p id="ori">{{ store.state.user?.address || 'No address provided' }}</p><hr>
            <p>Phone Number</p>
            <p id="ori">{{ store.state.user?.phone_number || 'N/A' }}</p><hr>
            <p>User Type</p>
            <p id="ori">{{ store.state.user?.role }}</p><hr>
            <div class="px-4"><button type="button" class="btn btn-warning" onclick="showForm('user-prof')"><p id="ori">Are you a service professional?</p></button></div>
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
</style>