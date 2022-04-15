<template>
  <v-container>
    <div v-if="selectedArtifact !== undefined">
      <v-row align="center">
        <v-col>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <h1 v-on="on" v-bind="attrs" class="text-h4 artifact-title">
                {{ selectedArtifact.name }}
              </h1>
            </template>
            {{ selectedArtifact.name }}
          </v-tooltip>
        </v-col>
        <v-col>
          <v-row justify="end" class="mr-1">
            <generic-icon-button
              v-if="!selectedArtifact.logicType"
              tooltip="Edit"
              icon-id="mdi-pencil"
              @click="handleArtifactEdit"
            />
            <generic-icon-button
              color="error"
              tooltip="Delete"
              icon-id="mdi-delete"
              @click="handleDeleteArtifact"
            />
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="mb-2" />

      <p class="text-body-1">
        {{ selectedArtifact.body }}
      </p>

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
              @click="handleArtifactClick(parentName)"
            >
              <span class="mb-1 text-ellipsis" style="max-width: 60px">
                {{ parentName }}
              </span>
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
              @click="handleArtifactClick(childName)"
            >
              <span class="mb-1 text-ellipsis" style="max-width: 60px">
                {{ childName }}
              </span>
            </v-btn>
          </v-list>
        </v-col>
      </v-row>

      <div v-if="documents.length > 0">
        <v-subheader>Documents</v-subheader>
        <v-divider />

        <v-list>
          <v-list-item
            v-for="doc in documents"
            :key="doc.documentId"
            @click="handleSwitchDocument(doc)"
          >
            <v-list-item-title>
              {{ doc.name }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ documentTypeName(doc.type) }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </div>

      <div v-if="selectedArtifactWarnings.length > 0">
        <v-row align="center" class="debug">
          <v-col>
            <v-subheader>Warnings</v-subheader>
          </v-col>
          <v-col class="flex-grow-0 mr-2">
            <v-icon color="secondary">mdi-hazard-lights</v-icon>
          </v-col>
        </v-row>

        <v-divider />

        <v-expansion-panels>
          <v-expansion-panel
            v-for="warning in selectedArtifactWarnings"
            :key="warning"
          >
            <v-expansion-panel-header class="text-body-1">
              {{ warning.ruleName }}
            </v-expansion-panel-header>
            <v-expansion-panel-content class="text-body-1">
              {{ warning.ruleMessage }}
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>

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
import { Artifact, ArtifactWarning, PanelType, ProjectDocument } from "@/types";
import { documentTypeOptions } from "@/util";
import {
  appModule,
  artifactModule,
  artifactSelectionModule,
  documentModule,
  errorModule,
  traceModule,
} from "@/store";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton, ArtifactCreatorModal } from "@/components/common";

/**
 * Displays the selected node tab.
 */
export default Vue.extend({
  name: "SelectedNodeTab",
  components: { GenericIconButton, ArtifactCreatorModal },
  data() {
    return {
      previousArtifact: undefined as Artifact | undefined,
      isArtifactCreatorOpen: false,
    };
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    selectedArtifactName(): string {
      return this.selectedArtifact?.name || "";
    },
    /**
     * @return The selected artifact's parents.
     */
    parents(): string[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ sourceName }) => sourceName === this.selectedArtifactName)
        .map(({ targetName }) => targetName);
    },
    /**
     * @return The selected artifact's children.
     */
    children(): string[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ targetName }) => targetName === this.selectedArtifactName)
        .map(({ sourceName }) => sourceName);
    },
    /**
     * @return The selected artifact's documents.
     */
    documents(): ProjectDocument[] {
      if (!this.selectedArtifact) return [];

      return documentModule.projectDocuments.filter(({ documentId }) =>
        this.selectedArtifact?.documentIds.includes(documentId)
      );
    },
    /**
     * @return The selected artifact's warnings.
     */
    selectedArtifactWarnings(): ArtifactWarning[] {
      const id = this.selectedArtifact?.id || "";

      return errorModule.getArtifactWarnings[id] || [];
    },
  },
  methods: {
    /**
     * Opens the artifact edit modal.
     */
    handleArtifactEdit(): void {
      this.isArtifactCreatorOpen = true;
    },
    /**
     * Selects an artifact.
     * @param artifactName - The artifact to select.
     */
    handleArtifactClick(artifactName: string): void {
      const artifact = artifactModule.getArtifactByName(artifactName);

      artifactSelectionModule.selectArtifact(artifact.id);
    },
    /**
     * Attempts to delete the selected artifact.
     */
    handleDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        handleDeleteArtifact(this.selectedArtifact).then(() => {
          appModule.closePanel(PanelType.left);
        });
      }
    },
    /**
     * Switches to another document.
     * @param document - The document to switch to.
     */
    handleSwitchDocument(document: ProjectDocument): void {
      documentModule.switchDocuments(document);
    },
    /**
     * Converts the document type into a display name.
     * @param typeId - The document type id.
     * @return The document type name.
     */
    documentTypeName(typeId: string): string {
      return (
        documentTypeOptions().find(({ id }) => id === typeId)?.name || typeId
      );
    },
  },
});
</script>

<style scoped>
.v-expansion-panel::before {
  box-shadow: none;
}

.artifact-title {
  overflow: hidden;
  text-overflow: ellipsis;
  width: 135px;
}
</style>
