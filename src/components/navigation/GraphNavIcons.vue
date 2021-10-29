<template>
  <button-row :definitions="definitions" justify="center" />
</template>

<script lang="ts">
import Vue from "vue";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { ButtonDefinition, ButtonType } from "@/types/common-components";
import { Artifact } from "@/types/domain/artifact";
import { capitalize } from "@/util/string-helper";
import {
  artifactSelectionModule,
  projectModule,
  viewportModule,
} from "@/store";

export default Vue.extend({
  components: {
    ButtonRow,
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
      return projectModule.getArtifacts;
    },
    definitions(): ButtonDefinition[] {
      // is computed because needs to react to changes to menuItems
      return [
        {
          type: ButtonType.ICON,
          handler: () => viewportModule.onZoomIn(),
          label: "Zoom In",
          icon: "mdi-magnify-plus-outline",
        },
        {
          type: ButtonType.ICON,
          handler: () => viewportModule.onZoomOut(),
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
            await viewportModule.setGraphLayout();
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
      ];
    },
  },
});
</script>
