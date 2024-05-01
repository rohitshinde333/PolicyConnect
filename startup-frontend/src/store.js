import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state() {
    return {
      accessToken: null, // Initial state for the access token
      is_admin: null,
      is_theater_admin: null,
      theatre_id: null,
    };
  },
  mutations: {
    SET_ACCESS_TOKEN(state, token) {
      state.accessToken = token;
    },
    SET_IS_ADMIN(state, is_admin) {
      state.is_admin = is_admin;
    },
    SET_IS_THEATER_ADMIN(state, is_theater_admin) {
      state.is_theater_admin = is_theater_admin;
    },
    SET_THEATRE_ID(state, theatre_id) {
      state.theatre_id = theatre_id;
    },
    CLEAR_ACCESS_TOKEN(state) {
      state.accessToken = null;
    }
  },
  actions: {
    
    setAccessToken({ commit }, { token }) {
      commit('SET_ACCESS_TOKEN', token);
    },
    setIsAdmin({ commit }, { is_admin }) {
      commit('SET_IS_ADMIN', is_admin);
    },
    setIsTheaterAdmin({ commit }, { is_theater_admin }) {
      commit('SET_IS_THEATER_ADMIN', is_theater_admin);
    },
    setTheatreId({commit}, {theatre_id}){
      commit('SET_THEATRE_ID', theatre_id);
    },
    clearAccessToken({ commit }) {
      commit('CLEAR_ACCESS_TOKEN');
    }
  },
  getters: {
    accessToken(state) {
      return state.accessToken;
    },
    isAdmin(state) {
      return state.is_admin;
    },
    isTheaterAdmin(state) {
      return state.is_theater_admin;
    },
    theatre_id(state){
      return state.theatre_id;
    }
  }
});

export default store;
