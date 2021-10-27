<template>
  <v-dialog
    :value="isOpen"
    :width="`${getWidth()}px`"
    @click:outside="$emit('onClose')"
  >
    <v-card :height="`${getHeight()}px`">
      <v-card-title class="grey lighten-2">
        <ModalTitle :title="title" @onClose="$emit('onClose')" />
      </v-card-title>

      <v-card-text>
        <slot name="body" />
      </v-card-text>

      <v-divider />
      <v-progress-linear v-if="isLoading" indeterminate color="secondary" />
      <v-card-actions
        v-if="actionsHeight > 0"
        class="grey lighten-1"
        dense
        :style="`height: ${actionsHeight}px`"
      >
        <slot name="actions" />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ModalTitle from "@/components/common/modals/ModalTitle.vue";
export default Vue.extend({
  components: {
    ModalTitle,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    actionsHeight: {
      type: Number,
      required: false,
      default: 75,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    size: {
      type: String as PropType<"xs" | "s" | "m" | "l">,
      required: false,
      default: "m",
    },
  },
  methods: {
    getHeight(): number {
      switch (this.size) {
        case "xs":
          return 200;
        case "s":
          return 300;
        case "m":
          return 500;
        case "l":
          return 600;
        default:
          return 400;
      }
    },
    getWidth(): number {
      switch (this.size) {
        case "xs":
          return 300;
        case "s":
          return 400;
        case "m":
          return 600;
        case "l":
          return 800;
        default:
          return 400;
      }
    },
  },
});
</script>

<style scoped>
html {
  overflow: hidden !important;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}
</style>
