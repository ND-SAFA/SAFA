<template>
  <v-autocomplete
    chips
    deletable-chips
    ref="projectInput"
    filled
    :multiple="multiple"
    label="My Projects"
    v-model="model"
    :items="projects"
    item-text="name"
    item-value="projectId"
    @keydown.enter="$emit('enter')"
  >
    <template v-slot:append>
      <icon-button
        small
        icon-id="mdi-content-save-outline"
        tooltip="Save Projects"
        data-cy="button-save-artifacts"
        @click="handleClose"
      />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { IdentifierSchema } from "@/types";
import { projectStore } from "@/hooks";
import { IconButton } from "@/components/common/button";

/**
 * An input for projects.
 *
 * @emits-1 `input` (string[] | string | undefined) - On value change.
 */
export default Vue.extend({
  name: "ProjectInput",
  components: {
    IconButton,
  },
  props: {
    value: {
      type: [Array, String] as PropType<string[] | string | undefined>,
      required: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    excludeCurrentProject: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      model: this.value,
    };
  },
  computed: {
    /**
     * @return All projects for the current user.
     */
    projects(): IdentifierSchema[] {
      return this.excludeCurrentProject
        ? projectStore.unloadedProjects
        : projectStore.allProjects;
    },
  },
  methods: {
    /**
     * Closes the selection window.
     */
    handleClose(): void {
      (this.$refs.projectInput as HTMLElement).blur();
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
