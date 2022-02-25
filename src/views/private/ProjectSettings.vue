<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Back To Tree View
      </v-btn>
      <v-container>
        <settings-general-section :project="project" />
        <settings-member-section :project="project" />
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  PrivatePage,
  SettingsGeneralSection,
  SettingsMemberSection,
} from "@/components";
import { Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { projectModule } from "@/store";

export default Vue.extend({
  name: "approval-links-view",
  components: {
    PrivatePage,
    SettingsGeneralSection,
    SettingsMemberSection,
  },

  computed: {
    project(): Project {
      return projectModule.getProject;
    },
    hasDescription(): boolean {
      const description = this.project.meta.description;
      return description !== "";
    },
    headers() {
      return [
        { text: "Email", value: "email", sortable: false, isSelectable: false },
        {
          text: "Role",
          value: "role",
          sortable: true,
          isSelectable: false,
        },
      ];
    },
  },
  methods: {
    handleGoBack() {
      navigateTo(Routes.ARTIFACT_TREE);
    },
  },
});
</script>
