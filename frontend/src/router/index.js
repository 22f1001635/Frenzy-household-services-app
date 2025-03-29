import { createRouter, createWebHistory } from 'vue-router';
import store from "../store";
import home from '@/views/home.vue';
import about from '@/views/aboutus.vue';
import cart from '@/views/cart.vue';
import address from '@/views/address.vue';
import confirmorder from '@/views/confirmorder.vue';
import dashboard from '@/views/dashboard.vue';
import payment from '@/views/payment.vue';
import profile from '@/views/profile.vue';
import review from '@/views/review.vue';
import serviceedit from '@/views/serviceedit.vue';
import service from '@/views/service.vue';
import signin from '@/views/signin.vue';
import signup from '@/views/signup.vue';
import summary from '@/views/statistics.vue';
import wishlist from '@/views/wishlist.vue';
import test from '@/views/test.vue';
import categorymanagement from '@/views/categorymanagement.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: home,
    meta: {
      title: 'Household Services - Frenzy',
      description: 'Home page of Frenzy the household services app'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: about,
    meta: {
      title: 'About Us - Frenzy',
      description: 'Explore how Frenzy the household app was incepted'
    }
  },
  {
    path: '/cart',
    name: 'cart',
    component: cart,
    meta: {
      title: 'Services Cart',
      description: 'You are visiting your cart at Frenzy'
    }
  },
  {
    path: '/address',
    name: 'address',
    component: address,
    meta: {
      title: 'Cart - Address',
      description: 'You are providing your address for delivery of items in your Frenzy cart'
    }
  },
  {
      path: '/confirmorder',
      name: 'confirmorder',
      component: confirmorder,
      meta: {
        title: 'Order Confirmation',
        description: 'View your order confirmation details',
        requiresAuth: true
      }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: dashboard,
    meta: {
      title: 'Dashboard',
      description: 'You have reached your dashboard at Frenzy'
    }
  },
  {
    path: '/payment',
    name: 'payment',
    component: payment,
    meta: {
      title: 'Cart - Payment',
      description: 'You are providing your payment details for delivery of items in your Frenzy cart'
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: profile,
    meta: {
      title: 'Profile',
      description: 'View your profile, previous orders, and items in your wishlist at Frenzy',
      requiresAuth: true
    }
  },
  {
    path: '/review',
    name: 'review',
    component: review,
    meta: {
      title: 'Order Review',
      description: 'Please provide a review for the order you placed with us!'
    }
  },
  {
    path: '/serviceedit',
    name: 'serviceedit',
    component: serviceedit,
    meta: {
      title: 'Edit Existing Service',
      description: 'Provide scrutiny for existing services such as price, name change, etc.',
      requiresAdmin: true
    }
  },
  {
    path: '/categorymanagement',
    name: 'categorymanagement',
    component: categorymanagement,
    meta: {
      title: 'Manage Service Categories',
      description: 'Provide scrutiny for service categories such as add, delete, etc.',
      requiresAdmin: true
    }
  },
  {
    path: '/service',
    name: 'service',
    component: service,
    meta: {
      title: 'Add a New Service',
      description: 'Provide details for the addition of a new service to the Frenzy app',
      requiresAdmin: true
    }
  },
  {
    path: '/signin',
    name: 'signin',
    component: signin,
    meta: {
      title: 'Sign In - Frenzy',
      description: 'Log in to your existing account in the Frenzy app',
      requiresGuest: true
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: signup,
    meta: {
      title: 'Sign Up - Frenzy',
      description: 'Register a new account in the Frenzy app',
      requiresGuest: true
    }
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: summary,
    meta: {
      title: 'View Statistics - Frenzy',
      description: 'View your statistics regarding orders, etc. at Frenzy'
    }
  },
  {
    path: '/wishlist',
    name: 'wishlist',
    component: wishlist,
    meta: {
      title: 'Services Wishlist',
      description: 'You are visiting your wishlist at Frenzy'
    }
  },
  {
    path: '/test',
    name: 'test',
    component: test
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach(async (to) => {
  // Fetch user if not already loaded
  if (store.state.user === null) {
    await store.dispatch('fetchUser');
  }

  const user = store.state.user;
  const isAuthenticated = store.getters.isAuthenticated;
  const isAdmin = store.getters.isAdmin;

  // Check if the user is blocked
  if (user?.is_blocked) {
    await store.dispatch('logout');
    alert('Your account has been blocked.');
    return { path: '/' };
  }

  // Handle route guards
  if (to.meta.requiresAuth && !isAuthenticated) {
    return { path: '/signin' };
  }

  if (to.meta.requiresAdmin && !isAdmin) {
    return { path: '/profile' };
  }

  if (to.meta.requiresGuest && isAuthenticated) {
    return { path: '/profile' };
  }

  return true;
});

router.afterEach((to) => {
  const { title, description } = to.meta;
  const defaultTitle = 'Frenzy';
  const defaultDescription = 'The household services app';

  document.title = title || defaultTitle;

  const descriptionElement = document.querySelector('head meta[name="description"]');
  if (descriptionElement) {
    descriptionElement.setAttribute('content', description || defaultDescription);
  }
});

export default router;