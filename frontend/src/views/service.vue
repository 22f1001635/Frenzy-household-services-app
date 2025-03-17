<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const name = ref('')
const description = ref('')
const time_required = ref('')
const base_price = ref('')
const service_pincodes = ref('')
const category_id = ref('')
const serviceImage = ref(null)
const router = useRouter()
const error = ref('')
const categories = ref([])

// Fetch categories on component mount
onMounted(async () => {
  try {
    const response = await fetch('/api/categories')
    categories.value = await response.json()
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
})

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    serviceImage.value = file
  }
}

const handleSubmit = async (event) => {
  event.preventDefault()
  error.value = ''
  
  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('description', description.value)
  formData.append('time_required', time_required.value)
  formData.append('base_price', base_price.value)
  formData.append('service_pincodes', service_pincodes.value)
  
  if (category_id.value) {
    formData.append('category_id', category_id.value)
  }
  
  if (serviceImage.value) {
    formData.append('service_image', serviceImage.value)
  }
  
  try {
    const response = await fetch('/api/services', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      alert('Service added successfully')
      router.go(-1)
    } else {
      const data = await response.json()
      throw new Error(data.message || 'Failed to add service')
    }
  }
  catch(err) {
    error.value = err.message || 'Network error or server unreachable'
    alert(error.value)
  }
}
</script>

<template>
<body style="font-family: 'Poppins';">
  <main>
    <div id="forms" style="padding-top: 4%;">
      <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Add Service</p></div>
      <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
        <div class="mainform3">
          <div class="service">
            <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
              <div class="mb-2">
                <label for="serviceImage" class="form-label">Service Image:</label>
                <input type="file" class="form-control" id="serviceImage" accept="image/*" @change="handleImageUpload">
              </div>
              <div class="row mb-2">
                <div class="col-md-6">
                  <label for="serviceName" class="form-label">Service Name:</label>
                  <input v-model="name" type="text" class="form-control" id="serviceName" required>
                </div>
                <div class="col-md-6">
                  <label for="serviceCategory" class="form-label">Category:</label>
                  <select v-model="category_id" class="form-control" id="serviceCategory">
                    <option value="">Select a category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mb-2">
                <label for="description" class="form-label">Description:</label>
                <textarea v-model="description" class="form-control" id="description" rows="2" required></textarea>
              </div>
              <div class="row mb-1">
                <div class="col-md-6">
                  <label for="reqTime" class="form-label">Time required (minutes):</label>
                  <input v-model="time_required" type="number" class="form-control" id="reqTime" min="10" max="180" required placeholder="??">
                </div>
                <div class="col-md-6">
                  <label for="basePrice" class="form-label">Base Price:</label>
                  <input v-model="base_price" type="number" class="form-control" id="basePrice" min="10" required placeholder="₹">
                </div>
              </div>
              <div class="mb-1">
                <label for="serviceLocations" class="form-label">Service Pincodes:</label>
                <input v-model="service_pincodes" type="text" class="form-control" id="serviceLocations" placeholder="Enter comma-separated pincodes">
              </div>
              <div class="d-flex gap-4 py-2 justify-content-center">
                <button type="submit" class="btn btn-success">Add</button>
                <button type="button" class="btn btn-warning" @click="$router.go(-1)">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
</body>
</template>
