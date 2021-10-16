import store from "@/store";
import { SnackbarMessage } from "@/types/store";
import { expect } from "chai";

describe("Vuex store", () => {
  it("snackbar message - get/set", () => {
    //VP 1: begins with no message
    let appErrorMessage: string = store.getters["app/getMessage"];
    expect(appErrorMessage).to.equal("");

    const snackMessage = "hello world";
    store.commit("app/setMessage", snackMessage);

    //VP 2: Able to set mesage
    appErrorMessage = store.getters["app/getMessage"];
    expect(appErrorMessage).to.equal(snackMessage);
    store.commit("app/clearMessage");
  });

  it("onError", () => {
    //VP 1: begins with no message
    let appErrorMessage: SnackbarMessage | undefined =
      store.getters["app/getMessage"];
    expect(appErrorMessage).to.equal(undefined);

    const errorMessage = "hello world";
    store.dispatch("app/onError", errorMessage);

    //VP 2: Able to set mesage
    appErrorMessage = store.getters["app/getMessage"];
    expect(appErrorMessage).to.not.equal(undefined);
    expect((appErrorMessage as SnackbarMessage).message).to.equal(errorMessage);
    store.commit("app/clearMessage");
  });
});
