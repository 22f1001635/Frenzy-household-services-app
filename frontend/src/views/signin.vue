<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/sign.css"
import axios from 'axios'
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const store = useStore()
const router = useRouter()
const error = ref('')

const handleSubmit = async (event) => {
    event.preventDefault()
    error.value = ''
    try {
        const response = await axios.post('/api/signin', {  
                email: email.value,
                password: password.value     
        },{
            timeout: 3000  // 3 second timeout
        })
        await store.dispatch('fetchUser')
        
        // Redirect based on role
        if (store.getters.isAdmin) {
            router.push('/service')
        } else {
            router.push('/profile')
        }
    }
    catch(err){
        error.value = err.response?.data?.message || 'Network error or server unreachable'
        alert(error.value)
    }
}
</script>

<template>
<body style="font-family: 'Poppins';">
    <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a></div>
        <div id="box" class="bg-light text-dark">
            <img src="../assets/images/login.svg" draggable="false">
            <div class="mainform">
                <h3>Welcome Back!</h3>
                <h6>Enter your Credentials to access your account</h6>
                <!--Form Fields-->
                <form @submit="handleSubmit">
                    <div class="form-group pt-1 pb-2">
                        <label class="form-label">Email address</label>
                        <input 
                            type="email" 
                            class="form-control" 
                            aria-describedby="emailHelp"
                            v-model="email"
                            required
                        >
                        <div id="emailHelp" class="opacity-25">We'll never share your email with anyone else.</div>                    
                    </div>
                    <div class="form-group pb-2">
                        <label class="form-label">Password</label>
                        <input 
                            type="password" 
                            class="form-control"
                            v-model="password"
                            required
                        >                    
                    </div>
                    <!--form submit button-->
                    <div class="form-group py-3 px-5">
                        <button type="submit" class="btn btn-primary col-12">Submit</button>
                    </div>
                </form>
                <div class="border-top pt-2">
                    <p class="text-dark-muted opacity-75">
                        Don't have an account? <router-link to="/signup">Sign Up</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
    </main>
</body>
</template>
