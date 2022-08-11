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
import { navigateBack } from "@/router";
import { projectModule } from "@/store";
import {
  PrivatePage,
  SettingsGeneralSection,
  SettingsMemberSection,
} from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "ProjectSettingsView",
  components: {
    PrivatePage,
    SettingsGeneralSection,
    SettingsMemberSection,
  },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectModule.getProject;
    },
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },
  },
});
</script>
