<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/sign.css"
import axios from 'axios'
import {ref} from 'vue'

const username=ref('')
const email=ref('')
const password=ref('')
const confirm_password=ref('')

const handleSubmit = async(event) => {
    event.preventDefault()
    try{
        const response=await axios.post('/api/signup',{
            email:email.value,
            username:username.value,
            password:password.value,
            confirm_password:confirm_password.value
        },{
            timeout:5000
        })
        alert('Account Created Successfully!')
        window.location.href = '/signin'
    }
    catch(err) {
        if (err.response && err.response.data) {
            alert(err.response.data.message || err.response.data.error)
        } else {
            alert('An error occurred during signup')
        }
        username.value = ''
        email.value = ''
        password.value = ''
        confirm_password.value = ''
    }
}

</script>

<template>
<body style="font-family: 'Poppins';">
    <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 3vw; padding-bottom: 6vw;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a></div>
        <div id="box" class="bg-light text-dark">
            <img src="../assets/images/login.svg" draggable="false">
            <div class="mainform2">
                <h3>Welcome New User!</h3>
                <h6>Enter your Information to make your account</h6>
                <!--Form Fields-->
                <form @submit="handleSubmit">
                    <div class="form-group pt-1 pb-2">
                        <label class="form-label">Full Name</label>
                        <input type="text" class="form-control" v-model="username" required>                    
                    </div>
                    <div class="form-group pb-2">
                        <label class="form-label">Email address</label>
                        <input type="email" class="form-control" aria-describedby="emailHelp" v-model="email" required>
                        <div id="emailHelp" class="opacity-25">We'll never share your email with anyone else.</div>                    
                    </div>
                    <div class="form-group pb-2">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" required>                    
                    </div>
                    <div class="form-group pb-2">
                        <label class="form-label">Confirm Password</label>
                        <input type="password" class="form-control" v-model="confirm_password" required>                    
                    </div>
                    <!--form submit button-->
                    <div class="form-group py-3 px-5">
                        <button type="submit" class="btn btn-primary col-12">Submit</button>
                    </div>
                </form>
                <div class="border-top pt-2">
                    <p class="text-dark-muted opacity-75">
                        Already have an account? <a href="#">Sign In</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    </main>
</body>
</template>