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
            <button-row :definitions="definitions" justify="start" />
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
    <CreateNewProjectModal
      :isOpen="createProjectOpen"
      @onClose="createProjectOpen = false"
    />
    <create-new-project-modal />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SAFAIcon from "@/components/navigation/SafaIcon.vue";
import ProjectName from "@/components/navigation/ProjectName.vue";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { ButtonDefinition, ButtonType } from "@/types/common-components";
import UploadNewVersionModal from "@/components/common/modals/UploadNewVersionModal.vue";
import router from "@/router";
import { TRACE_LINK_ROUTE_NAME } from "@/router/routes";
import BaselineVersionModal from "@/components/common/modals/BaselineVersionModal.vue";
import CreateNewProjectModal from "@/components/common/modals/CreateNewProjectModal.vue";

export default Vue.extend({
  components: {
    SAFAIcon,
    ProjectName,
    ButtonRow,
    UploadNewVersionModal,
    BaselineVersionModal,
    CreateNewProjectModal,
  },
  data() {
    return {
      openProjectOpen: false,
      uploadVersionOpen: false,
      createProjectOpen: true,
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
      console.log("create project clicked");
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
        menuHandlers: [
          () =>
            router.push(TRACE_LINK_ROUTE_NAME).catch((e) => console.warn(e)),
        ],
      },
    ];
  },
});
</script>
