<template>
  <v-container class="ma-0 pa-0">
    <v-row class="ma-0 pa-0">
      <v-col cols="1" class="ma-0 pa-0" align-self="center">
        <v-row class="ma-0 pa-0" justify="center">
          <SAFAIcon />
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
    <UploadNewVersionModal
      :isOpen="uploadVersionOpen"
      @onClose="uploadVersionOpen = false"
    />
    <BaselineVersionModal
      :isOpen="openProjectOpen"
      @onClose="openProjectOpen = false"
    />
    <ProjectCreatorModal
      :isOpen="createProjectOpen"
      @onClose="createProjectOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SAFAIcon from "@/components/navigation/SafaIcon.vue";
import ProjectName from "@/components/navigation/ProjectName.vue";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { ButtonDefinition, ButtonType } from "@/types";
import UploadNewVersionModal from "@/components/common/modals/UploadNewVersionModal.vue";
import router, { Routes } from "@/router";
import BaselineVersionModal from "@/components/common/modals/BaselineVersionModal.vue";
import ProjectCreatorModal from "@/components/project/creator/ProjectCreator.vue";
import { appModule } from "@/store";

export default Vue.extend({
  components: {
    SAFAIcon,
    ProjectName,
    ButtonRow,
    UploadNewVersionModal,
    BaselineVersionModal,
    ProjectCreatorModal,
  },
  data() {
    return {
      openProjectOpen: false,
      uploadVersionOpen: false,
      createProjectOpen: false,
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
    onCreateProject(): void {
      this.createProjectOpen = true;
    },
  },

  created() {
    this.definitions = [
      {
        type: ButtonType.LIST_MENU,
        label: "Project",
        menuItems: ["Create Project", "Open Project"],
        menuHandlers: [this.onCreateProject, this.onOpenProject],
      },
      {
        type: ButtonType.LIST_MENU,
        label: "Version",
        menuItems: ["Upload new version"],
        menuHandlers: [this.onUploadVersion],
      },
      {
        type: ButtonType.LIST_MENU,
        label: "Trace Links",
        menuItems: ["Approve Generated Trace Links"],
        menuHandlers: [() => router.push(Routes.TRACE_LINK)],
      },
    ];
  },
});
</script>
