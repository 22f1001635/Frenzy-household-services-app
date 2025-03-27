<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import { useRouter } from 'vue-router'
import "@/assets/styles/dashboard.css"

const router = useRouter()
const store = useStore()
const categories = ref([])
const servicesByCategory = ref({})
const selectedService = ref(null)
const quantity = ref(1)
const serviceContainers = ref({})
const hasServices = ref(false)
const professionalRequests = ref([])

const isUser = computed(() => store.state.user?.role === 'user')
const isProfessional = computed(() => store.state.user?.role === 'professional')

onMounted(async () => {
  if (isUser.value) {
    try {
      const [categoriesRes, servicesRes] = await Promise.all([
        axios.get('/api/categories/active'),
        axios.get('/api/services/active')
      ])
      
      categories.value = categoriesRes.data
      const allServices = servicesRes.data
      
      hasServices.value = allServices.length > 0
      
      categories.value.forEach(category => {
        servicesByCategory.value[category.id] = allServices.filter(
          service => service.category_id === category.id
        )
      })
    } catch (error) {
      console.error('Error fetching data:', error)
      alert('Failed to load dashboard data')
    }
  } else if (isProfessional.value) {
    try {
      const response = await axios.get('/api/professional/service-requests')
      professionalRequests.value = response.data
    } catch (error) {
      console.error('Error fetching requests:', error)
    }
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
  try {
    const response = await axios.post('/api/service-actions', {
      service_id: selectedService.value.id,
      action_type: actionType,
      quantity: quantity.value,
    });

    if (actionType === 'buy_now') {
      router.push({
        path: '/address',
        query: { 
          serviceId: selectedService.value.id,
          quantity: quantity.value,
          source: 'buy_now'
        }
      });
    } else {
      const message = actionType === 'cart' && response.data.new_quantity 
        ? `Quantity updated to ${response.data.new_quantity}`
        : `Service added to ${actionType.replace('_', ' ')}!`;
      alert(message);
      closeServiceDetails();
    }
  } catch (error) {
    if (error.response?.data?.error_type === 'duplicate') {
      alert(error.response.data.message || 'This item is already in your cart/wishlist.');
      if (actionType === 'buy_now') {
        router.push({
          path: '/address',
          query: { 
            serviceId: selectedService.value.id,
            quantity: quantity.value,
            source: 'buy_now'
          }
        });
      }
    } else {
      console.error('Action failed:', error);
      alert(error.response?.data?.message || 'Failed to perform action');
    }
  }
};

const handleRequestAction = async (requestId, action) => {
  try {
    await axios.patch(`/api/professional/service-requests/${requestId}`, { action })
    professionalRequests.value = professionalRequests.value.filter(req => req.id !== requestId)
    alert(`Request ${action}ed successfully`)
  } catch (error) {
    console.error('Error handling request:', error)
    alert(error.response?.data?.message || 'Action failed')
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
  <main style="padding-top: 4.5%; padding-bottom: 3.5%; padding-left: 6.25%; padding-right: 8.75%;">
    <!-- User Dashboard -->
    <div v-if="isUser" id="dashboard-container">
      <!-- No services message - global -->
      <div v-if="!hasServices" class="no-services-message">
        <h3>No services available currently</h3>
      </div>
      
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
          <!-- No services message for this category -->
          <p v-if="!servicesByCategory[category.id] || servicesByCategory[category.id].length === 0" 
             class="no-services-category">
            No services available in this category currently
          </p>
          
          <div 
            v-else
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
              <h3>{{ selectedService.name }}</h3>
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
                <button class="btn action-btn cart2" @click.stop="handleServiceAction('cart', $event)">
                  <i class="fas fa-shopping-cart"></i> Add to Cart
                </button>
                <button class="btn action-btn wishlist2" @click.stop="handleServiceAction('wishlist', $event)">
                  <i class="fas fa-heart"></i> Add to Wishlist
                </button>
                <button class="btn action-btn buy2" @click.stop="handleServiceAction('buy_now', $event)">
                  <i class="fas fa-bolt"></i> Book Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Professional Dashboard -->
    <div v-else-if="isProfessional" class="professional-dashboard">
      <h2 class="dashboard-heading">Service Requests</h2>
      
      <div v-if="professionalRequests.length === 0" class="no-requests">
        No pending service requests matching your service area
      </div>

      <table v-else class="requests-table">
        <thead>
          <tr>
            <th>Service</th>
            <th>Scheduled Date</th>
            <th>Quantity</th>
            <th>Total</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="req in professionalRequests" :key="req.id">
            <td>{{ req.service_name }}</td>
            <td>{{ new Date(req.scheduled_date).toLocaleString() }}</td>
            <td>{{ req.quantity }}</td>
            <td>₹{{ req.total_amount }}</td>
            <td class="action-buttons">
              <button 
                class="accept-btn"
                @click="handleRequestAction(req.id, 'accept')"
              >
                Accept
              </button>
              <button 
                class="reject-btn"
                @click="handleRequestAction(req.id, 'reject')"
              >
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Non-user message -->
    <div v-else class="non-user-message">
      <h2>Access Restricted</h2>
      <p>Please log in with a user or professional account to access this dashboard.</p>
    </div>
  </main>
</body>
</template>

<style scoped>
.no-services-message {
  text-align: center;
  padding: 30px;
  border-radius: 8px;
  margin: 20px 0;
  opacity: 0.3;
}

.no-services-category {
  text-align: center;
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
  font-style: italic;
  color: #666;
}

.professional-dashboard {
  padding: 20px;
}

.dashboard-heading {
  color: whitesmoke;
  opacity: 0.8;
  margin-bottom: 1.5rem;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.requests-table th,
.requests-table td {
  padding: 15px 15px;
  text-align: left;
  color: rgba(0, 0, 0, 0.623);
  border-bottom: 1px solid #ecf0f1;
}

.requests-table th {
  background-color: #f8f9fa;
  color: black;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.accept-btn {
  background: #4CAF50;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.accept-btn:hover {
  background: #3e8e41;
}

.reject-btn {
  background: #f44336;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reject-btn:hover {
  background: #d32f2f;
}

.no-requests {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
  font-style: italic;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.non-user-message {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  max-width: 600px;
  margin: 0 auto;
}

.non-user-message h2 {
  color: #e74c3c;
  margin-bottom: 15px;
}

.non-user-message p {
  color: #7f8c8d;
  font-size: 1.1rem;
}
</style>