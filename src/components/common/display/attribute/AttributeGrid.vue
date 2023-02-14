<template>
  <grid-layout
    v-if="editable"
    :layout="gridLayout"
    :is-draggable="true"
    :is-resizable="false"
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
      :is-draggable="!!attr"
      :is-resizable="false"
      @moved="handleMoveEvent"
      @resized="handleResizeEvent"
    >
      <slot name="item" :attribute="attr" />
    </grid-item>
  </grid-layout>
  <div v-else>
    <flex-box
      v-for="(attrs, y) of staticLayout"
      :key="y"
      full-width
      justify="space-between"
    >
      <div v-if="attrs[0]" :style="attrs[1] ? 'width: 50%' : 'width: 100%'">
        <slot name="item" :attribute="attrs[0]" />
      </div>
      <div v-if="attrs[1]" style="width: 50%">
        <slot name="item" :attribute="attrs[1]" />
      </div>
    </flex-box>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { GridLayout, GridItem, GridItemData } from "vue-grid-layout";
import {
  AttributeSchema,
  AttributeLayoutSchema,
  AttributePositionSchema,
} from "@/types";
import { attributesStore } from "@/hooks";
import { FlexBox } from "@/components/common/layout";

/**
 * Renders a grid of attributes.
 */
export default defineComponent({
  name: "AttributeGrid",
  components: { FlexBox, GridLayout, GridItem },
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
      staticLayout: [] as (AttributeSchema | undefined)[][],
    };
  },
  computed: {
    /**
     * @return All attributes and their positions in the active layout.
     */
    attributeLayout(): {
      attr: AttributeSchema | undefined;
      pos: GridItemData;
    }[] {
      return this.gridLayout.map((pos: GridItemData) => ({
        pos,
        attr: attributesStore.attributes.find(({ key }) => pos.i === key),
      }));
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
  mounted() {
    this.resetLayout();
  },
  methods: {
    /**
     * Resets the layout to match the store.
     *
     * Creates 2 layout objects:
     * - `gridLayout` represents the layout data needed for editing the arrangement.
     * - `staticLayout` represents the ordered attributes to display when not editing.
     *    This second layout is necessary to get around the variable height limitations of the grid library.
     */
    resetLayout(): void {
      let maxY = 0;
      const attributesByY: Record<number, string[]> = {};

      this.gridLayout = this.layout.positions.map(
        (pos: AttributePositionSchema) => {
          maxY = Math.max(pos.y, maxY);

          if (!attributesByY[pos.y]) attributesByY[pos.y] = [];

          if (pos.x === 0) {
            attributesByY[pos.y] = [pos.key, attributesByY[pos.y][1]];
          } else {
            attributesByY[pos.y] = [attributesByY[pos.y][0], pos.key];
          }

          return {
            i: pos.key,
            x: pos.x,
            y: pos.y,
            w: pos.width,
            h: pos.height,
          };
        }
      );

      this.staticLayout = Array.from(Array(maxY + 1)).map(
        (_, idx) =>
          attributesByY[idx]?.map((key) =>
            attributesStore.attributes.find((attr) => attr.key === key)
          ) || []
      );
    },
    /**
     * Called when an attribute is moved.
     */
    handleMoveEvent(i: string, x: number, y: number) {
      const position = this.layout.positions.find(
        ({ key }: AttributePositionSchema) => key === i
      );

      if (!position) return;

      position.x = x;
      position.y = y;
    },
    /**
     * Called when an attribute is resized.
     */
    handleResizeEvent(i: string, height: number, width: number) {
      const position = this.layout.positions.find(
        ({ key }: AttributePositionSchema) => key === i
      );

      if (!position) return;

      position.height = height;
      position.width = width;
    },
  },
});
</script>
