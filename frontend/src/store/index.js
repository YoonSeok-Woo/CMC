import { createStore } from "vuex";
import { userStore } from "@/store/modules/userStore.js";
import { scheduleStore } from "@/store/modules/scheduleStore.js";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  namespaced: true,
  modules: {
    userStore,
    scheduleStore,
  },
  state: {},
  mutations: {},
  actions: {},
  getters: {},
  plugins: [
    createPersistedState({
      storage: localStorage,
    }),
  ],
});
