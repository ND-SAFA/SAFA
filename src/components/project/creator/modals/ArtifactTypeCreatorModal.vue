<template>
  <GenericModal
    :isOpen="isOpen"
    size="s"
    title="Create Artifact Type"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <v-text-field
        v-model="artifactName"
        label="Artifact Name"
        required
        :error-messages="errors"
        @keydown.enter="onEnterPress"
      />
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
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/modal/GenericModal.vue";

export default Vue.extend({
  components: {
    GenericModal,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    artifactTypes: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  data() {
    return {
      artifactName: "",
      errors: [] as string[],
    };
  },
  methods: {
    onSubmit() {
      if (this.artifactName === "")
        this.errors = ["Artifact type cannot be empty."];
      else if (this.artifactTypes.includes(this.artifactName))
        this.errors = [`Artifact type has already been created.`];
      else this.errors = [];
      if (this.errors.length === 0) {
        this.$emit("onSubmit", this.artifactName);
        this.$emit("onClose");
      }
    },
    onEnterPress(event: Event): void {
      event.preventDefault();
      this.onSubmit();
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
