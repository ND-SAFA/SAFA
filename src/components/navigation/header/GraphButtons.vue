<template>
  <flex-box>
    <v-divider inset vertical class="white mx-1 faded" />

    <template v-for="definition in changeButtons">
      <generic-icon-button
        v-if="definition.handler"
        :key="definition.label"
        color="white"
        :tooltip="definition.label"
        :icon-id="definition.icon"
        :is-disabled="isButtonDisabled(definition)"
        :data-cy="definition.dataCy"
        @click="definition.handler"
      />
    </template>

    <v-divider inset vertical class="white mx-1 faded" />

    <template v-for="definition in viewButtons">
      <generic-icon-button
        v-if="definition.handler"
        :key="definition.label"
        color="white"
        :tooltip="definition.label"
        :icon-id="definition.icon"
        :is-disabled="isButtonDisabled(definition)"
        :data-cy="definition.dataCy"
        @click="definition.handler"
      />
    </template>

    <v-divider inset vertical class="white mx-1 faded" />

    <checkmark-menu
      :key="filterButton.label"
      :definition="filterButton"
      :is-disabled="isButtonDisabled(filterButton)"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import {
  artifactStore,
  documentStore,
  commitStore,
  selectionStore,
  layoutStore,
} from "@/hooks";
import { redoCommit, undoCommit } from "@/api";
import { cyZoomIn, cyZoomOut } from "@/cytoscape";
import { GenericIconButton, CheckmarkMenu, FlexBox } from "@/components/common";

export default Vue.extend({
  name: "GraphButtons",
  components: {
    FlexBox,
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
      return artifactStore.currentArtifacts;
    },
    /**
     * @return The change buttons.
     */
    changeButtons(): ButtonDefinition[] {
      return [
        {
          type: ButtonType.ICON,
          handler: () => {
            undoCommit().then();
          },
          label: "Undo",
          icon: "mdi-undo",
          isDisabled: !commitStore.canUndo,
        },
        {
          type: ButtonType.ICON,
          handler: () => redoCommit().then(),
          label: "Redo",
          icon: "mdi-redo",
          isDisabled: !commitStore.canRedo,
        },
      ];
    },
    /**
     * @return The view buttons.
     */
    viewButtons(): ButtonDefinition[] {
      return [
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
          handler: () => {
            selectionStore.filterGraph({
              type: "subtree",
              artifactsInSubtree: [],
            });
          },
          label: "Center Graph",
          icon: "mdi-graphql",
          dataCy: "button-nav-graph=center",
        },
        {
          type: ButtonType.ICON,
          handler: layoutStore.setArtifactTreeLayout,
          label: "Reformat Graph",
          icon: "mdi-refresh",
        },
      ];
    },
    /**
     * @return The filter button.
     */
    filterButton(): ButtonDefinition {
      return {
        type: ButtonType.CHECKMARK_MENU,
        label: "Filter Artifacts",
        icon: "mdi-filter",
        menuItems: this.menuItems.map(([name], itemIndex) => ({
          name,
          onClick: () => this.filterTypeHandler(itemIndex),
        })),
        checkmarkValues: this.menuItems.map((i) => i[1]),
      };
    },
  },
  methods: {
    /**
     * @return Whether to disable a graph button.
     */
    isButtonDisabled(button: ButtonDefinition): boolean {
      return button.isDisabled || documentStore.isTableDocument;
    },
    /**
     * Filters the visible artifacts on the graph.
     */
    filterTypeHandler(index: number) {
      const [type, oldState] = this.menuItems[index];
      const newState = !oldState;

      Vue.set(this.menuItems, index, [type, newState]);

      selectionStore.filterGraph({
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
