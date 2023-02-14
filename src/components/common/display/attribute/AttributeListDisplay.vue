<template>
  <attribute-grid v-if="doDisplay" :layout="layout">
    <template #item="{ attribute }">
      <attribute-display
        :model="artifact.attributes || {}"
        :attribute="attribute"
      />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { ArtifactSchema, AttributeLayoutSchema } from "@/types";
import { attributesStore } from "@/hooks";
import AttributeGrid from "./AttributeGrid.vue";
import AttributeDisplay from "./AttributeDisplay.vue";

/**
 * Displays a list of generic attributes.
 */
export default defineComponent({
  name: "AttributeListDisplay",
  components: { AttributeDisplay, AttributeGrid },
  props: {
    artifact: {
      type: Object as PropType<ArtifactSchema>,
      required: true,
    },
  },
  computed: {
    /**
     * @return The layout for this artifact.
     */
    layout(): AttributeLayoutSchema | undefined {
      return attributesStore.getLayoutByType(this.artifact.type);
    },
    /**
     * @return Whether the attribute list should be displayed.
     */
    doDisplay(): boolean {
      return !!this.layout && this.layout.positions.length > 0;
    },
  },
});
</script>
