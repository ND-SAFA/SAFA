<template>
  <flex-box align="center">
    <flex-box full-width align="center">
      <safa-icon />
      <typography el="h1" variant="large" l="4" color="white" value="SAFA" />
      <button-row :definitions="definitions" class="mx-3" />
      <saving-icon />
      <update-button />
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
import { appStore, projectStore } from "@/hooks";
import {
  getParams,
  navigateTo,
  Routes,
  routesWithRequiredProject,
} from "@/router";
import { handleLoadVersion } from "@/api";
import { ButtonRow, SafaIcon, Typography, FlexBox } from "@/components/common";
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

export default Vue.extend({
  name: "AppBarHeader",
  components: {
    TraceLinkGeneratorModal,
    UpdateButton,
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
      return [
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
    },
    /**
     * @return The menu items for links.
     */
    linkMenuItems(): ButtonMenuItem[] {
      return [
        {
          name: "Approve Generated Trace Links",
          tooltip: "Review automatically created graph links",
          onClick: () => navigateTo(Routes.TRACE_LINK, getParams()),
        },
        {
          name: "Generate New Trace Links",
          tooltip: "Generate new trace links within the current project view",
          onClick: () => appStore.toggleTraceLinkGenerator(),
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
          isHidden: !routesWithRequiredProject.includes(this.$route.path),
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
  },
});
</script>
