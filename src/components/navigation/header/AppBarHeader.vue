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
      @create="handleVersionCreated"
    />
  </v-flex>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ButtonDefinition,
  ButtonMenuItem,
  ButtonType,
  ProjectVersion,
} from "@/types";
import { navigateTo, Routes } from "@/router";
import { logModule, projectModule } from "@/store";
import { handleLoadVersion } from "@/api";
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
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectModule.getProject;
    },
    /**
     * @return The menu items for projects.
     */
    projectMenuItems(): ButtonMenuItem[] {
      const options: ButtonMenuItem[] = [
        {
          name: "Open Project",
          tooltip: "Open another project",
          onClick: this.handleOpenProject,
        },
        {
          name: "Create Project",
          tooltip: "Create a new project",
          onClick: this.handleCreateProject,
        },
        {
          name: "Project Settings",
          tooltip: "View this project's settings",
          onClick: () => navigateTo(Routes.PROJECT_SETTINGS),
        },
      ];

      return projectModule.projectId ? options : options.slice(0, -1);
    },
    /**
     * @return The dropdown menus displayed on the nav bar.
     */
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
              onClick: this.handleChangeVersion,
            },
            {
              name: "Create Version",
              tooltip: "Create a new version of this project",
              onClick: this.handleCreateVersion,
            },
            {
              name: "Upload Flat Files",
              tooltip: "Upload project files in bulk",
              onClick: this.handleUploadVersion,
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
  methods: {
    /**
     * Opens the project selector.
     */
    handleOpenProject(): void {
      this.openProjectOpen = true;
    },
    /**
     * Navigates to the create project page.
     */
    async handleCreateProject(): Promise<void> {
      await navigateTo(Routes.PROJECT_CREATOR);
    },
    /**
     * Opens the project version uploader.
     */
    handleUploadVersion(): void {
      this.uploadVersionOpen = true;
    },
    /**
     * Opens the project version selector.
     */
    handleChangeVersion(): void {
      if (projectModule.versionId) {
        this.changeVersionOpen = true;
      } else {
        logModule.onWarning("Please select a project.");
      }
    },
    /**
     * Opens the project version creator.
     */
    handleCreateVersion(): void {
      if (projectModule.projectId) {
        this.createVersionOpen = true;
      } else {
        logModule.onWarning("Please select a project.");
      }
    },
    /**
     * Closes the version creator and loads the created version.
     */
    handleVersionCreated(version: ProjectVersion) {
      handleLoadVersion(version.versionId);

      this.createVersionOpen = false;
    },
  },
});
</script>
