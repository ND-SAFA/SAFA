<template>
  <grid-layout
    :layout="layout"
    :is-draggable="editable"
    :is-resizable="editable"
    :margin="[0, 0]"
    :col-num="2"
    :row-height="80"
    :vertical-compact="false"
  >
    <grid-item
      v-for="{ attr, pos } of attributeLayout"
      :key="attr.key"
      :x="pos.x"
      :y="pos.y"
      :w="pos.width"
      :h="pos.height"
      :i="pos.key"
    >
      <slot name="item" :attribute="attr" />
    </grid-item>
  </grid-layout>
</template>

<script lang="ts">
import Vue from "vue";
import { GridLayout, GridItem, GridItemData } from "vue-grid-layout";
import {
  AttributeLayoutModel,
  AttributeModel,
  AttributePositionModel,
} from "@/types";
import { projectStore } from "@/hooks";

/**
 * Renders a grid of attributes.
 */
export default Vue.extend({
  name: "AttributeGrid",
  components: { GridLayout, GridItem },
  props: {
    editable: Boolean,
  },
  computed: {
    /**
     * @return The current layout to render.
     */
    currentLayout(): AttributeLayoutModel {
      return (
        projectStore.project.attributes?.layouts[0] || {
          id: "default",
          artifactTypes: [],
          positions: [],
        }
      );
    },
    /**
     * @return All custom attributes in this project.
     */
    attributes(): AttributeModel[] {
      return projectStore.project.attributes?.items || [];
    },
    /**
     * @return The layout of custom attributes.
     */
    layout(): GridItemData[] {
      return this.currentLayout.positions.map((pos) => ({
        i: pos.key,
        x: pos.x,
        y: pos.y,
        w: pos.width,
        h: pos.height,
      }));
    },
    /**
     * @return All attributes and their positions in the active layout.
     */
    attributeLayout(): {
      attr: AttributeModel | undefined;
      pos: AttributePositionModel;
    }[] {
      return this.currentLayout.positions.map((pos) => ({
        pos,
        attr: this.attributes.find(({ key }) => pos.key === key),
      }));
    },
  },
});
</script>
