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
      <v-list-item-content style="max-width: 500px">
        <v-list-item-title
          v-html="`${getTypePrintName(item.type)} - ${item.name}`"
        />
        <v-list-item-subtitle v-if="!isExpanded(item)" v-html="item.body" />
        <v-list-item-content v-if="isExpanded(item)" v-html="item.body" />
        <v-list-item-action class="ma-0">
          <v-spacer />
          <v-btn text small @click.stop="handleSeeMore(item)">
            {{ isExpanded(item) ? "See Less" : "See More" }}
          </v-btn>
        </v-list-item-action>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact } from "@/types";
import { artifactModule } from "@/store";
import { getArtifactTypePrintName } from "@/util";

/**
 * An input for artifacts.
 *
 * @emits `input` (Artifact[]) - On input change.
 * @emits `enter` - On submit.
 */
export default Vue.extend({
  name: "ArtifactInput",
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
      expandedId: "",
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

      return (
        name.toLowerCase().includes(lowercaseQuery) ||
        type.toLowerCase().includes(lowercaseQuery) ||
        this.getTypePrintName(type).toLowerCase().includes(lowercaseQuery)
      );
    },
    /**
     * Opens up the expanded display for an artifact.
     * @param artifact - The artifact to view.
     */
    handleSeeMore(artifact: Artifact) {
      this.expandedId = artifact.id === this.expandedId ? "" : artifact.id;
    },
    /**
     * Returns whether the artifact has its display expanded.
     * @param artifact - The artifact to check.
     * @return Whether its display is expanded.
     */
    isExpanded(artifact: Artifact): boolean {
      return artifact.id === this.expandedId;
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
