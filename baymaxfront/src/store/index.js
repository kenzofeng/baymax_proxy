import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    project: ''
  },
  getters: {
    getproject (state) {
      return state.project
    }
  },
  actions: {
    setProjectName ({commit, state}, name) {
      commit('setProject', name)
    }
  },
  mutations: {
    setProject (state, name) {
      state.project = name//
    }
  }
})

export default store
