<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import {
  deltaModule,
  errorModule,
  artifactSelectionModule,
  subtreeModule,
} from "@/store";
import {
  Artifact,
  ArtifactWarning,
  ProjectWarnings,
  AddedArtifact,
  ArtifactDeltaState,
  ModifiedArtifact,
  RemovedArtifact,
  ArtifactCytoCoreElement,
  EntityModification,
} from "@/types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  name: "artifact",
  props: {
    artifactDefinition: Object as PropType<Artifact>,
    opacity: {
      type: Number,
      required: true,
    },
  },
  data: function () {
    return {
      addedData: undefined as Artifact | undefined,
      removedData: undefined as Artifact | undefined,
      modifiedData: undefined as EntityModification<Artifact> | undefined,
    };
  },
  methods: {
    setAddedData(data: Artifact) {
      this.clearData();
      this.addedData = data;
    },
    setRemovedData(data: Artifact) {
      this.clearData();
      this.removedData = data;
    },
    setModifiedData(data: EntityModification<Artifact>) {
      this.clearData();
      this.modifiedData = data;
    },
    clearData() {
      this.addedData = undefined;
      this.removedData = undefined;
      this.modifiedData = undefined;
    },
  },
  watch: {
    artifactWarnings(): ProjectWarnings {
      return errorModule.getArtifactWarnings;
    },
  },
  computed: {
    selectedArtifact(): Artifact | undefined {
      return artifactSelectionModule.getSelectedArtifact;
    },
    isSelected(): boolean {
      const selectedArtifact = this.selectedArtifact;

      return (
        selectedArtifact !== undefined &&
        selectedArtifact.id === this.artifactDefinition.id
      );
    },
    isDeltaViewEnabled(): boolean {
      return deltaModule.getIsDeltaViewEnabled;
    },
    localWarnings(): ArtifactWarning[] | undefined {
      const artifactWarnings: ProjectWarnings = errorModule.getArtifactWarnings;
      const artifactId = this.artifactDefinition.id;

      if (artifactId in artifactWarnings) {
        return artifactWarnings[artifactId];
      }

      return undefined;
    },
    artifactDeltaState(): ArtifactDeltaState {
      if (!this.isDeltaViewEnabled) {
        this.clearData();
        return ArtifactDeltaState.NO_CHANGE;
      }

      const artifactId: string = this.artifactDefinition.id;
      const addedArtifacts: Record<string, Artifact> =
        deltaModule.addedArtifacts;
      const removedArtifacts: Record<string, Artifact> =
        deltaModule.removedArtifacts;
      const modifiedArtifacts: Record<
        string,
        EntityModification<Artifact>
      > = deltaModule.modifiedArtifacts;

      if (artifactId in addedArtifacts) {
        this.setAddedData(addedArtifacts[artifactId]);
        return ArtifactDeltaState.ADDED;
      } else if (artifactId in removedArtifacts) {
        this.setRemovedData(removedArtifacts[artifactId]);
        return ArtifactDeltaState.REMOVED;
      } else if (artifactId in modifiedArtifacts) {
        this.setModifiedData(modifiedArtifacts[artifactId]);
        return ArtifactDeltaState.MODIFIED;
      } else {
        return ArtifactDeltaState.NO_CHANGE;
      }
    },
    definition(): ArtifactCytoCoreElement {
      const { id, body, type, name } = this.artifactDefinition;
      const hiddenChildren = subtreeModule.getHiddenChildrenByParentId(id);
      const hiddenChildWarnings =
        errorModule.getWarningsByArtifactNames(hiddenChildren);
      const hiddenChildDeltaStates =
        deltaModule.getDeltaStatesByArtifactNames(hiddenChildren);

      return {
        data: {
          id,
          body,
          artifactName: name,
          type: "node",
          warnings: this.localWarnings,
          artifactType: type,
          artifactDeltaState: this.artifactDeltaState,
          isSelected: this.isSelected,
          opacity: this.opacity,
          hiddenChildren: hiddenChildren.length,
          childWarnings: hiddenChildWarnings,
          childDeltaStates: hiddenChildDeltaStates,
        },
      };
    },
  },
});
</script>
