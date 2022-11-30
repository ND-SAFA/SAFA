<template>
  <grid-layout
    :layout="layout"
    :is-draggable="editable"
    :is-resizable="editable"
    :margin="[0, 20]"
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
import { AttributeModel, AttributePositionModel } from "@/types";
import { attributesStore } from "@/hooks";

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
    currentLayout(): AttributePositionModel[] {
      return attributesStore.defaultLayout;
    },
    /**
     * @return The layout of custom attributes.
     */
    layout(): GridItemData[] {
      return this.currentLayout.map((pos) => ({
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
      return this.currentLayout.map((pos) => ({
        pos,
        attr: attributesStore.attributes.find(({ key }) => pos.key === key),
      }));
    },
  },
});
</script>
