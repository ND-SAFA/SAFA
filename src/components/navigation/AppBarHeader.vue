<template>
  <v-flex class="d-flex flex-row">
    <v-row dense>
      <v-col class="flex-grow-0 mt-2">
        <SafaIcon />
      </v-col>
      <v-col cols="2">
        <h1 class="text-h5 white--text pl-4">SAFA</h1>
        <ButtonRow :definitions="definitions" justify="start" />
      </v-col>
    </v-row>

    <account-dropdown />

    <upload-new-version-modal
      :isOpen="uploadVersionOpen"
      @onClose="uploadVersionOpen = false"
    />
    <baseline-version-modal
      :is-open="openProjectOpen"
      @onClose="openProjectOpen = false"
    />
    <baseline-version-modal
      title="Change project version"
      :is-open="changeVersionOpen"
      :project="project"
      @onClose="changeVersionOpen = false"
    />
  </v-flex>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType, Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { appModule, projectModule } from "@/store";
import {
  BaselineVersionModal,
  ButtonRow,
  UploadNewVersionModal,
} from "@/components/common";
import SafaIcon from "./SafaIcon.vue";
import AccountDropdown from "./AccountDropdown.vue";

export default Vue.extend({
  components: {
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
      definitions: [] as ButtonDefinition[], // defined once module has been created
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
        appModule.onWarning("Please select a project.");
      }
    },
  },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
  },
  created() {
    this.definitions = [
      {
        type: ButtonType.LIST_MENU,
        label: "Project",
        buttonIsText: true,
        menuItems: ["Open Project", "Create Project"],
        menuHandlers: [
          this.onOpenProject,
          () => navigateTo(Routes.PROJECT_CREATOR),
        ],
      },
      {
        type: ButtonType.LIST_MENU,
        label: "Version",
        buttonIsText: true,
        menuItems: ["Change Version", "Upload new version"],
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
});
</script>
