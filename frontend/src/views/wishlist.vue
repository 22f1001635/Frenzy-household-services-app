<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"

const wishlistItems = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/service-actions/wishlist')
    wishlistItems.value = response.data
  } catch (error) {
    console.error('Error fetching wishlist items:', error)
  }
})

const removeFromWishlist = async (itemId) => {
  try {
    await axios.delete(`/api/service-actions/${itemId}`)
    wishlistItems.value = wishlistItems.value.filter(item => item.id !== itemId)
  } catch (error) {
    console.error('Error removing item:', error)
    alert('Failed to remove item')
  }
}

const addToCart = async (serviceId) => {
  try {
    const response = await axios.post('/api/service-actions', {
      service_id: serviceId,
      action_type: 'cart',
      quantity: 1
    })
    alert('Item moved to cart!')
  } catch (error) {
    if (error.response?.data?.error_type === 'duplicate') {
      alert('This item is already in your cart')
    } else {
      console.error('Error moving to cart:', error)
      alert(error.response?.data?.message || 'Failed to move to cart')
    }
  }
}
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%;">
        <div id="back">
          <a href="javascript:window.history.back()">
            <i class="fa-solid fa-circle-left" style="font-size:250%;"></i>
          </a>
          <p class="text-dark" id="head">Your Wishlist</p>
        </div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="cart">
                <div class="cart-member" v-for="item in wishlistItems" :key="item.id">
                    <div class="cart-memeber-photo">
                        <img :src="`http://localhost:5000/service_images/${item.service.image_file}`" 
                             style="width: 90px; height: 90px; object-fit: cover; border-radius: 8px;">
                    </div>
                    <h4>{{ item.service.name }}</h4>
                    <button type="button" class="btn btn-warning" @click="addToCart(item.service.id)">
                        <i class="fa-duotone fa-solid fa-cart-plus fa-lg"></i>
                    </button>
                    <button type="button" class="btn btn-danger" @click="removeFromWishlist(item.id)">
                        <i class="fa-duotone fa-solid fa-trash-can fa-lg"></i>
                    </button>
                </div>
              </div>
            </div>
        </div>
    </div>
  </main>
</body>
</template>