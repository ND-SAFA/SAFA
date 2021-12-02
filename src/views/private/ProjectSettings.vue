<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Back To Tree View
      </v-btn>
      <v-container>
        <v-row>
          <h1>{{ project.name }}</h1>
          <p>{{ project.description }}</p>
        </v-row>
        <v-row> Project members </v-row>
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage } from "@/components";
import { Project } from "@/types";
import { navigateTo, Routes } from "@/router";
import { projectModule } from "@/store";

export default Vue.extend({
  name: "approval-links-view",
  components: { PrivatePage },
  computed: {
    project(): Project {
      return projectModule.getProject;
    },
  },
  methods: {
    handleGoBack() {
      navigateTo(Routes.ARTIFACT_TREE);
    },
  },
});
</script>
