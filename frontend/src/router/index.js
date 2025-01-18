import { createRouter, createWebHistory } from 'vue-router'
import home from '../views/home.vue'
import about from '../views/aboutus.vue'
import cart from '../views/cart.vue'
import address from '../views/address.vue'
import confirmorder from '@/views/confirmorder.vue'
import contactus from '@/views/contactus.vue'
import dashboard from '@/views/dashboard.vue'
import payment from '@/views/payment.vue'
import profile from '@/views/profile.vue'
import review from '@/views/review.vue'
import scruitny from '@/views/scruitny.vue'
import service from '@/views/service.vue'
import signin from '@/views/signin.vue'
import signup from '@/views/signup.vue'
import summary from '@/views/statistics.vue'
import wishlist from '@/views/wishlist.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: home,
    meta:{
      title:'Household Services -Frenzy',
      description :'Home page of Frenzy the household services app'
    }
  },
  {
    path: '/about',
    name: 'about',
    component: about,
    meta:{
      title:'About Us -Frenzy',
      description :'Explore how Frenzy the household app was incepted'
    }
  },
  {
    path: '/cart',
    name: 'cart',
    component: cart,
    meta:{
      title:'Services Cart',
      description :'You are visiting your cart at frenzy'
    }
  },
  {
    path: '/address',
    name: 'address',
    component: address,
    meta:{
      title:'Cart-Address',
      description :'you are providing your address for delivery of item in cart of your Frenzy account'
    }
  },
  {
    path: '/confirmorder',
    name: 'confirmorder',
    component: confirmorder,
    meta:{
      title:'Order Status',
      description :'View order status for the order you placed at frenzy'
    }
  },
  {
    path: '/contactus',
    name: 'contactus',
    component: contactus,
    meta:{
      title:'Contact Us -Frenzy',
      description :'You have reached the support/contact us page of frenzy! get your queries answered swiftly.'
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: dashboard,
    meta:{
      title:'Dashboard',
      description :'You have reached your dashboard at frenzy'
    }
  },
  {
    path: '/payment',
    name: 'payment',
    component: payment,
    meta:{
      title:'Cart-Payment',
      description :'you are providing your payment details for delivery of item in cart of your Frenzy account'
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: profile,
    meta:{
      title:'Profile',
      description :'View your profile,previous order and items in your wishlist at frenzy'
    }
  },
  {
    path: '/review',
    name: 'review',
    component: review,
    meta:{
      title:'Order Review',
      description :'please provide review for the order you placed with us!'
    }
  },
  {
    path: '/scruitny',
    name: 'scruitny',
    component: scruitny,
    meta:{
      title:'Edit existing service',
      description :'provide scruitny for existing service such as price,name change,etc.'
    }
  },
  {
    path: '/service',
    name: 'service',
    component: service,
    meta:{
      title:'Add a new service',
      description :'provide details for addition of new service to the frenzy app'
    }
  },
  {
    path: '/signin',
    name: 'signin',
    component: signin,
    meta:{
      title:'Signin -Frenzy',
      description :'login to your existing account in the frenzy app'
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: signup,
    meta:{
      title:'Signup -Frenzy',
      description :'Register a new account in the frenzy app'
    }
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: summary,
    meta:{
      title:'view statistics -Frenzy',
      description :'View your statistics regarding order,etc at frenzy'
    }
  },
  {
    path: '/wishlist',
    name: 'wishlist',
    component: wishlist,
    meta:{
      title:'Services Wishlist',
      description :'You are visiting your wishlist at frenzy'
    }
  }
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  const { title, description } = to.meta;
  const defaultTitle = 'Frenzy';
  const defaultDescription = 'The household services app';

  document.title = title || defaultTitle

  const descriptionElement = document.querySelector('head meta[name="description"]')

  descriptionElement.setAttribute('content', description || defaultDescription)
})

export default router