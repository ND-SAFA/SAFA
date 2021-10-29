<template>
  <GenericModal
    :isOpen="isOpen"
    size="s"
    title="Create Artifact Type"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <v-text-field v-model="artifactName" label="Artifact Name" required />
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn @click="onSubmit" fab color="secondary">
            <v-icon> mdi-content-save </v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue from "vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";

export default Vue.extend({
  components: {
    GenericModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      artifactName: "",
    };
  },
  methods: {
    onSubmit() {
      this.$emit("onSubmit", this.artifactName);
      this.$emit("onClose");
    },
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.artifactName = "";
      }
    },
  },
});
</script>
