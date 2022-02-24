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
              @selected="selectVersion"
              @unselected="unselectVersion"
            />
          </v-row>
        </v-container>
      </v-row>
    </template>
    <template v-slot:actions>
      <v-spacer />
      <v-btn @click="onSubmit" color="primary ">
        Save <v-icon id="upload-button">mdi-check</v-icon>
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectDelta, ProjectVersion } from "@/types";
import { getProjectDelta } from "@/api";
import { logModule, deltaModule, projectModule } from "@/store";
import { GenericModal } from "@/components/common";
import { VersionSelector } from "@/components/project";

/**
 * A modal for displaying delta versions.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
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
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;

      if (this.isInitialized) {
        this.onSubmit();
      } else {
        this.isInitialized = true;
      }
    },
    unselectVersion() {
      this.selectedVersion = undefined;
    },
    onSubmit() {
      if (this.selectedVersion === undefined) {
        logModule.onWarning("Please select a version to upload to");
      } else {
        const sourceVersion = this.project.projectVersion;

        if (sourceVersion !== undefined) {
          getProjectDelta(
            sourceVersion.versionId,
            this.selectedVersion.versionId
          ).then(async (deltaPayload: ProjectDelta) => {
            await projectModule.deleteArtifacts(
              Object.values(deltaModule.addedArtifacts)
            );

            await deltaModule.setDeltaPayload(deltaPayload);
            deltaModule.setAfterVersion(this.selectedVersion);
            this.$emit("close");
            logModule.onSuccess("Delta state was updated successfully.");
          });
        } else {
          logModule.onWarning("Project source version is not selected.");
        }
      }
    },
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.selectedVersion = undefined;
      this.isLoading = false;
      this.isInitialized = false;
    },
  },
});
</script>
