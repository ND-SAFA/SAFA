import ArtifactView from "@/views/private/ArtifactView.vue";
import { shallowMount } from "@vue/test-utils";
import { expect } from "chai";

describe("Views will render", () => {
  it("ArtifactView.vue", () => {
    const wrapper = shallowMount(ArtifactView, {});
    expect(wrapper.text()).to.not.equal(null).and.not.equal(undefined);
  });
});
