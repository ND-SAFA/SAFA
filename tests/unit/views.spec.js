"use strict";
exports.__esModule = true;
var ArtifactView_vue_1 = require("@/views/private/ArtifactView.vue");
var test_utils_1 = require("@vue/test-utils");
var chai_1 = require("chai");
describe("Views will render", function () {
    it("ArtifactView.vue", function () {
        var wrapper = test_utils_1.shallowMount(ArtifactView_vue_1["default"], {});
        chai_1.expect(wrapper.text()).to.not.equal(null).and.not.equal(undefined);
    });
});
