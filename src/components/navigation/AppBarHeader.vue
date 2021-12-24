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
  </v-flex>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType, EmptyLambda, Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { logModule, projectModule } from "@/store";
import {
  BaselineVersionModal,
  ButtonRow,
  UploadNewVersionModal,
} from "@/components/common";
import SafaIcon from "./SafaIcon.vue";
import AccountDropdown from "./AccountDropdown.vue";
import VersionLabel from "@/components/artifact-tree-view/VersionLabel.vue";

/**
 * Local representation of generated menu items.
 */
type CondensedMenuItem = [string, EmptyLambda];

export default Vue.extend({
  components: {
    VersionLabel,
    AccountDropdown,
    SafaIcon,
    ButtonRow,
    UploadNewVersionModal,
    BaselineVersionModal,
  },
  data() {
    return {
      openProjectOpen: false,
      uploadVersionOpen: false,
      changeVersionOpen: false,
    };
  },
  methods: {
    onOpenProject(): void {
      this.openProjectOpen = true;
    },
    onUploadVersion(): void {
      this.uploadVersionOpen = true;
    },
    onChangeVersion(): void {
      const versionId = this.project.projectVersion?.versionId;
      if (versionId !== undefined && versionId !== "") {
        this.changeVersionOpen = true;
      } else {
        logModule.onWarning("Please select a project.");
      }
    },
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
    projectMenuItems(): CondensedMenuItem[] {
      const isProjectDefined = this.project.projectId !== "";
      const options: CondensedMenuItem[] = [
        ["Open", this.onOpenProject],
        ["Create", () => navigateTo(Routes.PROJECT_CREATOR)],
        ["Settings", () => navigateTo(Routes.PROJECT_SETTINGS)],
      ];
      return isProjectDefined ? options : options.slice(0, -1);
    },
    definitions(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.LIST_MENU,
          label: "Project",
          buttonIsText: true,
          menuItems: this.projectMenuItems.map((i) => i[0]),
          menuHandlers: this.projectMenuItems.map((i) => i[1]),
        },
        {
          type: ButtonType.LIST_MENU,
          label: "Version",
          buttonIsText: true,
          menuItems: ["Change Version", "Upload Flat Files"],
          menuHandlers: [this.onChangeVersion, this.onUploadVersion],
        },
        {
          type: ButtonType.LIST_MENU,
          label: "Trace Links",
          buttonIsText: true,
          menuItems: ["Approve Generated Trace Links"],
          menuHandlers: [() => navigateTo(Routes.TRACE_LINK)],
        },
      ];
    },
  },
});
</script>
