<template>
  <attribute-grid v-if="layout" :layout="layout">
    <template #item="{ attribute }">
      <attribute-input
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
import { AttributeGrid } from "@/components/common/display";
import AttributeInput from "./AttributeInput.vue";

/**
 * A list of inputs for a list of generic attributes.
 */
export default defineComponent({
  name: "AttributeListInput",
  components: { AttributeGrid, AttributeInput },
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
  },
  watch: {
    artifact() {
      this.initializeArtifact();
    },
  },
  mounted() {
    this.initializeArtifact();
  },
  methods: {
    /**
     * Initializes the artifact's custom attributes.
     */
    initializeArtifact(): void {
      if (this.artifact.attributes) return;

      this.artifact.attributes = {};
    },
  },
});
</script>
