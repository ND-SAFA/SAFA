<template>
  <v-container>
    <div v-if="selectedArtifact !== undefined">
      <v-row align="center">
        <v-col>
          <h1 class="text-h4">{{ selectedArtifact.name }}</h1>
        </v-col>
        <v-col>
          <v-row justify="end" class="mr-1">
            <generic-icon-button
              tooltip="Edit"
              icon-id="mdi-pencil"
              @click="onArtifactEdit"
            />
            <generic-icon-button
              color="error"
              tooltip="Delete"
              icon-id="mdi-delete"
              @click="onDeleteArtifact"
            />
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="mb-2" />

      <p class="text-body-1">
        {{ selectedArtifact.body }}
      </p>

      <v-divider />

      <v-row>
        <v-col>
          <v-subheader>Parents</v-subheader>
          <v-divider />
          <p v-if="parents.length === 0" class="text-caption text-center mt-1">
            No parents linked.
          </p>
          <v-list dense v-else>
            <v-btn
              outlined
              block
              class="mb-1"
              v-for="parentName in parents"
              :key="parentName"
              @click="onArtifactClick(parentName)"
            >
              {{ parentName }}
            </v-btn>
          </v-list>
        </v-col>

        <v-col>
          <v-subheader>Children</v-subheader>
          <v-divider />
          <p v-if="children.length === 0" class="text-caption text-center mt-1">
            No children linked.
          </p>
          <v-list dense v-else>
            <v-btn
              outlined
              block
              class="mb-1"
              v-for="childName in children"
              :key="childName"
              @click="onArtifactClick(childName)"
            >
              {{ childName }}
            </v-btn>
          </v-list>
        </v-col>
      </v-row>

      <v-expansion-panels v-if="selectedArtifactWarnings.length > 0">
        <v-expansion-panel>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-expansion-panel-header
                v-on="on"
                v-bind="attrs"
                disable-icon-rotate
                expand-icon="mdi-hazard-lights"
              >
                Warnings ({{ selectedArtifactWarnings.length }})
              </v-expansion-panel-header>
            </template>
            <span>View warnings</span>
          </v-tooltip>
          <v-expansion-panel-content>
            <p
              class="text-body-1"
              v-for="warning in selectedArtifactWarnings"
              :key="warning"
            >
              <v-divider />
              {{ warning }}
            </p>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <artifact-creator-modal
        title="Edit Artifact Contents"
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @close="isArtifactCreatorOpen = false"
      />
    </div>

    <p v-else class="text-body-1">No artifact is selected.</p>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact, PanelType, ProjectWarnings } from "@/types";
import { deleteArtifactFromCurrentVersion } from "@/api";
import {
  appModule,
  artifactSelectionModule,
  errorModule,
  projectModule,
} from "@/store";
import { GenericIconButton, ArtifactCreatorModal } from "@/components/common";

export default Vue.extend({
  components: { GenericIconButton, ArtifactCreatorModal },
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
        const traceLinks = projectModule.traceLinks;
        const query = traceLinks.filter(
          (l) => l.sourceName === selectedArtifact.name
        );
        return query.map((l) => l.targetName);
      } else {
        return [];
      }
    },
    children(): string[] {
      const selectedArtifactName = this.selectedArtifactName;
      if (selectedArtifactName !== undefined) {
        const traceLinks = projectModule.traceLinks;
        const query = traceLinks.filter(
          (l) => l.targetName === selectedArtifactName
        );
        return query.map((l) => l.sourceName);
      } else {
        return [];
      }
    },
    projectWarnings(): ProjectWarnings {
      return errorModule.getArtifactWarnings;
    },
    selectedArtifactWarnings(): string[] {
      const id = this.selectedArtifact?.id || "";

      return (this.projectWarnings[id] || []).map(
        ({ ruleMessage }) => ruleMessage
      );
    },
  },
  methods: {
    onArtifactEdit(): void {
      this.isArtifactCreatorOpen = true;
    },
    onArtifactClick(artifactName: string): void {
      const artifact = projectModule.getArtifactByName(artifactName);
      artifactSelectionModule.selectArtifact(artifact.id);
    },
    onDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        deleteArtifactFromCurrentVersion(this.selectedArtifact).then(() => {
          artifactSelectionModule.UNSELECT_ARTIFACT();
          appModule.closePanel(PanelType.left);
        });
      }
    },
  },
});
</script>
