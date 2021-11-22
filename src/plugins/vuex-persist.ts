import VuexPersistence from "vuex-persist";

export const vuexLocal = new VuexPersistence<any>({
  storage: window.localStorage,
});
