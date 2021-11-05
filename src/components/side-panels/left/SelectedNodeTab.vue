<template>
  <v-container>
    <v-container v-if="selectedArtifact !== undefined">
      <h3 class="text-center">
        {{ selectedArtifact.name }}
      </h3>
      <v-divider />
      <p class="text-body-1 mt-2 pa-2">
        {{ selectedArtifact.body }}
      </p>
      <v-divider class="mb-1" />
      <v-row>
        <v-col class="mr-1" cols="5" v-if="parents.length > 0">
          <h4>Parents</h4>
          <v-btn
            fab
            x-small
            class="ma-2"
            color="primary"
            v-for="parentName in parents"
            :key="parentName"
            @click="onArtifactClick(parentName)"
          >
            {{ parentName }}
          </v-btn>
        </v-col>

        <v-col cols="5" v-if="children.length > 0">
          <h4>Children</h4>
          <v-btn
            fab
            x-small
            class="ma-1"
            color="primary"
            v-for="childName in children"
            :key="childName"
            @click="onArtifactClick(childName)"
          >
            {{ childName }}
          </v-btn>
        </v-col>
      </v-row>
      <v-divider class="mt-2" />
      <v-row class="pa-1 mt-10">
        <p
          class="text-body-2 font-italic"
          v-if="selectedArtifactWarnings !== undefined"
        >
          <v-icon color="secondary"> mdi-hazard-lights </v-icon>
          {{ selectedArtifactWarnings }}
        </p>
      </v-row>
    </v-container>
    <p v-else>No artifact selected</p>
  </v-container>
</template>

<script lang="ts">
import { Artifact, ProjectWarnings } from "@/types";
import Vue from "vue";
import { errorModule, artifactSelectionModule, projectModule } from "@/store";

export default Vue.extend({
  data() {
    return {
      previousArtifact: undefined as Artifact | undefined,
    };
  },
  computed: {
    parents(): string[] {
      const selectedArtifact = artifactSelectionModule.getSelectedArtifact;
      if (selectedArtifact !== undefined) {
        const traceLinks = projectModule.getTraceLinks;
        const query = traceLinks.filter(
          (l) => l.source === selectedArtifact.name
        );
        return query.map((l) => l.target);
      } else {
        return [];
      }
    },
    children(): string[] {
      const selectedArtifact = artifactSelectionModule.getSelectedArtifact;
      if (selectedArtifact !== undefined) {
        const traceLinks = projectModule.getTraceLinks;
        const query = traceLinks.filter(
          (l) => l.target === selectedArtifact.name
        );
        return query.map((l) => l.source);
      } else {
        return [];
      }
    },
    selectedArtifact(): Artifact | undefined {
      return artifactSelectionModule.getSelectedArtifact;
    },
    projectWarnings(): ProjectWarnings {
      return errorModule.artifactWarnings;
    },
    selectedArtifactWarnings(): string | undefined {
      if (
        this.selectedArtifact !== undefined &&
        this.selectedArtifact.name in this.projectWarnings
      ) {
        return this.projectWarnings[this.selectedArtifact.name][0].ruleMessage;
      }
      return undefined;
    },
  },
  methods: {
    onArtifactClick(artifactName: string): void {
      const artifactQuery = projectModule.getArtifactByName(artifactName);
      if (artifactQuery !== undefined) {
        artifactSelectionModule.selectArtifact(artifactQuery);
      }
    },
  },
});
</script>
