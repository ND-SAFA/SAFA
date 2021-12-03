<template>
  <v-container>
    <v-container v-if="selectedArtifact !== undefined">
      <v-row align="center">
        <v-col>
          <h1>{{ selectedArtifact.name }}</h1>
        </v-col>
        <v-col>
          <v-row justify="end">
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
            <v-list-item-group>
              <v-list-item
                v-for="parentName in parents"
                :key="parentName"
                @click="onArtifactClick(parentName)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="parentName" />
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-col>

        <v-col>
          <v-subheader>Children</v-subheader>
          <v-divider />
          <p v-if="children.length === 0" class="text-caption text-center mt-1">
            No children linked.
          </p>
          <v-list dense v-else>
            <v-list-item-group>
              <v-list-item
                v-for="childName in children"
                :key="childName"
                @click="onArtifactClick(childName)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="childName" />
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-col>
      </v-row>

      <v-divider />

      <v-row justify="center" v-if="selectedArtifactWarnings !== undefined">
        <v-col class="flex-grow-0 my-1">
          <v-icon color="secondary"> mdi-hazard-lights </v-icon>
        </v-col>
      </v-row>

      <p
        class="text-body-2 font-italic"
        v-if="selectedArtifactWarnings !== undefined"
      >
        {{ selectedArtifactWarnings }}
      </p>

      <artifact-creator-modal
        title="Edit Artifact Contents"
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @close="isArtifactCreatorOpen = false"
      />
    </v-container>

    <p v-else>No artifact selected</p>
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
      artifactSelectionModule.selectArtifact(artifactQuery);
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
