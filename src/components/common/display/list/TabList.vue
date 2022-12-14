<template>
  <div>
    <v-lazy>
      <flex-box class="width-fit" align="center">
        <v-tabs v-model="model" class="transparent-bg">
          <v-tab v-for="{ name } in tabs" :key="name" class="transparent-bg">
            <typography :value="name" />
          </v-tab>
        </v-tabs>
        <slot name="tabs" />
      </flex-box>
    </v-lazy>
    <v-tabs-items v-model="model" class="mt-1">
      <slot />
    </v-tabs-items>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { SelectOption } from "@/types";
import FlexBox from "@/components/common/layout/FlexBox.vue";
import Typography from "../Typography.vue";

/**
 * Renders content across multiple tabs.
 * Use the `<v-tab-item/>` component to wrap each tab's child component.
 *
 * @emits-1 `input` (NUmber) - On tab change.
 */
export default Vue.extend({
  name: "TabList",
  components: { FlexBox, Typography },
  props: {
    value: Number,
    tabs: {
      type: Array as PropType<SelectOption[]>,
      required: true,
    },
    background: {
      type: String as PropType<"outer" | "inner">,
      default: "outer",
    },
  },
  data() {
    return {
      model: this.value,
    };
  },
  computed: {
    /**
     * @return The class name for the tab header.
     */
    className(): string {
      return this.background === "inner" ? "neutral-bg" : "primary lighten-5";
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: number) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: number) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
