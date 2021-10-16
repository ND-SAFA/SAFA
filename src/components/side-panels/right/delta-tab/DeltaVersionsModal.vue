<template>
  <GenericModal
    :isOpen="isOpen"
    :isLoading="isLoading"
    title="Delta View Target Version"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <v-row justify="center" class="mt-5">
        <v-container>
          <v-row justify="center">
            <h3 style="text-align: center" class="mt-3 mb-3">
              Select a Target Version
            </h3>
          </v-row>
          <v-row justify="center">
            <VersionSelector
              :project="project"
              :isOpen="isOpen"
              @onVersionSelected="selectVersion"
              @onVersionUnselected="unselectVersion"
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
  </GenericModal>
</template>

<script lang="ts">
import VersionSelector from "@/components/common/modals/VersionSelector.vue";
import { Project, ProjectVersion } from "@/types/domain/project";
import Vue, { PropType } from "vue";
import { getProjectDelta } from "@/api/project-api";
import { DeltaPayload } from "@/types/store";
import GenericModal from "@/components/common/modals/GenericModal.vue";
import { appModule, deltaModule } from "@/store";
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
        appModule.onWarning("Please select a version to upload to");
      } else {
        const sourceVersion = this.project.projectVersion;

        if (sourceVersion !== undefined) {
          getProjectDelta(
            sourceVersion.versionId,
            this.selectedVersion.versionId
          ).then((deltaPayload: DeltaPayload) => {
            deltaModule.setDeltaPayload(deltaPayload);
            deltaModule.setAfterVersion(this.selectedVersion);
            this.$emit("onClose");
            appModule.onSuccess("Delta state was updated successfully.");
          });
        } else {
          appModule.onError("Project source version is not selected.");
        }
      }
    },
  },
  mounted() {
    this.selectedVersion = undefined;
  },
});
</script>
