<template>
  <flex-box align="center">
    <flex-box full-width align="center">
      <safa-icon
        style="width: 200px; cursor: pointer"
        @click="handleLogoClick"
      />
      <button-row :definitions="definitions" class="mx-3" />
      <saving-icon />
      <update-button />
    </flex-box>

    <div class="mr-2">
      <version-label />
    </div>

    <notifications />

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
    <trace-link-generator-modal />
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
import { appStore, projectStore, sessionStore } from "@/hooks";
import {
  getParams,
  navigateTo,
  Routes,
  routesWithRequiredProject,
} from "@/router";
import { handleLoadVersion } from "@/api";
import { ButtonRow, SafaIcon, FlexBox } from "@/components/common";
import {
  VersionCreator,
  BaselineVersionModal,
  UploadNewVersionModal,
} from "@/components/project";
import { TraceLinkGeneratorModal } from "@/components/trace-link";
import SavingIcon from "./SavingIcon.vue";
import VersionLabel from "./VersionLabel.vue";
import AccountDropdown from "./AccountDropdown.vue";
import UpdateButton from "./UpdateButton.vue";
import Notifications from "./Notifications.vue";

export default Vue.extend({
  name: "AppBarHeader",
  components: {
    Notifications,
    TraceLinkGeneratorModal,
    UpdateButton,
    FlexBox,
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
     * @return Whether the current user is an editor of the current project.
     */
    isEditor(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
    /**
     * @return The menu items for projects.
     */
    projectMenuItems(): ButtonMenuItem[] {
      const options: ButtonMenuItem[] = [
        {
          name: "Open Project",
          tooltip: "Open another project",
          onClick: () => (this.openProjectOpen = true),
        },
        {
          name: "Create Project",
          tooltip: "Create a new project",
          onClick: () => navigateTo(Routes.PROJECT_CREATOR),
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
     * @return The menu items for versions.
     */
    versionMenuItems(): ButtonMenuItem[] {
      const options: ButtonMenuItem[] = [
        {
          name: "Change Version",
          tooltip: "Change to a different version of this project",
          onClick: () =>
            projectStore.ifProjectDefined(
              () => (this.changeVersionOpen = true)
            ),
        },
        {
          name: "Create Version",
          tooltip: "Create a new version of this project",
          onClick: () =>
            projectStore.ifProjectDefined(
              () => (this.createVersionOpen = true)
            ),
        },
        {
          name: "Upload Flat Files",
          tooltip: "Upload project files in bulk",
          onClick: () =>
            projectStore.ifProjectDefined(
              () => (this.uploadVersionOpen = true)
            ),
        },
      ];

      return this.isEditor ? options : [options[0]];
    },
    /**
     * @return The menu items for links.
     */
    linkMenuItems(): ButtonMenuItem[] {
      return [
        {
          name: "Project Models",
          tooltip: "View this project's models",
          onClick: () => navigateTo(Routes.PROJECT_MODELS, getParams()),
        },
        {
          name: "Train Models",
          tooltip: "Train your project's models to improve their performance.",
          onClick: () => appStore.openTraceLinkGenerator("train"),
        },
        {
          name: "Generate New Trace Links",
          tooltip: "Generate new trace links within the current project view",
          onClick: () => appStore.openTraceLinkGenerator("generate"),
        },
        {
          name: "Approve Generated Trace Links",
          tooltip: "Review automatically created graph links",
          onClick: () => navigateTo(Routes.TRACE_LINK, getParams()),
        },
      ];
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
          isHidden: !routesWithRequiredProject.includes(this.$route.path),
          type: ButtonType.LIST_MENU,
          label: "Version",
          buttonIsText: true,
          dataCy: "button-nav-version",
          menuItems: this.versionMenuItems,
        },
        {
          isHidden:
            !routesWithRequiredProject.includes(this.$route.path) ||
            !this.isEditor,
          type: ButtonType.LIST_MENU,
          label: "Trace Links",
          buttonIsText: true,
          dataCy: "button-nav-links",
          menuItems: this.linkMenuItems,
        },
      ];
    },
  },
  methods: {
    /**
    /**
     * Closes the version creator and loads the created version.
     */
    handleVersionCreated(version: VersionModel) {
      handleLoadVersion(version.versionId);

      this.createVersionOpen = false;
    },
    /**
     * Navigates to the project creator when the logo is clicked.
     */
    handleLogoClick() {
      navigateTo(Routes.HOME);
    },
  },
});
</script>
