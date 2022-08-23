<template>
  <v-autocomplete
    chips
    deletable-chips
    :filled="filled"
    :multiple="multiple"
    :label="label"
    v-model="model"
    :items="artifacts"
    item-text="name"
    item-value="id"
    hide-details
    :filter="filterArtifacts"
    @keydown.enter="$emit('enter')"
  >
    <template v-slot:item="{ item, on, attrs }">
      <v-list-item v-on="on" v-bind="attrs" dense>
        <v-checkbox :value="isSelected(item)" />
        <generic-artifact-body-display display-title :artifact="item" />
      </v-list-item>
    </template>
    <template v-slot:selection="{ item, index }">
      <v-chip v-if="index < 3" outlined close @click:close="handleDelete(item)">
        <typography :value="item.name" />
      </v-chip>
      <typography
        v-else-if="index === 3"
        secondary
        x="2"
        :value="'+' + (selectedCount - 3)"
      />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel } from "@/types";
import { artifactStore } from "@/hooks";
import { filterArtifacts } from "@/util";
import { GenericArtifactBodyDisplay } from "@/components/common/generic";
import { Typography } from "@/components/common/display";

/**
 * An input for artifacts.
 *
 * @emits `input` (Artifact[]) - On input change.
 * @emits `enter` - On submit.
 */
export default Vue.extend({
  name: "ArtifactInput",
  components: {
    Typography,
    GenericArtifactBodyDisplay,
  },
  props: {
    value: {
      type: [Array, String] as PropType<string[] | string | undefined>,
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
    };
  },
  methods: {
    filterArtifacts,
    /**
     * Determines whether an artifact is in the selected state.
     *
     * @param item - The artifact to check.
     * @return Whether it is selected.
     */
    isSelected(item: ArtifactModel): boolean {
      if (typeof this.model === "string") {
        return item.id === this.model;
      } else if (Array.isArray(this.model)) {
        return this.model.includes(item.id);
      } else {
        return false;
      }
    },
    /**
     * Removes an artifact from the selection.
     *
     * @param item - The artifact to remove.
     */
    handleDelete(item: ArtifactModel): void {
      if (typeof this.model === "string") {
        this.model = "";
      } else if (Array.isArray(this.model)) {
        this.model = this.model.filter((id) => id !== item.id);
      }
    },
  },
  computed: {
    /**
     * @return The artifacts to select from.
     */
    artifacts(): ArtifactModel[] {
      return this.onlyDocumentArtifacts
        ? artifactStore.currentArtifacts
        : artifactStore.allArtifacts;
    },
    /**
     * @return The number of selected artifacts.
     */
    selectedCount(): number {
      if (typeof this.model === "string") {
        return 1;
      } else if (Array.isArray(this.model)) {
        return this.model.length;
      } else {
        return 0;
      }
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
