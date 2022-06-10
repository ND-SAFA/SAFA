import store from "@/store";
import { SnackbarMessage } from "@/types/store/snackbar";
import { expect } from "chai";

const snackMessage = "hello world";

describe("Vuex store", () => {
  it("snackbar message - get/set", () => {
    //VP 1: begins with no message
    let appErrorMessage: SnackbarMessage = store.getters["snackbar/getMessage"];

    expect(appErrorMessage.message).to.equal("");

    store.dispatch("snackbar/onInfo", snackMessage);

    //VP 2: Able to set message
    appErrorMessage = store.getters["snackbar/getMessage"];

    expect(appErrorMessage.message).to.equal(snackMessage);

    store.dispatch("snackbar/onInfo", "");
  });

  it("onError", () => {
    //VP 1: begins with no message
    let appErrorMessage: SnackbarMessage = store.getters["snackbar/getMessage"];

    expect(appErrorMessage.message).to.equal("");

    store.dispatch("snackbar/onError", snackMessage);

    //VP 2: Able to set message
    appErrorMessage = store.getters["snackbar/getMessage"];

    expect(appErrorMessage.message).to.equal(snackMessage);

    store.dispatch("snackbar/onInfo", "");
  });
});
