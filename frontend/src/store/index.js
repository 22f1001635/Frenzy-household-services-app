import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    logout(state) {
      state.user = null;
    },
  },
  actions: {
    async fetchUser({ commit }) {
      try {
        const response = await fetch('/api/current_user');
        if (response.status === 401) {
          commit('setUser', null);
          return;
        }
        const data = await response.json();
        commit('setUser', data.user);
      } catch (error) {
        console.error('Error fetching user:', error);
        commit('setUser', null);
      }
    },
    async logout({ commit }) {
      try {
        await fetch('/api/logout');
        commit('logout');
        alert('You have been logged out');
      } catch (error) {
        console.error('Error during logout:', error);
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    isAdmin: state => state.user?.role === 'admin',
    currentUser: state => state.user,
    userImage: state => state.user?.image_file
      ? `http://localhost:5000/profile_pictures/${state.user.image_file}`
      : `http://localhost:5000/profile_pictures/profile.png`
  },
});