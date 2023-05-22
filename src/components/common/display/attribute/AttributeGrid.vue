<template>
  <grid-layout
    v-if="editable"
    :layout="gridItemLayout"
    :is-draggable="true"
    :is-resizable="false"
    :margin="[20, 20]"
    :col-num="2"
    :row-height="100"
    :vertical-compact="false"
  >
    <template #default="{ gridItemProps }">
      <grid-item
        v-for="{ attr, pos } of attributeLayout"
        v-bind="gridItemProps"
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
    </template>
  </grid-layout>
  <div v-else>
    <flex-box
      v-for="(attrs, y) of staticLayout"
      :key="y"
      full-width
      justify="between"
    >
      <div v-if="attrs[0]" :class="attrs[1] ? 'width-50' : 'width-100'">
        <slot name="item" :attribute="attrs[0]" />
      </div>
      <div v-if="attrs[1]" class="width-50">
        <slot name="item" :attribute="attrs[1]" />
      </div>
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Renders a grid of attributes.
 */
export default {
  name: "AttributeGrid",
};
</script>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from "vue";
import { GridItem, GridLayout } from "vue3-drr-grid-layout";
import {
  AttributeSchema,
  AttributePositionSchema,
  GridItemData,
  AttributeGridProps,
} from "@/types";
import { attributesStore } from "@/hooks";
import { FlexBox } from "../content";

const props = defineProps<AttributeGridProps>();

const gridItemLayout = ref<GridItemData[]>([]);
const staticLayout = ref<(AttributeSchema | undefined)[][]>([]);

const attributeLayout = computed(() =>
  gridItemLayout.value.map((pos: GridItemData) => ({
    pos,
    attr: attributesStore.attributes.find(({ key }) => pos.i === key),
  }))
);

/**
 * Resets the layout to match the store.
 *
 * Creates 2 layout objects:
 * - `gridLayout` represents the layout data needed for editing the arrangement.
 * - `staticLayout` represents the ordered attributes to display when not editing.
 *    This second layout is necessary to get around the variable height limitations of the grid library.
 */
function resetLayout(): void {
  let maxY = 0;
  const attributesByY: Record<number, string[]> = {};

  gridItemLayout.value = props.layout.positions.map(
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

  staticLayout.value = Array.from(Array(maxY + 1)).map(
    (_, idx) =>
      attributesByY[idx]?.map((key) =>
        attributesStore.attributes.find((attr) => attr.key === key)
      ) || []
  );
}

/**
 * Called when an attribute is moved.
 */
function handleMoveEvent(i: string, x: number, y: number) {
  const position = props.layout.positions.find(
    ({ key }: AttributePositionSchema) => key === i
  );

  if (!position) return;

  position.x = x;
  position.y = y;
}

/**
 * Called when an attribute is resized.
 */
function handleResizeEvent(i: string, height: number, width: number) {
  const position = props.layout.positions.find(
    ({ key }: AttributePositionSchema) => key === i
  );

  if (!position) return;

  position.height = height;
  position.width = width;
}

onMounted(() => resetLayout());

watch(
  () => props.layout.positions.length,
  () => resetLayout()
);
</script>
