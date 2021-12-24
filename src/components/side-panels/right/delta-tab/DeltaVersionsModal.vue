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
      <v-container class="ma-0 pa-0">
        <v-row justify="center" class="ma-10">
          <v-btn @click="onSubmit" color="primary ">
            Save <v-icon id="upload-button">mdi-check</v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Project, ProjectDelta, ProjectVersion } from "@/types";
import { getProjectDelta } from "@/api";
import { logModule, deltaModule, viewportModule } from "@/store";
import { GenericModal } from "@/components/common";
import { VersionSelector } from "@/components/project/version-selector";

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
    };
  },
  methods: {
    selectVersion(version: ProjectVersion) {
      this.selectedVersion = version;
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
            await deltaModule.setDeltaPayload(deltaPayload);
            deltaModule.setAfterVersion(this.selectedVersion);
            this.$emit("close");
            logModule.onSuccess("Delta state was updated successfully.");
            await viewportModule.setArtifactTreeLayout();
          });
        } else {
          logModule.onWarning("Project source version is not selected.");
        }
      }
    },
  },
  mounted() {
    this.selectedVersion = undefined;
  },
});
</script>
