<template>
  <cy-element :definition="definition" />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  Artifact,
  ArtifactCytoCoreElement,
  ArtifactDeltaState,
  ArtifactWarning,
} from "@/types";
import {
  artifactSelectionModule,
  deltaModule,
  errorModule,
  subtreeModule,
} from "@/store";

export default Vue.extend({
  name: "ArtifactNode",
  props: {
    artifactDefinition: {
      type: Object as PropType<Artifact>,
      required: true,
    },
    hidden: Boolean,
    faded: Boolean,
  },
  computed: {
    /**
     * @return Whether the current artifact is selected.
     */
    isSelected(): boolean {
      return artifactSelectionModule.isArtifactInSelectedGroup(
        this.artifactDefinition.id
      );
    },
    /**
     * @return Any artifact warnings.
     */
    localWarnings(): ArtifactWarning[] | undefined {
      return errorModule.getArtifactWarnings[this.artifactDefinition.id];
    },
    /**
     * @return The delta state of this artifact.
     */
    artifactDeltaState(): ArtifactDeltaState {
      if (!deltaModule.inDeltaView) {
        return ArtifactDeltaState.NO_CHANGE;
      }

      return (
        deltaModule.getArtifactDeltaType(this.artifactDefinition.id) ||
        ArtifactDeltaState.NO_CHANGE
      );
    },
    /**
     * @return The cytoscape definition of this artifact.
     */
    definition(): ArtifactCytoCoreElement {
      const { id, body, type, name, safetyCaseType, logicType } =
        this.artifactDefinition;
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
          opacity: this.hidden ? 0 : this.faded ? 0.1 : 1,
          hiddenChildren: hiddenChildren.length,
          childWarnings: hiddenChildWarnings,
          childDeltaStates: hiddenChildDeltaStates,
          safetyCaseType,
          logicType,
        },
      };
    },
  },
});
</script>
