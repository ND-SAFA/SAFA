<template>
  <attribute-grid v-if="!!layout" :layout="layout">
    <template #item="{ attribute }">
      <attribute-input
        v-if="!!attribute"
        class="q-mr-sm q-pb-md"
        :attributes="attributes"
        :attribute="attribute"
        :data-cy="`input-attribute-${attribute.key}`"
      />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
/**
 * A list of inputs for a list of generic attributes.
 */
export default {
  name: "AttributeListInput",
};
</script>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { AttributeListInputProps } from "@/types";
import { attributesStore } from "@/hooks";
import { AttributeGrid } from "@/components/common/display";
import AttributeInput from "./AttributeInput.vue";

const props = defineProps<AttributeListInputProps>();

const layout = computed(() =>
  attributesStore.getLayoutByType(props.artifact.type)
);

const attributes = computed(() => props.artifact.attributes || {});

/**
 * Initializes the artifact's custom attributes.
 */
function initializeArtifact(): void {
  if (props.artifact.attributes) return;

  props.artifact.attributes = {};
}

onMounted(() => initializeArtifact());

watch(
  () => props.artifact,
  () => initializeArtifact()
);
</script>
