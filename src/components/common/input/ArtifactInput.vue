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
    <template v-slot:item="{ item }">
      <generic-artifact-body-display display-title :artifact="item" />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel } from "@/types";
import { artifactModule } from "@/store";
import { GenericArtifactBodyDisplay } from "@/components/common/generic";
import { filterArtifacts } from "@/util";

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
  },
  computed: {
    /**
     * @return The artifacts to select from.
     */
    artifacts(): ArtifactModel[] {
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
