<template>
  <v-autocomplete
    filled
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
      <generic-artifact-body-display
        :body="item.body"
        :title="getTitle(item)"
      />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact } from "@/types";
import { artifactModule } from "@/store";
import { getArtifactTypePrintName } from "@/util";
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
      type: [Array, String],
      required: true,
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
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  methods: {
    /**
     * Converts the type name to title case.
     * @param type - The type to convert.
     * @return The title case type name.
     */
    getTypePrintName: getArtifactTypePrintName,
    /**
     * Decides whether to filter an artifact out of view.
     * @param artifact - The artifact to check.
     * @param queryText - The current query text.
     * @return If true, the artifact should be kept.
     */
    filter(artifact: Artifact, queryText: string): boolean {
      const lowercaseQuery = queryText.toLowerCase();
      const { name, type } = artifact;

      if (this.value.includes(artifact.id)) return false;

      return (
        name.toLowerCase().includes(lowercaseQuery) ||
        type.toLowerCase().includes(lowercaseQuery) ||
        this.getTypePrintName(type).toLowerCase().includes(lowercaseQuery)
      );
    },
    /**
     * Returns whether the artifact has its display expanded.
     * @param artifact - The artifact to check.
     * @return Whether its display is expanded.
     */
    getTitle(artifact: Artifact): string {
      return `${this.getTypePrintName(artifact.type)} - ${artifact.name}`;
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
    value(currentValue: string[] | string) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string[] | string) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
