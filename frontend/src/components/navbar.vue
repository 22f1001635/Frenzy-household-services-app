<template>
  <nav class="navbar fixed-top navbar-expand-xl bg-body-tertiary">
    <div class="container-fluid py-2" id="nav2">
      <a class="navbar-brand">Frenzy</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <div id="bars"><i class="fa-solid fa-bars"></i></div>
        <div id="x-mark"><i class="fa-solid fa-xmark"></i></div>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/' }" aria-current="page" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/dashboard' }" aria-current="page" to="/dashboard">Services</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/about' }" to="/about">About</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.path === '/contactus' }" to="/contactus">Contact Us</router-link>
          </li>
        </ul>
        <div class="find">
          <div class="search-container me-2">
            <input class="form-control" type="search" placeholder="Search" id="searchInput">
            <div class="search-modal" id="searchModal">
              <div class="p-2">
                <div class="search-results">
                  <div class="search-item">
                    Sample Result 1
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="d-flex align-items-center">
          <!-- Show cart only if user is logged in -->
          <div id="shopping" style="padding-left: 1vw;" v-if="isLoggedIn">
            <router-link to="/cart"><i class="fa-solid fa-cart-shopping" draggable="false"></i></router-link>
          </div>
          <!-- Authentication section -->
          <div id="user" class="d-flex align-items-center">
            <!-- User is logged in -->
            <div v-if="isLoggedIn" class="d-flex align-items-center">
              <router-link to="/profile" class="d-flex align-items-center text-decoration-none">
                <img :src="userImage" alt="Profile" class="rounded-circle border border-3 border-light-subtle" style="width: 30px; height: 30px;">
                <span class="d-none d-md-inline ms-1">{{ user?.username.split(' ')[0] }}</span>
              </router-link>
              <div id="logout" style="padding-left: 1.25vw;"></div><button  @click="handleLogout" class="btn btn-outline-danger ms-2">Logout</button>
            </div>
            <!-- User is NOT logged in -->
            <div v-else class="d-flex align-items-center">
              <router-link to="/signin" class="btn btn-outline-success me-2">SignIn</router-link>
              <router-link to="/signup" class="btn btn-primary">SignUp</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>

import { useStore } from 'vuex';
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // Using the correct getter names from your store
    const isLoggedIn = computed(() => store.getters.isAuthenticated);
    const user = computed(() => store.getters.currentUser);
    const userImage = computed(() => store.getters.userImage);
    
    // Fetch user data when component mounts
    onMounted(() => {
      store.dispatch('fetchUser');
    });
    
    // Logout handler
    const handleLogout = async () => {
      await store.dispatch('logout'); // Call the logout action
      router.push('/'); // Redirect to home page
    };
    
    return {
      isLoggedIn,
      user,
      userImage,
      handleLogout,
    };
  }
};
</script>