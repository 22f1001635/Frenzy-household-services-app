<template>
    <div>
    <h2>Flask API Test</h2>
    <button @click="fetchData">Fetch Data</button>
    <div v-if="data">{{ data }}</div>
    <div v-if="error">{{ error }}</div>
  </div>
</template>
<script setup>
import axios from 'axios'
import { ref } from 'vue'

const data = ref(null)
const error = ref(null)

const fetchData = async () => {
  try {
    const response = await axios.get('/api/data')
    data.value = response.data
    error.value = null
  } catch (err) {
    error.value = 'Error fetching data: ' + err.message
    data.value = null
  }
}
</script>