<template>
  <flex-box align="center">
    <flex-box full-width align="center">
      <safa-icon />
      <typography el="h1" variant="large" l="4" color="white" value="SAFA" />
      <button-row :definitions="definitions" class="mx-3" />
      <saving-icon />
    </flex-box>

    <div class="mr-5">
      <version-label />
    </div>

    <account-dropdown />

    <upload-new-version-modal
      :is-open="uploadVersionOpen"
      @close="uploadVersionOpen = false"
    />
    <baseline-version-modal
      data-cy="modal-project-select"
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
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ButtonDefinition,
  ButtonMenuItem,
  ButtonType,
  VersionModel,
} from "@/types";
import { getParams, navigateTo, Routes } from "@/router";
import { logStore, projectStore } from "@/hooks";
import { handleLoadVersion } from "@/api";
import { ButtonRow, SafaIcon, Typography, FlexBox } from "@/components/common";
import {
  VersionCreator,
  BaselineVersionModal,
  UploadNewVersionModal,
} from "@/components/project";
import AccountDropdown from "./AccountDropdown.vue";
import VersionLabel from "./VersionLabel.vue";
import SavingIcon from "./SavingIcon.vue";

export default Vue.extend({
  name: "AppBarHeader",
  components: {
    FlexBox,
    Typography,
    VersionLabel,
    AccountDropdown,
    SafaIcon,
    ButtonRow,
    UploadNewVersionModal,
    BaselineVersionModal,
    VersionCreator,
    SavingIcon,
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
      return projectStore.project;
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
          name: "Project Uploads",
          tooltip: "View recent and in-progress uploads",
          onClick: () => navigateTo(Routes.UPLOAD_STATUS),
        },
        {
          name: "Project Settings",
          tooltip: "View this project's settings",
          onClick: () => navigateTo(Routes.PROJECT_SETTINGS, getParams()),
        },
      ];

      return projectStore.projectId ? options : options.slice(0, -1);
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
          dataCy: "button-nav-project",
          menuItems: this.projectMenuItems,
        },
        {
          isHidden: !this.$route.path.includes(Routes.ARTIFACT),
          type: ButtonType.LIST_MENU,
          label: "Version",
          buttonIsText: true,
          dataCy: "button-nav-version",
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
          dataCy: "button-nav-links",
          menuItems: [
            {
              name: "Approve Generated Trace Links",
              tooltip: "Review automatically created graph links",
              onClick: () => navigateTo(Routes.TRACE_LINK, getParams()),
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
      if (projectStore.versionId) {
        this.changeVersionOpen = true;
      } else {
        logStore.onWarning("Please select a project.");
      }
    },
    /**
     * Opens the project version creator.
     */
    handleCreateVersion(): void {
      if (projectStore.projectId) {
        this.createVersionOpen = true;
      } else {
        logStore.onWarning("Please select a project.");
      }
    },
    /**
     * Closes the version creator and loads the created version.
     */
    handleVersionCreated(version: VersionModel) {
      handleLoadVersion(version.versionId);

      this.createVersionOpen = false;
    },
  },
});
</script>
