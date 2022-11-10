<template>
  <panel-card v-if="doDisplay">
    <flex-box justify="space-between">
      <typography el="h2" l="1" variant="subtitle" value="Trace Links" />
      <v-icon color="primary" style="transform: rotate(-45deg)">
        mdi-ray-start-arrow
      </v-icon>
    </flex-box>

    <v-divider />

    <v-list expand>
      <toggle-list
        v-if="parents.length > 0"
        :title="parentTitle"
        data-cy="list-selected-parents"
      >
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
          <template v-for="parent in parents">
            <v-list-item
              :key="parent.id"
              data-cy="list-selected-parent-item"
              @click="handleArtifactClick(parent.name)"
            >
              <v-list-item-title>
                <generic-artifact-body-display
                  display-title
                  :artifact="parent"
                />
              </v-list-item-title>
              <v-list-item-action @click.stop="">
                <generic-icon-button
                  icon-id="mdi-ray-start-end"
                  tooltip="View Trace Link"
                  data-cy="button-selected-parent-link"
                  @click="handleTraceLinkClick(parent.name)"
                />
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
      </toggle-list>
      <toggle-list
        v-if="children.length > 0"
        :title="childTitle"
        data-cy="list-selected-children"
      >
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
          <template v-for="child in children">
            <v-list-item
              :key="child.name"
              data-cy="list-selected-child-item"
              @click="handleArtifactClick(child.name)"
            >
              <v-list-item-title>
                <generic-artifact-body-display
                  display-title
                  :artifact="child"
                />
              </v-list-item-title>
              <v-list-item-action @click.stop="">
                <generic-icon-button
                  icon-id="mdi-ray-start-end"
                  tooltip="View Trace Link"
                  data-cy="button-selected-child-link"
                  @click="handleTraceLinkClick(child.name)"
                />
              </v-list-item-action>
            </v-list-item>
          </template>
        </v-list>
      </toggle-list>
    </v-list>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, ListItem } from "@/types";
import {
  artifactStore,
  selectionStore,
  subtreeStore,
  traceStore,
} from "@/hooks";
import {
  GenericListItem,
  Typography,
  FlexBox,
  ToggleList,
  GenericIconButton,
  PanelCard,
} from "@/components/common";
import GenericArtifactBodyDisplay from "@/components/common/generic/GenericArtifactBodyDisplay.vue";

/**
 * Displays the selected node's parents and children.
 */
export default Vue.extend({
  name: "ArtifactTraces",
  components: {
    GenericArtifactBodyDisplay,
    PanelCard,
    GenericIconButton,
    FlexBox,
    Typography,
    GenericListItem,
    ToggleList,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's parents.
     */
    parents(): ArtifactModel[] {
      if (!this.selectedArtifact) return [];

      return subtreeStore
        .getParents(this.selectedArtifact.id)
        .map((id) => artifactStore.getArtifactById(id)) as ArtifactModel[];
    },
    /**
     * @return The selected artifact's children.
     */
    children(): ArtifactModel[] {
      if (!this.selectedArtifact) return [];

      return subtreeStore
        .getChildren(this.selectedArtifact.id)
        .map((id) => artifactStore.getArtifactById(id)) as ArtifactModel[];
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

      if (!artifact || !this.selectedArtifact) return;

      const traceLink = traceStore.getTraceLinkByArtifacts(
        artifact.id,
        this.selectedArtifact.id,
        true
      );

      if (!traceLink) return;

      selectionStore.selectTraceLink(traceLink);
    },
  },
});
</script>
