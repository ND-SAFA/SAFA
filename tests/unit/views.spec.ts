import Home from "@/views/ArtifactTreeView.vue";
import { shallowMount } from "@vue/test-utils";
import { expect } from "chai";

describe("Views will render", () => {
  it("Home.vue", () => {
    const wrapper = shallowMount(Home, {});
    expect(wrapper.text()).to.not.equal(null).and.not.equal(undefined);
  });
});
