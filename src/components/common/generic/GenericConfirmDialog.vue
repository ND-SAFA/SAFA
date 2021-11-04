<template>
  <GenericModal
    size="xs"
    :isOpen="isOpen"
    :title="title"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>{{ body }}</template>
    <template v-slot:actions>
      <v-row justify="center">
        <v-btn outlined text color="primary" @click="onConfirm">
          I accept
        </v-btn>
      </v-row>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue from "vue";
import GenericModal from "./GenericModal.vue";
export default Vue.extend({
  components: { GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    body: {
      type: String,
      required: true,
    },
    width: {
      type: String,
      required: false,
      default: "500",
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    onConfirm(): void {
      this.$emit("onClose");
      this.$emit("onSubmit");
    },
  },
});
</script>
