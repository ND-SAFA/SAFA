<template>
  <div>
    <v-lazy>
      <v-tabs v-model="model" class="width-fit">
        <v-tab v-for="{ name } in tabs" :key="name" class="primary lighten-5">
          <typography :value="name" />
        </v-tab>
      </v-tabs>
    </v-lazy>
    <v-tabs-items v-model="model" class="mt-1">
      <slot />
    </v-tabs-items>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { SelectOption } from "@/types";
import Typography from "../Typography.vue";

/**
 * Renders content across multiple tabs.
 * Use the `<v-tab-item/>` component to wrap each tab's child component.
 *
 * @emits-1 `input` (NUmber) - On tab change.
 */
export default Vue.extend({
  name: "TabList",
  components: { Typography },
  props: {
    value: Number,
    tabs: {
      type: Array as PropType<SelectOption[]>,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
    };
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
