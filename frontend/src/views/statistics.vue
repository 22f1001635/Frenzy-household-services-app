<script setup>
import "@/assets/styles/main.css"
import "@/assets/styles/statistics.css"
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const store = useStore();
let chartInstance = ref(null);

// Common configuration
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' }
  }
};

// Destroy existing chart
const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
    chartInstance.value = null;
  }
};

// User Chart Data
const getUserChartData = (current, completed) => {
  const services = [...new Set([...current, ...completed].map(r => r.service_name))];
  return {
    labels: ['Current Requests', 'Completed Requests'],
    datasets: services.map(service => ({
      label: service,
      data: [
        current.filter(r => r.service_name === service).length,
        completed.filter(r => r.service_name === service).length
      ],
      backgroundColor: `hsl(${Math.random() * 360}, 55%, 60%)`
    }))
  };
};

// Professional Chart Data
const getProChartData = (current, completed) => ({
  labels: ['Requests'],
  datasets: [
    {
      label: 'Current',
      data: [current.length],
      backgroundColor: '#4CAF50'
    },
    {
      label: 'Completed',
      data: [completed.length],
      backgroundColor: '#2196F3'
    }
  ]
});

// Admin Chart Data
const getAdminChartData = (threeMonthData) => {
  const categories = [...new Set(threeMonthData.flatMap(m => m.data.map(d => d.service_name)))];
  return {
    labels: threeMonthData.map(m => m.month),
    datasets: categories.map(category => ({
      label: category,
      data: threeMonthData.map(month => 
        month.data.filter(d => d.service_name === category).length
      ),
      backgroundColor: `hsl(${Math.random() * 360}, 55%, 60%)`
    }))
  };
};

// Fetch data based on role
const fetchData = async () => {
  const role = store.state.user?.role;
  
  try {
    if (role === 'user') {
      const [current, completed] = await Promise.all([
        fetch('/api/user/current-requests').then(r => r.json()),
        fetch('/api/user/completed-requests').then(r => r.json())
      ]);
      return { type: 'user', data: { current, completed } };
    }

    if (role === 'professional') {
      const [current, completed] = await Promise.all([
        fetch('/api/professional/accepted-requests').then(r => r.json()),
        fetch('/api/professional/completed-requests').then(r => r.json())
      ]);
      return { type: 'pro', data: { current, completed } };
    }

    if (role === 'admin') {
      const [allRequests] = await Promise.all([
        fetch('/api/service-requests').then(r => r.json()) // CORRECT ENDPOINT
      ]);
      const completed = allRequests.filter(req => req.status === 'completed');
      
      // Get last 3 months data
      const months = Array.from({ length: 3 }, (_, i) => {
        const date = new Date();
        date.setMonth(date.getMonth() - i);
        return date;
      }).reverse();
      
      const threeMonthData = months.map(date => ({
        month: date.toLocaleString('default', { month: 'short' }),
        data: completed.filter(req => {
          const reqDate = new Date(req.completion_date);
          return (
            reqDate.getMonth() === date.getMonth() &&
            reqDate.getFullYear() === date.getFullYear()
          );
        })
      }));
      return { type: 'admin', data: threeMonthData };
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
};

// Initialize chart
const initChart = async () => {
  destroyChart();
  const ctx = document.getElementById('chartCanvas');
  if (!ctx) return;

  const roleData = await fetchData();
  if (!roleData) return;

  let config = null;
  
  switch (roleData.type) {
    case 'user':
      config = {
        type: 'bar',
        data: getUserChartData(roleData.data.current, roleData.data.completed),
        options: { ...chartOptions, scales: { x: { stacked: true }, y: { stacked: true } } }
      };
      break;

    case 'pro':
      config = {
        type: 'bar',
        data: getProChartData(roleData.data.current, roleData.data.completed),
        options: chartOptions
      };
      break;

    case 'admin':
      config = {
        type: 'bar',
        data: getAdminChartData(roleData.data),
        options: { ...chartOptions, scales: { x: { stacked: true }, y: { stacked: true } } }
      };
      break;
  }

  if (config) {
    chartInstance.value = new Chart(ctx, config);
  }
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', initChart);
});
</script>

<template>
    <body style="font-family: 'Poppins';">
      <main style="padding-top:2.75%;">
        <div id="graph1">
            <canvas id="chartCanvas"></canvas>
        </div>
        <div id="graph2"></div>
        <div id="graph3"></div>
      </main>
    </body>
</template>
