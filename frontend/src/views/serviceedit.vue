<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, watch, onMounted } from 'vue'

const services = ref([])
const categories = ref([])
const selectedService = ref(null)
const formData = ref({
  name: '',
  time_required: '',
  base_price: '',
  service_pincodes: '',
  category_id: null
})
const serviceImage = ref(null)

// Fetch all services and categories on component mount
onMounted(async () => {
  try {
    const [servicesRes, categoriesRes] = await Promise.all([
      fetch('/api/services'),
      fetch('/api/categories')
    ])
    services.value = await servicesRes.json()
    categories.value = await categoriesRes.json()
  } catch (error) {
    console.error('Error fetching data:', error)
    alert('Failed to load data')
  }
})

// Watch for service selection changes
watch(selectedService, async (newVal) => {
  if (!newVal) return
  
  try {
    const response = await fetch(`/api/services/${newVal}`)
    const service = await response.json()
    
    formData.value = {
      name: service.name,
      time_required: service.time_required,
      base_price: service.base_price,
      service_pincodes: service.service_pincodes,
      category_id: service.category_id
    }
  } catch (error) {
    console.error('Error fetching service details:', error)
    alert('Failed to load service details')
  }
})

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    serviceImage.value = file
  }
}

const handleUpdate = async () => {
  if (!selectedService.value || !confirm('Are you sure you want to update this service?')) {
    alert('Please select a service first')
    return
  }

  const formDataObj = new FormData()
  formDataObj.append('name', formData.value.name)
  formDataObj.append('time_required', formData.value.time_required)
  formDataObj.append('base_price', formData.value.base_price)
  formDataObj.append('service_pincodes', formData.value.service_pincodes)
  formDataObj.append('category_id', formData.value.category_id)
  
  if (serviceImage.value) {
    formDataObj.append('service_image', serviceImage.value)
  }

  try {
    const response = await fetch(`/api/services/${selectedService.value}`, {
      method: 'PUT',
      body: formDataObj
    })

    if (response.ok) {
      alert('Service updated successfully')
      // Refresh services list
      const refreshRes = await fetch('/api/services')
      services.value = await refreshRes.json()
    } else {
      throw new Error(await response.text())
    }
  } catch (error) {
    console.error('Update error:', error)
    alert('Failed to update service')
  }
}

const handleDelete = async () => {
  if (!selectedService.value || !confirm('Are you sure you want to delete this service?')) return

  try {
    const response = await fetch(`/api/services/${selectedService.value}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      alert('Service deleted successfully')
      // Reset form and refresh list
      selectedService.value = null
      formData.value = { name: '', time_required: '', base_price: '', service_pincodes: '', category_id: null }
      const refreshRes = await fetch('/api/services')
      services.value = await refreshRes.json()
    }
  } catch (error) {
    console.error('Delete error:', error)
    alert('Failed to delete service')
  }
}

const handleBlock = async () => {
  if (!selectedService.value || !confirm('Are you sure you want to block/activate this service?')) return

  try {
    const response = await fetch(`/api/services/${selectedService.value}`, {
      method: 'PATCH'
    })

    if (response.ok) {
      const data = await response.json() // Get updated status
      alert(`Service ${data.is_active ? 'Activated' : 'Blocked'}`)
      // Refresh services list
      const refreshRes = await fetch('/api/services')
      services.value = await refreshRes.json()
    }
  } catch (error) {
    console.error('Block error:', error)
    alert('Failed to update service status')
  }
}
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top: 2.75vw;">
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Edit Service</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="service">
                <form>
                    <div class="form-group mb-3">
                      <label for="existingService">Select Existing Service:</label>
                      <select class="form-control" id="existingService" v-model="selectedService">
                        <option :value="null">Select a service</option>
                        <option v-for="service in services" :key="service.id" :value="service.id">
                          {{ service.name }}
                        </option>
                      </select>
                    </div>
                    <div class="row mb-2">
                      <div class="col-md-6">
                        <label for="serviceName">Service Name:</label>
                        <input type="text" class="form-control" id="serviceName" v-model="formData.name" required>
                      </div>
                      <div class="col-md-6">
                        <label for="serviceCategory">Category:</label>
                        <select class="form-control" id="serviceCategory" v-model="formData.category_id">
                          <option :value="null">Select category</option>
                          <option v-for="category in categories" :key="category.id" :value="category.id">
                            {{ category.name }}
                          </option>
                        </select>
                      </div>
                    </div>
                    <div class="row mb-2">
                      <div class="col-md-6">
                        <label for="reqTime" class="form-label">Time required:</label>
                        <input type="number" class="form-control" id="reqTime" min="1" step="10" max="180" required placeholder="??" v-model="formData.time_required">
                      </div>
                      <div class="col-md-6">
                        <label for="basePrice" class="form-label">Base Price:</label>
                        <input type="number" class="form-control" id="basePrice" placeholder="Enter base price" v-model="formData.base_price">
                      </div>
                    </div>
                    <div class="form-group mb-2">
                      <label for="serviceLocations">Service Pincodes:</label>
                      <input type="text" class="form-control" id="serviceLocations" placeholder="Enter comma-separated pincodes" v-model="formData.service_pincodes">
                    </div>
                    <div class="form-group mb-2">
                      <label for="serviceImage">Update Service Image:</label>
                      <input type="file" class="form-control" id="serviceImage" @change="handleImageUpload">
                    </div>
                    <div class="d-flex px-2 py-2 gap-3 justify-content-center">
                    <button type="button" class="btn btn-success" @click="handleUpdate">Update</button>
                    <button type="button" class="btn btn-warning" @click="handleBlock">Block/Activate</button>
                    <button type="button" class="btn btn-danger" @click="handleDelete">Delete</button>
                    <button type="button" class="btn btn-secondary" @click="$router.go(-1)">Cancel</button>
                    </div>
                  </form>
              </div>
            </div>
        </div>
    </div>
    </main>
</body>
</template>
