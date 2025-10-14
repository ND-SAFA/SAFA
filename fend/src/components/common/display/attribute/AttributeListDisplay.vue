<template>
  <attribute-grid v-if="doDisplay && !!layout" :layout="layout">
    <template #item="{ attribute }">
      <attribute-display
        v-if="!!attribute"
        show-name
        :values="attributes"
        :attribute="attribute"
      />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
/**
 * Displays a list of generic attributes.
 */
export default {
  name: "AttributeListDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { AttributeListProps } from "@/types";
import { attributesStore } from "@/hooks";
import AttributeGrid from "./AttributeGrid.vue";
import AttributeDisplay from "./AttributeDisplay.vue";

const props = defineProps<AttributeListProps>();

const attributes = computed(() => props.artifact.attributes || {});

const layout = computed(() =>
  attributesStore.getLayoutByType(props.artifact.type)
);

const doDisplay = computed(() => (layout.value?.positions.length || 0) > 0);
</script>
