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

    <v-menu>
      <template v-slot:activator="{ on: menuOn, attrs }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: tooltipOn }">
            <v-btn
              icon
              class="mt-2"
              v-on="{ ...tooltipOn, ...menuOn }"
              v-bind="attrs"
            >
              <v-avatar color="white">
                <v-icon color="primary" style="font-size: 48px">
                  mdi-account-circle
                </v-icon>
              </v-avatar>
            </v-btn>
          </template>
          <span>My Account</span>
        </v-tooltip>
      </template>

      <v-list dense>
        <v-list-item>
          <v-btn text color="error" @click="handleLogout">Logout</v-btn>
        </v-list-item>
      </v-list>
    </v-menu>

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
import { appModule, projectModule, sessionModule } from "@/store";
import {
  BaselineVersionModal,
  ButtonRow,
  UploadNewVersionModal,
} from "@/components/common";
import SafaIcon from "./SafaIcon.vue";

export default Vue.extend({
  components: {
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
    handleLogout(): void {
      sessionModule.logout().then(() => navigateTo(Routes.LOGIN_ACCOUNT));
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
