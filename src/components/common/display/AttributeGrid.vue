<template>
  <grid-layout
    :layout="layout"
    :is-draggable="editable"
    :is-resizable="editable"
    :margin="[0, 0]"
    :col-num="2"
    :row-height="80"
  >
    <grid-item
      v-for="attribute of attributes"
      :key="attribute.key"
      :x="attribute.layout.x"
      :y="attribute.layout.y"
      :w="attribute.layout.w"
      :h="attribute.layout.h"
      :i="attribute.key"
    >
      <slot name="item" :attribute="attribute" />
    </grid-item>
  </grid-layout>
</template>

<script lang="ts">
import Vue from "vue";
import { GridLayout, GridItem, GridItemData } from "vue-grid-layout";
import { CustomAttributeModel } from "@/types";
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
     * @return All custom attributes in this project.
     */
    attributes(): CustomAttributeModel[] {
      return projectStore.project.attributes || [];
    },
    /**
     * @return The layout of custom attributes.
     */
    layout(): GridItemData[] {
      return this.attributes.map(({ key, layout }) => ({
        ...layout,
        i: key,
      }));
    },
  },
});
</script>
