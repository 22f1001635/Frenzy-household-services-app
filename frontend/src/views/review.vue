<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import "@/assets/styles/main.css"
import "@/assets/styles/cart.css"

const route = useRoute();
const router = useRouter();
const rating = ref(0);
const comment = ref('');
const existingReview = ref(null);
const professionalName = ref('');

onMounted(async () => {
    window.dispatchEvent(new CustomEvent('vue-component-starsystem'));
    
    // Fetch existing review if request_id exists
    if (route.query.request_id) {
        try {
            // Fetch review data
            const reviewResponse = await fetch(`/api/reviews?request_id=${route.query.request_id}`);
            if (reviewResponse.ok) {
                const reviewData = await reviewResponse.json();
                if (reviewData.id) {
                    existingReview.value = reviewData;
                    rating.value = reviewData.rating;
                    comment.value = reviewData.comment || '';
                }
            }

            // Fetch professional name if available
            const requestResponse = await fetch(`/api/service-requests/${route.query.request_id}`);
            if (requestResponse.ok) {
                const requestData = await requestResponse.json();
                if (requestData.order?.professional_name) {
                    professionalName.value = requestData.order.professional_name;
                }
            }
        } catch (error) {
            console.error('Error fetching review data:', error);
        }
    }
});

const submitReview = async () => {
    try {
        const method = existingReview.value ? 'PUT' : 'POST';
        const url = existingReview.value 
            ? `/api/reviews/${existingReview.value.id}`
            : '/api/reviews';

        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                request_id: route.query.request_id,
                rating: rating.value,
                comment: comment.value
            })
        });

        if (response.ok) {
            router.push('/profile');
        } else {
            const errorData = await response.json();
            alert(errorData.error || 'Failed to submit review');
        }
    } catch (error) {
        console.log(request_id, rating, comment);
        console.error('Review submission error:', error);
        alert('An error occurred while submitting your review');
    }
};

const setRating = (value) => {
    rating.value = value;
    document.querySelectorAll('.star').forEach((star, index) => {
        star.classList.toggle('active', index < value);
    });
};
</script>

<template>
<body style="font-family: 'Poppins';">
  <main style="padding-top:2.75%;">
    <div id="forms" style="padding-top: 4%;">
        <div id="back"><a href="javascript:window.history.back()"><i class="fa-solid fa-circle-left" style="font-size:250%;"></i></a><p class="text-dark" id="head">Service Remarks</p></div>
        <div id="box" class="bg-light text-dark" style="padding-bottom: 2vw;">
            <div class="mainform3">
              <div class="cart">
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-lg-8">
                            <div class="form-container">
                                <p class="text-center request-id mb-4" style="margin-right: 3vw;">Request ID: {{ route.query.request_id }}</p>
                                <p v-if="professionalName" class="text-center mb-4">Professional: {{ professionalName }}</p>
                                <form @submit.prevent="submitReview">
                                    <div class="mb-0">
                                        <label class="form-label d-block">Service Rating (5 being the best):</label>
                                        <div class="star-rating">
                                            <input type="hidden" id="rating" name="rating" :value="rating" required>
                                            <div class="stars" style="margin-right: 3vw;">
                                              <i v-for="i in 5" :key="i" 
                                                 class="star fa-solid fa-star" 
                                                 :class="{ 'active': i <= rating }"
                                                 @click="setRating(i)"
                                                 :data-value="i"></i>
                                            </div>
                                            <div class="invalid-feedback">Please select a rating.</div>
                                        </div>
                                    </div>
                                    <div class="mb-1">
                                        <label class="form-label">Remarks (if any):</label>
                                        <textarea class="form-control" rows="3" v-model="comment"></textarea>
                                    </div>
                                    <div class="d-flex gap-3 justify-content-center py-2" style="margin-right: 3vw;">
                                        <button type="submit" class="btn btn-success">
                                            {{ existingReview ? 'Update' : 'Submit' }} Review
                                        </button>
                                        <button type="button" class="btn btn-secondary" @click="router.push('/profile')">Close</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
              </div>
            </div>
        </div>
    </div>
  </main>
</body>
</template>
