<template>
  <v-flex class="d-flex flex-row align-center">
    <v-flex class="d-flex flex-row align-center">
      <safa-icon />
      <div>
        <h1 class="text-h5 white--text pl-4">SAFA</h1>
        <button-row :definitions="definitions" justify="start" />
      </div>
    </v-flex>

    <div class="mr-5">
      <version-label />
    </div>

    <account-dropdown />

    <upload-new-version-modal
      :is-open="uploadVersionOpen"
      @close="uploadVersionOpen = false"
    />
    <baseline-version-modal
      :is-open="openProjectOpen"
      @close="openProjectOpen = false"
    />
    <baseline-version-modal
      title="Change project version"
      :is-open="changeVersionOpen"
      :project="project"
      @close="changeVersionOpen = false"
    />
    <version-creator
      :is-open="createVersionOpen"
      :project="project"
      @close="createVersionOpen = false"
      @create="onVersionCreated"
    />
  </v-flex>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ButtonDefinition,
  ButtonMenuItem,
  ButtonType,
  EmptyLambda,
  ProjectIdentifier,
  ProjectVersion,
} from "@/types";
import { navigateTo, Routes } from "@/router";
import { logModule, projectModule } from "@/store";
import { clearProject, loadVersionIfExistsHandler } from "@/api";
import {
  BaselineVersionModal,
  ButtonRow,
  UploadNewVersionModal,
  SafaIcon,
} from "@/components/common";
import { VersionCreator } from "@/components/project";
import AccountDropdown from "./AccountDropdown.vue";
import VersionLabel from "./VersionLabel.vue";

export default Vue.extend({
  name: "AppBarHeader",
  components: {
    VersionLabel,
    AccountDropdown,
    SafaIcon,
    ButtonRow,
    UploadNewVersionModal,
    BaselineVersionModal,
    VersionCreator,
  },
  data() {
    return {
      openProjectOpen: false,
      uploadVersionOpen: false,
      changeVersionOpen: false,
      createVersionOpen: false,
    };
  },
  methods: {
    onOpenProject(): void {
      this.openProjectOpen = true;
    },
    async onCreateProject(): Promise<void> {
      await clearProject();
      await navigateTo(Routes.PROJECT_CREATOR);
    },
    onUploadVersion(): void {
      this.uploadVersionOpen = true;
    },
    onChangeVersion(): void {
      if (projectModule.versionId) {
        this.changeVersionOpen = true;
      } else {
        logModule.onWarning("Please select a project.");
      }
    },
    onCreateVersion(): void {
      if (projectModule.projectId) {
        this.createVersionOpen = true;
      } else {
        logModule.onWarning("Please select a project.");
      }
    },
    onVersionCreated(version: ProjectVersion) {
      loadVersionIfExistsHandler(version.versionId);

      this.createVersionOpen = false;
    },
  },
  computed: {
    project(): ProjectIdentifier {
      return projectModule.getProject;
    },
    projectMenuItems(): ButtonMenuItem[] {
      const options: ButtonMenuItem[] = [
        {
          name: "Open Project",
          tooltip: "Open another project",
          onClick: this.onOpenProject,
        },
        {
          name: "Create Project",
          tooltip: "Create a new project",
          onClick: this.onCreateProject,
        },
        {
          name: "Project Settings",
          tooltip: "Open this project's settings",
          onClick: () => navigateTo(Routes.PROJECT_SETTINGS),
        },
      ];

      return projectModule.projectId ? options : options.slice(0, -1);
    },
    definitions(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.LIST_MENU,
          label: "Project",
          buttonIsText: true,
          menuItems: this.projectMenuItems,
        },
        {
          isHidden: !this.$route.path.includes(Routes.ARTIFACT),
          type: ButtonType.LIST_MENU,
          label: "Version",
          buttonIsText: true,
          menuItems: [
            {
              name: "Change Version",
              tooltip: "Change to a different version of this project",
              onClick: this.onChangeVersion,
            },
            {
              name: "Create Version",
              tooltip: "Create a new version of this project",
              onClick: this.onCreateVersion,
            },
            {
              name: "Upload Flat Files",
              tooltip: "Upload project files in bulk",
              onClick: this.onUploadVersion,
            },
          ],
        },
        {
          isHidden: !this.$route.path.includes(Routes.ARTIFACT),
          type: ButtonType.LIST_MENU,
          label: "Trace Links",
          buttonIsText: true,
          menuItems: [
            {
              name: "Approve Generated Trace Links",
              tooltip: "Review automatically created graph links",
              onClick: () => navigateTo(Routes.TRACE_LINK),
            },
          ],
        },
      ];
    },
  },
});
</script>
