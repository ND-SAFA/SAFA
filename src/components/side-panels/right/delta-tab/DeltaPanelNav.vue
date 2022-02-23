<template>
  <v-container>
    <h1 class="text-h4 my-2">Delta View</h1>
    <v-row justify="center">
      <v-switch
        color="primary"
        @click="onChange"
        :value="isDeltaViewEnabled"
        :error-messages="errorMessage"
        readonly
      >
        <template v-slot:label> Enable Delta View Mode </template>
      </v-switch>
    </v-row>
    <v-row justify="center" v-if="isDeltaViewEnabled">
      <v-btn
        v-if="isProjectDefined()"
        color="primary"
        @click="isModalOpen = true"
        class="pt-6 pb-6"
      >
        <v-icon class="pr-2">mdi-source-branch</v-icon>
        Compare Against <br />
        {{ afterVersion }}
      </v-btn>
      <p v-else>No project has been selected.</p>
    </v-row>
    <delta-versions-modal
      v-if="isProjectDefined()"
      :is-open="isModalOpen"
      :project="project"
      @close="isModalOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Project } from "@/types";
import { versionToString } from "@/util";
import { deltaModule, projectModule } from "@/store";
import DeltaVersionsModal from "./DeltaVersionsModal.vue";
import { reloadProject } from "@/api";

export default Vue.extend({
  name: "left-panel-nav",
  components: {
    DeltaVersionsModal,
  },
  data: () => ({
    isModalOpen: false,
    errorMessage: undefined as string | undefined,
  }),
  methods: {
    isProjectDefined(): boolean {
      return this.project.projectId !== "";
    },
    onChange(): void {
      if (!this.isDeltaViewEnabled) {
        if (this.isProjectDefined()) {
          deltaModule.setIsDeltaViewEnabled(true);
        } else {
          this.errorMessage = "Please select a baseline project version";
        }
      } else {
        deltaModule.setIsDeltaViewEnabled(false);
        reloadProject();
      }
    },
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
    afterVersion(): string {
      return versionToString(deltaModule.deltaVersion);
    },
    beforeVersion(): string {
      return versionToString(projectModule.getProject.projectVersion);
    },
    isDeltaViewEnabled(): boolean {
      return deltaModule.inDeltaView;
    },
  },
  watch: {
    project(): void {
      if (this.isProjectDefined()) {
        this.errorMessage = undefined;
      }
    },
  },
});
</script>
