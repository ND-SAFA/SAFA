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
      :w="pos.w"
      :h="pos.h"
      :i="pos.i"
      @moved="(...args) => handleMoveEvent(pos, ...args)"
      @resized="(...args) => handleResizeEvent(pos, ...args)"
    >
      <slot name="item" :attribute="attr" />
    </grid-item>
  </grid-layout>
</template>

<script lang="ts">
import Vue from "vue";
import { GridLayout, GridItem, GridItemData } from "vue-grid-layout";
import { AttributeSchema, AttributePositionSchema } from "@/types";
import { attributesStore } from "@/hooks";
import { handleUpdateAttributeLayout } from "@/api/handlers/project/attribute-handler";

/**
 * Renders a grid of attributes.
 */
export default Vue.extend({
  name: "AttributeGrid",
  components: { GridLayout, GridItem },
  props: {
    editable: Boolean,
  },
  data() {
    return {
      layout: [] as GridItemData[],
    };
  },
  mounted() {
    this.resetLayout();
  },
  computed: {
    /**
     * @return The current layout to render.
     */
    currentLayout(): AttributePositionSchema[] {
      return attributesStore.defaultLayout;
    },
    /**
     * @return All attributes and their positions in the active layout.
     */
    attributeLayout(): {
      attr: AttributeSchema | undefined;
      pos: GridItemData;
    }[] {
      return this.layout.map((pos) => ({
        pos,
        attr: attributesStore.attributes.find(({ key }) => pos.i === key),
      }));
    },
  },
  methods: {
    /**
     * Resets the layout to match the store.
     */
    resetLayout(): void {
      this.layout = this.currentLayout.map((pos) => ({
        i: pos.key,
        x: pos.x,
        y: pos.y,
        w: pos.width,
        h: pos.height,
      }));
    },
    /**
     * Called when an attribute is moved.
     */
    handleMoveEvent(
      position: AttributePositionSchema,
      i: string,
      x: number,
      y: number
    ) {
      handleUpdateAttributeLayout(position, { x, y });
    },
    /**
     * Called when an attribute is resized.
     */
    handleResizeEvent(
      position: AttributePositionSchema,
      i: string,
      height: number,
      width: number
    ) {
      handleUpdateAttributeLayout(position, { height, width });
    },
  },
  watch: {
    /**
     * Resets the layout when the stored layout changes.
     */
    currentLayout() {
      this.resetLayout();
    },
  },
});
</script>
