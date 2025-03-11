<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const categories = ref([])
const newCategory = ref({ name: '', description: '' })
const selectedCategory = ref(null)
const editData = ref({ name: '', description: '' })
const showManageForm = ref(false)
const router = useRouter()
const error = ref('')

onMounted(async () => {
  await fetchCategories()
})

const fetchCategories = async () => {
  try {
    const response = await fetch('/api/categories')
    categories.value = await response.json()
  } catch (error) {
    console.error('Error fetching categories:', error)
    error.value = 'Failed to fetch categories'
  }
}

// Watcher to load category data when selected
watch(selectedCategory, async (categoryId) => {
  if (categoryId) {
    try {
      const response = await fetch(`/api/categories/${categoryId}`)
      const category = await response.json()
      editData.value = {
        name: category.name,
        description: category.description
      }
    } catch (error) {
      console.error('Error fetching category details:', error)
      error.value = 'Failed to fetch category details'
    }
  }
})

const handleCreate = async () => {
  error.value = ''
  try {
    const response = await fetch('/api/categories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCategory.value)
    })
    if (response.ok) {
      await fetchCategories()
      newCategory.value = { name: '', description: '' }
      alert('Category created successfully')
    } else {
      const errorData = await response.json()
      error.value = errorData.message || 'Failed to create category'
      alert(error.value)
    }
  } catch (error) {
    console.error('Error creating category:', error)
    error.value = 'Network error or server unreachable'
    alert(error.value)
  }
}

const handleUpdate = async () => {
  error.value = ''
  try {
    const response = await fetch(`/api/categories/${selectedCategory.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editData.value)
    })
    if (response.ok) {
      await fetchCategories()
      selectedCategory.value = null
      showManageForm.value = false
      alert('Category updated successfully')
    } else {
      const errorData = await response.json()
      error.value = errorData.message || 'Failed to update category'
      alert(error.value)
    }
  } catch (error) {
    console.error('Error updating category:', error)
    error.value = 'Network error or server unreachable'
    alert(error.value)
  }
}

const handleDelete = async (id) => {
  if (confirm('Are you sure you want to delete this category?')) {
    try {
      const response = await fetch(`/api/categories/${id}`, { method: 'DELETE' })
      if (response.ok) {
        await fetchCategories()
        selectedCategory.value = null
        showManageForm.value = false
        alert('Category deleted successfully')
      } else {
        const errorData = await response.json()
        error.value = errorData.message || 'Delete failed'
        alert(error.value)
      }
    } catch (error) {
      console.error('Error deleting category:', error)
      error.value = 'Network error or server unreachable'
      alert(error.value)
    }
  }
}

const handleStatusToggle = async (id) => {
  try {
    const response = await fetch(`/api/categories/${id}`, { method: 'PATCH' })
    if (response.ok) {
      await fetchCategories()
      alert('Category status updated successfully')
    } else {
      const errorData = await response.json()
      error.value = errorData.message || 'Status update failed'
      alert(error.value)
    }
  } catch (error) {
    console.error('Error toggling category status:', error)
    error.value = 'Network error or server unreachable'
    alert(error.value)
  }
}

const toggleManageForm = () => {
  showManageForm.value = !showManageForm.value
  if (!showManageForm.value) {
    selectedCategory.value = null
  }
}

const handleCancel = () => {
  newCategory.value = { name: '', description: '' }
  if (showManageForm.value) {
    showManageForm.value = false
    selectedCategory.value = null
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
        <p class="text-dark" id="head" style="font-size: 1.5em; margin-left: 32.5vw;">Category Management</p>
      </div>
      <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
        <div class="mainform3">
          <div class="service mt-5">
            <!-- Create Category Form -->
            <div v-if="!showManageForm">
              <form @submit.prevent="handleCreate">
                <div class="mb-2">
                  <label for="categoryName" class="form-label">Category Name:</label>
                  <input v-model="newCategory.name" type="text" class="form-control" id="categoryName" required>
                </div>
                <div class="mb-2">
                  <label for="description" class="form-label">Description:</label>
                  <textarea v-model="newCategory.description" class="form-control" id="description" rows="2" required></textarea>
                </div>
                <div class="d-flex gap-4 py-2 justify-content-center">
                  <button type="submit" class="btn btn-success">Create</button>
                  <button type="button" class="btn btn-warning" @click="handleCancel">Cancel</button>
                  <button type="button" class="btn btn-primary" @click="toggleManageForm">Manage</button>
                </div>
              </form>
            </div>

            <!-- Edit Category Form -->
            <div v-if="showManageForm">
              <div class="mb-3 px-1">
                <label for="categorySelect" class="form-label">Select Category:</label>
                <select v-model="selectedCategory" class="form-control" id="categorySelect">
                  <option :value="null">Select category</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>

              <form v-if="selectedCategory" @submit.prevent="handleUpdate">
                <div class="mb-2">
                  <label for="editCategoryName" class="form-label">Category Name:</label>
                  <input v-model="editData.name" type="text" class="form-control" id="editCategoryName" required>
                </div>
                <div class="mb-2">
                  <label for="editDescription" class="form-label">Description:</label>
                  <textarea v-model="editData.description" class="form-control" id="editDescription" rows="2" required></textarea>
                </div>
                <div class="d-flex gap-3 py-2 justify-content-center">
                  <button type="submit" class="btn btn-success">Update</button>
                  <button type="button" class="btn btn-danger" @click="handleDelete(selectedCategory)">Delete</button>
                  <button type="button" class="btn btn-info" @click="handleStatusToggle(selectedCategory)">Toggle Status</button>
                  <button type="button" class="btn btn-warning" @click="toggleManageForm">Back</button>
                </div>
              </form>

              <div v-if="!selectedCategory" class="d-flex justify-content-center pt-3">
                <button type="button" class="btn btn-warning" @click="toggleManageForm">Back to Create</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</body>
</template>