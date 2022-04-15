<template>
  <v-row class="ma-0 pa-0" justify="center" style="flex-wrap: nowrap">
    <v-col
      v-for="definition in definitions"
      :key="definition.label"
      :cols="12 / definitions.length"
    >
      <v-row justify="center">
        <generic-icon-button
          v-if="definition.handler"
          color="secondary"
          :tooltip="definition.label"
          :icon-id="definition.icon"
          @click="definition.handler"
          :is-disabled="isButtonDisabled(definition)"
        />
        <checkmark-menu
          v-else
          :definition="definition"
          :is-disabled="isButtonDisabled(definition)"
        />
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import {
  artifactModule,
  artifactSelectionModule,
  commitModule,
  documentModule,
  viewportModule,
} from "@/store";
import { redoCommit, undoCommit } from "@/api";
import { cyZoomIn, cyZoomOut } from "@/cytoscape";
import { GenericIconButton, CheckmarkMenu } from "@/components/common";

export default Vue.extend({
  name: "GraphButtons",
  components: {
    GenericIconButton,
    CheckmarkMenu,
  },
  data() {
    return {
      menuItems: [] as [string, boolean][], // label , persistent value
    };
  },
  /**
   * Updates the graph button state on mount.
   */
  mounted() {
    this.menuItems = this.createMenuPersistentData();
  },
  computed: {
    /**
     * @return The visible project artifacts.
     */
    artifacts() {
      return artifactModule.artifacts;
    },
    /**
     * @return The graph button definitions to display.
     */
    definitions(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.ICON,
          handler: () => {
            undoCommit().then();
          },
          label: "Undo Commit",
          icon: "mdi-undo",
          isDisabled: !commitModule.canUndo,
        },
        {
          type: ButtonType.ICON,
          handler: () => cyZoomIn(),
          label: "Zoom In",
          icon: "mdi-magnify-plus-outline",
        },
        {
          type: ButtonType.ICON,
          handler: () => cyZoomOut(),
          label: "Zoom Out",
          icon: "mdi-magnify-minus-outline",
        },
        {
          type: ButtonType.ICON,
          handler: async () => {
            await artifactSelectionModule.filterGraph({
              type: "subtree",
              artifactsInSubtree: [],
            });
          },
          label: "Center Graph",
          icon: "mdi-graphql",
        },
        {
          type: ButtonType.ICON,
          handler: viewportModule.setArtifactTreeLayout,
          label: "Reformat Graph",
          icon: "mdi-refresh",
        },
        {
          type: ButtonType.CHECKMARK_MENU,
          label: "Filter Artifacts",
          icon: "mdi-filter",
          menuItems: this.menuItems.map(([name], itemIndex) => ({
            name,
            onClick: () => this.filterTypeHandler(itemIndex),
          })),
          checkmarkValues: this.menuItems.map((i) => i[1]),
        },
        {
          type: ButtonType.ICON,
          handler: () => redoCommit().then(),
          label: "Redo Commit",
          icon: "mdi-redo",
          isDisabled: !commitModule.canRedo,
        },
      ];
    },
  },
  methods: {
    /**
     * @return Whether to disable a graph button.
     */
    isButtonDisabled(button: ButtonDefinition): boolean {
      return button.isDisabled || documentModule.isTableDocument;
    },
    /**
     * Filters the visible artifacts on the graph.
     */
    filterTypeHandler(index: number) {
      const [type, oldState] = this.menuItems[index];
      const newState = !oldState;

      Vue.set(this.menuItems, index, [type, newState]);

      artifactSelectionModule.filterGraph({
        type: "ignore",
        ignoreType: type,
        action: newState ? "remove" : "add",
      });
    },
    /**
     * Creates saved state for the graph menu items.
     */
    createMenuPersistentData(): [string, boolean][] {
      return Array.from(new Set(this.artifacts.map((a) => a.type))).map((i) => [
        i,
        true,
      ]);
    },
  },
  watch: {
    /**
     * Updates the graph button state when artifacts change
     */
    artifacts(): void {
      this.menuItems = this.createMenuPersistentData();
    },
  },
});
</script>
