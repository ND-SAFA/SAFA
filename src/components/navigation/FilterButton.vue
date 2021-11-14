<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon small color="secondary" dark v-on="on">
        <v-icon>mdi-filter</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item v-for="item in artifactTypes" :key="item.name">
        <v-checkbox
          :label="item.name"
          :value="item.name"
          v-model="selectedMenuItems"
        />
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { projectModule } from "@/store";
import { Artifact } from "@/types";
import { Project } from "@/types";
import Vue from "vue";
export default Vue.extend({
  computed: {
    data() {
      return {
        selectedMenuItems: [],
      };
    },
    artifactTypes(): string[] {
      const project: Project | undefined = projectModule.getProject;
      if (project === undefined) {
        return [];
      } else {
        return project.artifacts.map((artifact: Artifact) => artifact.type);
      }
    },
  },
});
</script>
