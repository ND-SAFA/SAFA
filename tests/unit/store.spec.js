"use strict";
exports.__esModule = true;
var store_1 = require("@/store");
var chai_1 = require("chai");
var snackMessage = "hello world";
describe("Vuex store", function () {
    it("snackbar message - get/set", function () {
        //VP 1: begins with no message
        var appErrorMessage = store_1["default"].getters["snackbar/getMessage"];
        chai_1.expect(appErrorMessage.message).to.equal("");
        store_1["default"].dispatch("snackbar/onInfo", snackMessage);
        //VP 2: Able to set message
        appErrorMessage = store_1["default"].getters["snackbar/getMessage"];
        chai_1.expect(appErrorMessage.message).to.equal(snackMessage);
        store_1["default"].dispatch("snackbar/onInfo", "");
    });
    it("onError", function () {
        //VP 1: begins with no message
        var appErrorMessage = store_1["default"].getters["snackbar/getMessage"];
        chai_1.expect(appErrorMessage.message).to.equal("");
        store_1["default"].dispatch("snackbar/onError", snackMessage);
        //VP 2: Able to set message
        appErrorMessage = store_1["default"].getters["snackbar/getMessage"];
        chai_1.expect(appErrorMessage.message).to.equal(snackMessage);
        store_1["default"].dispatch("snackbar/onInfo", "");
    });
});
