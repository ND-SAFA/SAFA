<template>
  <div v-if="doDisplay">
    <panel-card>
      <flex-box justify="space-between" align="center">
        <typography el="h2" l="1" variant="subtitle" value="Parent Artifacts" />
        <text-button
          text
          variant="add"
          data-cy="button-artifact-link-parent"
          @click="handleLinkParent"
        >
          Link Parent
        </text-button>
      </flex-box>
      <v-divider />
      <v-list
        v-if="parents.length > 0"
        dense
        style="max-height: 300px"
        class="overflow-y-auto"
        data-cy="list-selected-parents"
      >
        <template v-for="parent in parents">
          <v-list-item
            :key="parent.id"
            data-cy="list-selected-parent-item"
            @click="handleArtifactClick(parent.name)"
          >
            <v-list-item-title>
              <artifact-body-display display-title :artifact="parent" />
            </v-list-item-title>
            <v-list-item-action @click.stop="">
              <icon-button
                icon-id="mdi-ray-start-end"
                tooltip="View Trace Link"
                data-cy="button-selected-parent-link"
                @click="handleTraceLinkClick(parent.name)"
              />
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card>
      <flex-box justify="space-between" align="center">
        <typography el="h2" l="1" variant="subtitle" value="Child Artifacts" />
        <text-button
          text
          variant="add"
          data-cy="button-artifact-link-child"
          @click="handleLinkChild"
        >
          Link Child
        </text-button>
      </flex-box>
      <v-divider />
      <v-list
        v-if="children.length > 0"
        dense
        style="max-height: 300px"
        class="overflow-y-auto"
        data-cy="list-selected-children"
      >
        <template v-for="child in children">
          <v-list-item
            :key="child.name"
            data-cy="list-selected-child-item"
            @click="handleArtifactClick(child.name)"
          >
            <v-list-item-title>
              <artifact-body-display display-title :artifact="child" />
            </v-list-item-title>
            <v-list-item-action @click.stop="">
              <icon-button
                icon-id="mdi-ray-start-end"
                tooltip="View Trace Link"
                data-cy="button-selected-child-link"
                @click="handleTraceLinkClick(child.name)"
              />
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no child artifacts."
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactSchema } from "@/types";
import {
  appStore,
  artifactStore,
  selectionStore,
  subtreeStore,
  traceStore,
} from "@/hooks";
import {
  Typography,
  IconButton,
  PanelCard,
  ArtifactBodyDisplay,
  TextButton,
  FlexBox,
} from "@/components/common";

/**
 * Displays the selected node's parents and children.
 */
export default Vue.extend({
  name: "ArtifactTraces",
  components: {
    FlexBox,
    ArtifactBodyDisplay,
    PanelCard,
    IconButton,
    Typography,
    TextButton,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    artifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's parents.
     */
    parents(): ArtifactSchema[] {
      if (!this.artifact) return [];

      return subtreeStore
        .getParents(this.artifact.id)
        .map((id) => artifactStore.getArtifactById(id)) as ArtifactSchema[];
    },
    /**
     * @return The selected artifact's children.
     */
    children(): ArtifactSchema[] {
      if (!this.artifact) return [];

      return subtreeStore
        .getChildren(this.artifact.id)
        .map((id) => artifactStore.getArtifactById(id)) as ArtifactSchema[];
    },
    /**
     * @return Whether to display this section.
     */
    doDisplay(): boolean {
      return this.parents.length + this.children.length > 0;
    },
    /**
     * Determines the width of trace link buttons.
     */
    style(): string {
      return this.children.length > 0 && this.parents.length > 0
        ? "max-width: 75px"
        : "max-width: 240px";
    },
    /**
     * Generates the name of the parent dropdown.
     */
    parentTitle(): string {
      const length = this.parents.length;

      return length === 1 ? "1 Parent" : `${length} Parents`;
    },
    /**
     * Generates the name of the child dropdown.
     */
    childTitle(): string {
      const length = this.children.length;

      return length === 1 ? "1 Child" : `${length} Children`;
    },
  },
  methods: {
    /**
     * Selects an artifact.
     * @param artifactName - The artifact to select.
     */
    handleArtifactClick(artifactName: string): void {
      const artifact = artifactStore.getArtifactByName(artifactName);

      if (!artifact) return;

      selectionStore.selectArtifact(artifact.id);
    },
    /**
     * Selects the trace link to an artifact.
     * @param artifactName - The artifact to select the link to.
     */
    handleTraceLinkClick(artifactName: string): void {
      const artifact = artifactStore.getArtifactByName(artifactName);

      if (!artifact || !this.artifact) return;

      const traceLink = traceStore.getTraceLinkByArtifacts(
        artifact.id,
        this.artifact.id,
        true
      );

      if (!traceLink) return;

      selectionStore.selectTraceLink(traceLink);
    },
    /**
     * Opens the create trace link panel with this artifact as the child.
     */
    handleLinkParent(): void {
      if (!this.artifact) return;

      appStore.openTraceCreatorTo({
        type: "source",
        artifactId: this.artifact.id,
      });
    },
    /**
     * Opens the create trace link panel with this artifact as the parent.
     */
    handleLinkChild(): void {
      if (!this.artifact) return;

      appStore.openTraceCreatorTo({
        type: "target",
        artifactId: this.artifact.id,
      });
    },
  },
});
</script>
