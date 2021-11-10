<template>
  <v-container>
    <v-container v-if="selectedArtifact !== undefined">
      <h3 class="text-center">
        {{ selectedArtifact.name }}
        <v-btn icon small @click="onArtifactEdit">
          <v-icon small>mdi-pencil</v-icon>
        </v-btn>
      </h3>
      <v-divider />
      <p class="text-body-1 mt-2 pa-2">
        {{ selectedArtifact.body }}
      </p>
      <v-divider class="mb-1" />
      <v-row>
        <v-col class="mr-1" cols="5">
          <v-container v-if="parents.length > 0">
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
          </v-container>
          <p v-else>No parents linked.</p>
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
      <v-row>
        <v-divider />
      </v-row>
      <v-row justify="center">
        <v-btn icon fab color="error" @click="onDeleteArtifact">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-row>
      <ArtifactCreatorModal
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @onClose="isArtifactCreatorOpen = false"
      />
    </v-container>
    <p v-else>No artifact selected</p>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact, PanelType, ProjectWarnings } from "@/types";
import {
  appModule,
  artifactSelectionModule,
  errorModule,
  projectModule,
} from "@/store";
import ArtifactCreatorModal from "@/components/common/modals/ArtifactCreatorModal.vue";
import { deleteArtifactHandler } from "@/api";

export default Vue.extend({
  components: { ArtifactCreatorModal },
  data() {
    return {
      previousArtifact: undefined as Artifact | undefined,
      isArtifactCreatorOpen: false,
    };
  },
  computed: {
    selectedArtifact(): Artifact | undefined {
      return artifactSelectionModule.getSelectedArtifact;
    },
    selectedArtifactName(): string | undefined {
      return this.selectedArtifact === undefined
        ? undefined
        : this.selectedArtifact.name;
    },
    parents(): string[] {
      const selectedArtifact = this.selectedArtifact;
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
      const selectedArtifactName = this.selectedArtifactName;
      if (selectedArtifactName !== undefined) {
        const traceLinks = projectModule.getTraceLinks;
        const query = traceLinks.filter(
          (l) => l.target === selectedArtifactName
        );
        return query.map((l) => l.source);
      } else {
        return [];
      }
    },
    projectWarnings(): ProjectWarnings {
      return errorModule.getArtifactWarnings;
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
    onArtifactEdit(): void {
      this.isArtifactCreatorOpen = true;
    },
    onArtifactClick(artifactName: string): void {
      const artifactQuery = projectModule.getArtifactByName(artifactName);
      if (artifactQuery !== undefined) {
        artifactSelectionModule.selectArtifact(artifactQuery);
      }
    },
    onDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        const { projectId } = projectModule.getProject;
        const artifactName = this.selectedArtifact.name;
        deleteArtifactHandler(projectId, artifactName).then(() => {
          artifactSelectionModule.UNSELECT_ARTIFACT();
          appModule.closePanel(PanelType.left);
        });
      }
    },
  },
});
</script>
