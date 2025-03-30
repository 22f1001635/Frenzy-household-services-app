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
          <!-- Non-logged-in items -->
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" :class="{ active: $route.path === '/' }" to="/">Home</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" :class="{ active: $route.path === '/about' }" to="/about">About</router-link>
          </li>

          <!-- Logged-in items -->
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :class="{ active: $route.path === '/dashboard' }" to="/dashboard">Services</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" :class="{ active: $route.path === '/statistics' }" to="/statistics">Statistics</router-link>
          </li>

        </ul>

        <!-- Search (logged-in only) -->
        <div class="find" v-if="isLoggedIn">
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

        <!-- Right section -->
        <div class="d-flex align-items-center">
          <!-- Cart -->
          <div id="shopping" class="ms-2" v-if="isLoggedIn">
            <router-link to="/cart"><i class="fa-solid fa-cart-shopping" draggable="false"></i></router-link>
          </div>

          <!-- Notifications -->
          <div class="notification-dropdown ms-2 position-relative" v-if="isLoggedIn">
            <button class="btn btn-link text-dark" @click="toggleNotifications">
              <i class="fa-solid fa-bell" style="color: aqua;"></i>
            </button>
            <div v-if="showNotifications" class="dropdown-menu show position-absolute end-0 mt-1">
              <div class="dropdown-item small">No new notifications</div>
            </div>
          </div>

          <!-- Auth section -->
          <div id="user" class="d-flex align-items-center">
            <div v-if="isLoggedIn" class="d-flex align-items-center">
              <router-link to="/profile" class="d-flex align-items-center text-decoration-none">
                <img :src="userImage" alt="Profile" class="rounded-circle border border-3 border-light-subtle" style="width: 30px; height: 30px;">
                <span class="d-none d-md-inline ms-1">{{ user?.username.split(' ')[0] }}</span>
              </router-link>
              <button @click="handleLogout" class="btn btn-outline-danger ms-2">Logout</button>
            </div>
            
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
import { ref } from 'vue';
import { useStore } from 'vuex';
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const showNotifications = ref(false);

    const isLoggedIn = computed(() => store.getters.isAuthenticated);
    const user = computed(() => store.getters.currentUser);
    const userImage = computed(() => store.getters.userImage);

    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value;
    };

    onMounted(() => {
      store.dispatch('fetchUser');
    });

    const handleLogout = async () => {
      await store.dispatch('logout');
      router.push('/');
    };

    return {
      isLoggedIn,
      user,
      userImage,
      showNotifications,
      toggleNotifications,
      handleLogout
    };
  }
};
</script>

<style scoped>
.notification-dropdown .dropdown-menu {
  max-height: 300px;
  overflow-y: auto;
  min-width: 250px;
}
</style>