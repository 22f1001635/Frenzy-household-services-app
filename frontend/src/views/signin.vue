<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/sign.css"
import axios from 'axios'
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const handleSubmit = async (event) => {
    event.preventDefault()
    try {
        const response = await axios.post('/api/signin', {  
                email: email.value,
                password: password.value     
        },{
            timeout: 5000  // 5 second timeout
        })
        window.location.href = '/profile'  // Redirect on success
    }
    catch(err){
        const data = await response.json();
            if (response) {
            alert(data.message);
    }}
}
</script>

<template>
<body style="font-family: 'Poppins';">
    <main>
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a></div>
        <div id="box" class="bg-light text-dark" style="padding: 9.5% 4.75%;">
            <img src="../assets/images/login.svg" draggable="false" style="padding-left: 7%;">
            <div class="mainform">
                <h2>Welcome Back!</h2>
                <h6>Enter your Credentials to access your account</h6>
                <!--Form Fields-->
                <form @submit="handleSubmit">
                    <div class="form-group pt-2 pb-2">
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
                        Don't have an account? <a href="#">Sign Up</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    </main>
    <footer class="d-flex flex-wrap justify-content-between py-3 px-3 border-top fixed-bottom bg-body-tertiary">
        <div class="col-md-4 d-flex align-items-center">
          <a href="#" class="mb-3 me-2 mb-md-0 text-muted text-decoration-none lh-1">
            Frenzy
          </a>
          <span class="text-muted">© 2024 Frenzy, Inc</span>
        </div>
        <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-x-twitter"></i></a></li>
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-facebook"></i></a></li>
          <li class="ms-3"><a class="text-muted" href="#"><i class="fa-brands fa-square-instagram"></i></a></li>
        </ul>
    </footer>
</body>
</template>
