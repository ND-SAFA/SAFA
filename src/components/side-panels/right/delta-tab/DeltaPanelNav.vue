<template>
  <v-container>
    <v-row justify="center">
      <v-switch
        color="primary"
        @click="onSwitchChange"
        :value="isSwitchOn"
        :error-messages="errorMessage"
        readonly
      >
        <template v-slot:label>
          <span class="text-h5">Delta View Mode</span>
        </template>
      </v-switch>
    </v-row>
    <v-row justify="center" v-if="isDeltaViewEnabled">
      <v-btn
        v-if="isProjectDefined()"
        color="secondary"
        @click="isModalOpen = true"
        class="pt-6 pb-6"
      >
        <v-icon class="pr-2">mdi-source-branch</v-icon>
        Compare Against <br />
        {{ afterVersion }}
      </v-btn>
      <p v-else>No project has been selected.</p>
    </v-row>
    <DeltaVersionModal
      v-if="isProjectDefined()"
      :isOpen="isModalOpen"
      :project="project"
      @onClose="isModalOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import DeltaVersionModal from "@/components/side-panels/right/delta-tab/DeltaVersionsModal.vue";
import { Project } from "@/types";
import { versionToString } from "@/util";
import { deltaModule, projectModule } from "@/store";

export default Vue.extend({
  name: "left-panel-nav",
  components: {
    DeltaVersionModal,
  },
  data: () => ({
    isModalOpen: false,
    isSwitchOn: false,
    errorMessage: undefined as string | undefined,
  }),
  methods: {
    onSwitchChange() {
      if (this.isSwitchOn) {
        // always allow turn off
        deltaModule.setIsDeltaViewEnabled(false);
        this.isSwitchOn = false;
      } else {
        if (this.isProjectDefined()) {
          deltaModule.setIsDeltaViewEnabled(true);
          this.isSwitchOn = true;
        } else {
          this.errorMessage = "Please select a baseline project version";
          this.isSwitchOn = false;
        }
      }
    },
    isProjectDefined(): boolean {
      return this.project !== undefined && this.project.projectId !== "";
    },
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
    afterVersion(): string {
      return versionToString(deltaModule.getAfterVersion);
    },
    beforeVersion(): string {
      return versionToString(projectModule.getProject.projectVersion);
    },
    isDeltaViewEnabled(): boolean {
      return deltaModule.getIsDeltaViewEnabled;
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
