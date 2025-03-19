<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"

const cartItems = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/service-actions/cart')
    cartItems.value = response.data
  } catch (error) {
    console.error('Error fetching cart items:', error)
  }
})

const removeFromCart = async (itemId) => {
  try {
    await axios.delete(`/api/service-actions/${itemId}`)
    cartItems.value = cartItems.value.filter(item => item.id !== itemId)
  } catch (error) {
    console.error('Error removing item:', error)
    alert('Failed to remove item')
  }
}

const updateQuantity = async (itemId, newQuantity) => {
  try {
    await axios.patch(`/api/service-actions/${itemId}`, {
      quantity: newQuantity
    })
  } catch (error) {
    console.error('Error updating quantity:', error)
    alert('Failed to update quantity')
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
          <p class="text-dark" id="head">Your Cart</p>
        </div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="cart">
                <div class="cart-member" v-for="item in cartItems" :key="item.id">
                    <div class="cart-memeber-photo">
                        <img :src="`http://localhost:5000/service_images/${item.service.image_file}`" 
                             style="width: 90px; height: 90px; object-fit: cover; border-radius: 8px;">
                    </div>
                    <h4>{{ item.service.name }}</h4>
                    <input type="number" class="form-control" id="quantity" v-model.number="item.quantity" min="1" max="9" @change="updateQuantity(item.id, item.quantity)">
                    <button type="button" class="btn btn-danger" @click="removeFromCart(item.id)">
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
