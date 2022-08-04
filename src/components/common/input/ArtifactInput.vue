<template>
  <v-autocomplete
    :filled="filled"
    chips
    :multiple="multiple"
    deletable-chips
    :label="label"
    v-model="model"
    :items="artifacts"
    item-text="name"
    item-value="id"
    :filter="filter"
    @keydown.enter="$emit('enter')"
  >
    <template v-slot:item="{ item }">
      <generic-artifact-body-display display-title :artifact="item" />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact } from "@/types";
import { artifactModule } from "@/store";
import { GenericArtifactBodyDisplay } from "@/components/common/generic";

/**
 * An input for artifacts.
 *
 * @emits `input` (Artifact[]) - On input change.
 * @emits `enter` - On submit.
 */
export default Vue.extend({
  name: "ArtifactInput",
  components: {
    GenericArtifactBodyDisplay,
  },
  props: {
    value: {
      type: Array as PropType<string[] | string | undefined>,
      required: false,
    },
    multiple: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      default: "Visible Artifacts",
    },
    onlyDocumentArtifacts: {
      type: Boolean,
      default: false,
    },
    filled: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  methods: {
    /**
     * Decides whether to filter an artifact out of view.
     * @param artifact - The artifact to check.
     * @param queryText - The current query text.
     * @return If true, the artifact should be kept.
     */
    filter(artifact: Artifact, queryText: string): boolean {
      const lowercaseQuery = queryText.toLowerCase();
      const { name, type } = artifact;

      if (this.value?.includes(artifact.id)) return false;

      return (
        name.toLowerCase().includes(lowercaseQuery) ||
        type.toLowerCase().includes(lowercaseQuery) ||
        type.toLowerCase().includes(lowercaseQuery)
      );
    },
  },
  computed: {
    /**
     * @return The artifacts to select from.
     */
    artifacts(): Artifact[] {
      return this.onlyDocumentArtifacts
        ? artifactModule.artifacts
        : artifactModule.allArtifacts;
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: string[] | string | undefined) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string[] | string | undefined) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
