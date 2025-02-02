<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, watch, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const services = ref([])
const selectedService = ref(null)
const formData = ref({
  time_required: '',
  base_price: '',
  service_pincodes: ''
})

// Fetch all services on component mount
onMounted(async () => {
  try {
    const response = await fetch('/api/services')
    services.value = await response.json()
  } catch (error) {
    console.error('Error fetching services:', error)
    alert('Failed to load services')
  }
})

// Watch for service selection changes
watch(selectedService, async (newVal) => {
  if (!newVal) return
  
  try {
    const response = await fetch(`/api/services/${newVal}`)
    const service = await response.json()
    
    formData.value = {
      time_required: service.time_required,
      base_price: service.base_price,
      service_pincodes: service.service_pincodes
    }
  } catch (error) {
    console.error('Error fetching service details:', error)
    alert('Failed to load service details')
  }
})

const handleUpdate = async () => {
  if (!selectedService.value || !confirm('Are you sure you want to update this service?')) {
    alert('Please select a service first')
    return
  }

  try {
    const response = await fetch(`/api/services/${selectedService.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        time_required: parseInt(formData.value.time_required),
        base_price: parseFloat(formData.value.base_price),
        service_pincodes: formData.value.service_pincodes
      })
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
      formData.value = { time_required: '', base_price: '', service_pincodes: '' }
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
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Edit Service</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="service">
                <form class="pt-3">
                    <div class="form-group mb-3">
                      <label for="existingService">Select Existing Service:</label>
                      <select class="form-control" id="existingService" v-model="selectedService">
                        <option :value="null">Select a service</option>
                        <option v-for="service in services" :key="service.id" :value="service.id">
                          {{ service.name }}
                        </option>
                      </select>
                    </div>
                    <div class="form-group mb-3">
                      <label for="reqTime" class="form-label">Time required:</label>
                      <input type="number" class="form-control" id="reqTime" min="1" step="10" max="180" required placeholder="??"v-model="formData.time_required">
                    </div>
                    <div class="form-group mb-3">
                      <label for="basePrice">Base Price:</label>
                      <input type="number" class="form-control" id="basePrice" placeholder="Enter base price" v-model="formData.base_price">
                    </div>
                    <div class="form-group mb-3">
                      <label for="serviceLocations">Service Pincodes:</label>
                      <input type="text" class="form-control" id="serviceLocations" placeholder="Enter comma-separated pincodes" v-model="formData.service_pincodes">
                    </div>
                    <div class="d-flex py-2 gap-4 justify-content-center">
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
