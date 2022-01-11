<template>
  <v-row class="ma-0 pa-0" justify="center">
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
          :is-disabled="definition.isDisabled"
        />
        <checkmark-menu v-else :definition="definition" />
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { ButtonDefinition, ButtonType, Artifact } from "@/types";
import { capitalize } from "@/util";
import {
  artifactSelectionModule,
  commitModule,
  projectModule,
  viewportModule,
} from "@/store";
import { GenericIconButton, CheckmarkMenu } from "@/components/common";
import { redoCommit, undoCommit } from "@/api";
import { cyZoomIn, cyZoomOut } from "@/cytoscape";

export default Vue.extend({
  components: {
    GenericIconButton,
    CheckmarkMenu,
  },
  data() {
    return {
      menuItems: [] as [string, boolean][], // label , persistent value
    };
  },
  methods: {
    async filterTypeHandler(index: number): Promise<void> {
      const [type, oldState] = this.menuItems[index];
      const newState = !oldState;
      // Changes to arrays not detected: https://vuejs.org/v2/guide/reactivity.html#Change-Detection-Caveats
      Vue.set(this.menuItems, index, [type, newState]);
      artifactSelectionModule
        .filterGraph({
          type: "ignore",
          ignoreType: type,
          action: newState ? "remove" : "add",
        })
        .then();
    },
    createMenuPersistentData(): [string, boolean][] {
      return Array.from(new Set(this.artifacts.map((a) => a.type))).map((i) => [
        i,
        true,
      ]);
    },
  },
  mounted() {
    this.menuItems = this.createMenuPersistentData();
  },
  watch: {
    artifacts(): void {
      this.menuItems = this.createMenuPersistentData();
    },
  },
  computed: {
    artifacts(): Artifact[] {
      return projectModule.artifacts;
    },
    definitions(): ButtonDefinition[] {
      // is computed because needs to react to changes to menuItems
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
          type: ButtonType.CHECKMARK_MENU,
          label: "Filter Artifacts",
          icon: "mdi-filter",
          menuItems: this.menuItems.map((i) => capitalize(i[0])),
          menuHandlers: this.menuItems.map(
            (item, itemIndex) => () => this.filterTypeHandler(itemIndex)
          ),
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
});
</script>
