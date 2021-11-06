<template>
  <v-btn small fab :color="titleColor" @click="$emit('onClick', name)">
    {{ name }}
  </v-btn>
</template>

<script lang="ts">
import { DeltaType } from "@/types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  props: {
    name: {
      type: String,
      required: true,
    },
    deltaType: {
      type: String as PropType<DeltaType>,
      required: true,
    },
  },
  computed: {
    titleColor(): string {
      switch (this.deltaType) {
        case "added":
          return "success";
        case "modified":
          return "info";
        case "removed":
          return "error";
        default:
          return "black";
      }
    },
  },
});
</script>
