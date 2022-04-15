<template>
  <generic-modal
    title="Delta View Target Version"
    :is-open="isOpen"
    :is-loading="isLoading"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <v-row justify="center" class="mt-5">
        <v-container>
          <v-row justify="center">
            <span class="text-body-1 mt-3 mb-3 text-center">
              Select a Target Version
            </span>
          </v-row>
          <v-row justify="center">
            <version-selector
              hide-current-version
              :project="project"
              :is-open="isOpen"
              @selected="handleSelectVersion"
              @unselected="handleDeselectVersion"
            />
          </v-row>
        </v-container>
      </v-row>
    </template>
    <template v-slot:actions>
      <v-spacer />
      <v-btn @click="handleSubmit" color="primary "> Save </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectVersion } from "@/types";
import { logModule } from "@/store";
import { GenericModal } from "@/components/common";
import { VersionSelector } from "@/components/project";
import { handleSetProjectDelta } from "@/api/handlers/delta-handler";

/**
 * A modal for displaying delta versions.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "DeltaVersionsModal",
  components: { VersionSelector, GenericModal },
  props: {
    isOpen: Boolean,
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
  data() {
    return {
      selectedVersion: undefined as ProjectVersion | undefined,
      isLoading: false,
      isInitialized: false,
    };
  },
  methods: {
    /**
     * Selects a delta version.
     * @param version - The version to select.
     */
    handleSelectVersion(version: ProjectVersion) {
      this.selectedVersion = version;

      if (this.isInitialized) {
        this.handleSubmit();
      } else {
        this.isInitialized = true;
      }
    },
    /**
     * Deselects a delta version.
     */
    handleDeselectVersion() {
      this.selectedVersion = undefined;
    },
    /**
     * Attempts to load a project delta.
     */
    handleSubmit() {
      if (!this.selectedVersion) {
        logModule.onWarning("Please select a version to upload to");
      } else if (!this.project.projectVersion) {
        logModule.onWarning("Project source version is not selected.");
      } else {
        handleSetProjectDelta(
          this.project.projectVersion,
          this.selectedVersion,
          () => this.$emit("close")
        );
      }
    },
  },
  watch: {
    /**
     * Resets modal state when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.selectedVersion = undefined;
      this.isLoading = false;
      this.isInitialized = false;
    },
  },
});
</script>
