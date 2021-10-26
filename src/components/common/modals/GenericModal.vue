<template>
  <v-dialog :value="isOpen" :width="width" @click:outside="$emit('onClose')">
    <v-card height="500px">
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
import Vue from "vue";
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
    width: {
      type: Number,
      required: false,
      default: 700,
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
