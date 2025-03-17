<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import "@/assets/styles/dashboard.css"
const store = useStore()
const categories = ref([])
const servicesByCategory = ref({})
const selectedService = ref(null)
const quantity = ref(1)
const serviceContainers = ref({})

const isUser = computed(() => store.state.user?.role === 'user')

onMounted(async () => {
  if (!isUser.value) return

  try {
    const [categoriesRes, servicesRes] = await Promise.all([
      axios.get('/api/categories/active'),
      axios.get('/api/services/active')
    ])
    
    categories.value = categoriesRes.data
    const allServices = servicesRes.data
    
    categories.value.forEach(category => {
      servicesByCategory.value[category.id] = allServices.filter(
        service => service.category_id === category.id
      )
    })
  } catch (error) {
    console.error('Error fetching data:', error)
    alert('Failed to load dashboard data')
  }
})


const scroll = (categoryId, direction) => {
  const container = serviceContainers.value[categoryId] 
  if (container) {
    const scrollAmount = direction === 'left' ? -300 : 300
    container.scrollBy({ left: scrollAmount, behavior: 'smooth' })
  }
}

const openServiceDetails = (service, event) => {
  if (event && event.target.closest('.view-details-btn')) {
    event.stopPropagation()
  }
  selectedService.value = service
}

const closeServiceDetails = () => {
  selectedService.value = null
  quantity.value = 1
}

const handleServiceAction = async (actionType, event) => {
  if (event) {
    event.stopPropagation()
  }

  if (!selectedService.value) return
  
  try {
    await axios.post('/api/service-actions', {
      service_id: selectedService.value.id,
      action_type: actionType,
      quantity: quantity.value
    })
    
    alert(`Service added to ${actionType.replace('_', ' ')}!`)
    closeServiceDetails()
  } catch (error) {
    console.error('Action failed:', error)
    alert('Failed to perform action')
  }
}
const registerContainerRef = (el, categoryId) => {
  if (el) {
    serviceContainers.value[categoryId] = el
  }
}
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top: 1.5%;">
    <div v-if="isUser" id="dashboard-container">
      <div v-for="category in categories" :key="category.id" class="category-section">
        <div class="category-header">
          <h2 class="category-title">{{ category.name }}</h2>
          <div class="scroll-arrows">
            <button class="nav-arrow" @click.stop="scroll(category.id, 'left')">
              <i class="fas fa-chevron-left"></i>
            </button>
            <button class="nav-arrow" @click.stop="scroll(category.id, 'right')">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
        
        <div class="services-carousel">
          <div 
            class="services-wrapper"
            :ref="el => registerContainerRef(el, category.id)"
          >
            <div 
              v-for="service in servicesByCategory[category.id]" 
              :key="service.id" 
              class="service-card"
              @click="openServiceDetails(service, $event)"
            >
              <div class="service-image">
                <img 
                  :src="`http://localhost:5000/service_images/${service.image_file}`" 
                  alt="Service image"
                >
              </div>
              <div class="service-info">
                <h3>{{ service.name }}</h3>
                <div class="price-badge">₹{{ service.base_price }}</div>
                <button class="view-details-btn" @click.stop="openServiceDetails(service, $event)">
                  View Details <i class="fas fa-arrow-right"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Details Overlay -->
      <div v-if="selectedService" class="service-detail-overlay" @click="closeServiceDetails">
        <div class="service-detail-modal" @click.stop>
          <button class="close-btn" @click="closeServiceDetails">&times;</button>
          
          <div class="detail-content">
            <div class="detail-image">
              <img :src="`http://localhost:5000/service_images/${selectedService.image_file}`" 
                   alt="Service image">
            </div>
            
            <div class="detail-info">
              <h2>{{ selectedService.name }}</h2>
              <div class="meta-info">
                <span class="price">₹{{ selectedService.base_price }}</span>
                <span class="duration">{{ selectedService.time_required }} mins</span>
              </div>
              
              <p class="description">{{ selectedService.description }}</p>
              
              <div class="pincode-section">
                <h4>Available in:</h4>
                <div class="pincodes">
                    <span v-for="pincode in selectedService.service_pincodes" :key="pincode" class="pincode-badge">
                    {{ pincode }}
                    </span>
                </div>
              </div>

              <div class="quantity-control">
                <button @click.stop="quantity > 1 ? quantity-- : null">-</button>
                <input type="number" v-model.number="quantity" min="1" @click.stop>
                <button @click.stop="quantity++">+</button>
              </div>

              <div class="action-buttons">
                <button class="btn action-btn cart" @click.stop="handleServiceAction('cart', $event)">
                  <i class="fas fa-shopping-cart"></i> Add to Cart
                </button>
                <button class="btn action-btn wishlist" @click.stop="handleServiceAction('wishlist', $event)">
                  <i class="fas fa-heart"></i> Add to Wishlist
                </button>
                <button class="btn action-btn buy" @click.stop="handleServiceAction('buy_now', $event)">
                  <i class="fas fa-bolt"></i> Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Non-user message -->
    <div v-else class="non-user-message">
      <h2>Access Restricted</h2>
      <p>Please log in with a user account to access this dashboard.</p>
    </div>
  </main>
</body>
</template>
