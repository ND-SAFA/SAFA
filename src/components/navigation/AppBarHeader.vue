<template>
  <v-container class="ma-0 pa-0">
    <v-row class="ma-0 pa-0">
      <v-col cols="1" class="ma-0 pa-0" align-self="center">
        <v-row class="ma-0 pa-0" justify="center">
          <SafaIcon />
        </v-row>
      </v-col>
      <v-col cols="11" class="ma-0 pa-0">
        <v-row class="ma-0 pa-0">
          <ProjectName color="white" />
        </v-row>
        <v-row class="ma-0 pa-0">
          <v-col cols="auto" class="ma-0 pa-0">
            <ButtonRow :definitions="definitions" justify="start" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
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
      :start-step="2"
      @onClose="changeVersionOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import { navigateTo, Routes } from "@/router";
import {
  BaselineVersionModal,
  UploadNewVersionModal,
  ButtonRow,
} from "@/components/common";
import ProjectName from "./ProjectName.vue";
import SafaIcon from "./SafaIcon.vue";

export default Vue.extend({
  components: {
    SafaIcon,
    ProjectName,
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
    onUploadVersion(): void {
      this.uploadVersionOpen = true;
    },
    onOpenProject(): void {
      this.openProjectOpen = true;
    },
  },

  created() {
    this.definitions = [
      {
        type: ButtonType.LIST_MENU,
        label: "Project",
        buttonIsText: true,
        menuItems: ["Create Project", "Open Project"],
        menuHandlers: [
          () => navigateTo(Routes.PROJECT_CREATOR),
          this.onOpenProject,
        ],
      },
      {
        type: ButtonType.LIST_MENU,
        label: "Version",
        buttonIsText: true,
        menuItems: ["Upload new version"],
        menuHandlers: [this.onUploadVersion],
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
