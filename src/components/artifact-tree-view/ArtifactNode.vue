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
      addedData: undefined as AddedArtifact | undefined,
      removedData: undefined as RemovedArtifact | undefined,
      modifiedData: undefined as ModifiedArtifact | undefined,
    };
  },
  methods: {
    setAddedData(data: AddedArtifact) {
      this.clearData();
      this.addedData = data;
    },
    setRemovedData(data: RemovedArtifact) {
      this.clearData();
      this.removedData = data;
    },
    setModifiedData(data: ModifiedArtifact) {
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
    selectedSubtree(): string[] {
      return artifactSelectionModule.getSelectedSubtree;
    },
    isSelected(): boolean {
      const selectedArtifact = this.selectedArtifact;
      return (
        selectedArtifact !== undefined &&
        selectedArtifact.name === this.artifactDefinition.name
      );
    },
    isDeltaViewEnabled(): boolean {
      return deltaModule.getIsDeltaViewEnabled;
    },
    localWarnings(): ArtifactWarning[] | undefined {
      const artifactWarnings: ProjectWarnings = errorModule.getArtifactWarnings;
      const artifactName = this.artifactDefinition.name;
      if (artifactName in artifactWarnings) {
        return artifactWarnings[artifactName];
      }
      return undefined;
    },
    artifactDeltaState(): ArtifactDeltaState {
      if (!this.isDeltaViewEnabled) {
        this.clearData();
        return ArtifactDeltaState.NO_CHANGE;
      }
      const name: string = this.artifactDefinition.name;
      const addedArtifacts: Record<string, AddedArtifact> =
        deltaModule.getAdded;
      const removedArtifacts: Record<string, RemovedArtifact> =
        deltaModule.getRemoved;
      const modifiedArtifacts: Record<string, ModifiedArtifact> =
        deltaModule.getModified;

      if (name in addedArtifacts) {
        this.setAddedData(addedArtifacts[name]);
        return ArtifactDeltaState.ADDED;
      } else if (name in removedArtifacts) {
        this.setRemovedData(removedArtifacts[name]);
        return ArtifactDeltaState.REMOVED;
      } else if (name in modifiedArtifacts) {
        this.setModifiedData(modifiedArtifacts[name]);
        return ArtifactDeltaState.MODIFIED;
      } else {
        return ArtifactDeltaState.NO_CHANGE;
      }
    },
    definition(): ArtifactCytoCoreElement {
      const id = this.artifactDefinition.name;
      const body = this.artifactDefinition.body;
      const artifactType = this.artifactDefinition.type;
      const isSelected = this.isSelected;
      const hiddenChildren = subtreeModule.hiddenChildrenForNode(id);
      const hiddenChildWarnings =
        errorModule.allArtifactWarnings(hiddenChildren);
      const hiddenChildDeltaStates = deltaModule.allDeltaStates(hiddenChildren);

      return {
        data: {
          id,
          body,
          artifactName: id,
          type: "node",
          warnings: this.localWarnings,
          artifactType,
          artifactDeltaState: this.artifactDeltaState,
          isSelected,
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
