<template>
  <grid-layout
    :layout="gridLayout"
    :is-draggable="editable"
    :is-resizable="editable"
    :margin="[0, 20]"
    :col-num="2"
    :row-height="80"
    :vertical-compact="false"
  >
    <grid-item
      v-for="{ attr, pos } of attributeLayout"
      :key="pos.i"
      :x="pos.x"
      :y="pos.y"
      :w="pos.w"
      :h="pos.h"
      :i="pos.i"
      :is-draggable="!!editable && !!attr"
      :is-resizable="!!editable && !!attr"
      @moved="handleMoveEvent"
      @resized="handleResizeEvent"
    >
      <slot name="item" :attribute="attr" />
    </grid-item>
  </grid-layout>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GridLayout, GridItem, GridItemData } from "vue-grid-layout";
import { AttributeSchema, AttributeLayoutSchema } from "@/types";
import { attributesStore } from "@/hooks";

/**
 * Renders a grid of attributes.
 */
export default Vue.extend({
  name: "AttributeGrid",
  components: { GridLayout, GridItem },
  props: {
    editable: Boolean,
    layout: {
      type: Object as PropType<AttributeLayoutSchema>,
      required: true,
    },
  },
  data() {
    return {
      gridLayout: [] as GridItemData[],
    };
  },
  mounted() {
    this.resetLayout();
  },
  computed: {
    /**
     * @return All attributes and their positions in the active layout.
     */
    attributeLayout(): {
      attr: AttributeSchema | undefined;
      pos: GridItemData;
    }[] {
      return this.gridLayout.map((pos) => ({
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
      let maxY = 0;
      const gridLayout = this.layout.positions.map((pos) => {
        maxY = Math.max(pos.y, maxY);

        return {
          i: pos.key,
          x: pos.x,
          y: pos.y,
          w: pos.width,
          h: pos.height,
        };
      });

      if (this.editable) {
        gridLayout.push({
          i: "ADD-NEW-ATTRIBUTE",
          x: 0,
          y: gridLayout.length === 0 ? 0 : maxY + 1,
          w: 2,
          h: 1,
        });
      }

      this.gridLayout = gridLayout;
    },
    /**
     * Called when an attribute is moved.
     */
    handleMoveEvent(i: string, x: number, y: number) {
      const position = this.layout.positions.find(({ key }) => key === i);

      if (!position) return;

      position.x = x;
      position.y = y;
    },
    /**
     * Called when an attribute is resized.
     */
    handleResizeEvent(i: string, height: number, width: number) {
      const position = this.layout.positions.find(({ key }) => key === i);

      if (!position) return;

      position.height = height;
      position.width = width;
    },
  },
  watch: {
    /**
     * Resets the layout when the stored layout changes.
     */
    "layout.positions"() {
      this.resetLayout();
    },
  },
});
</script>
