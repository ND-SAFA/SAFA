<template>
  <attribute-grid :layout="layout">
    <template v-slot:item="{ attribute }">
      <attribute-input
        :model="artifact.attributes || {}"
        :attribute="attribute"
      />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactSchema, AttributeLayoutSchema } from "@/types";
import { attributesStore } from "@/hooks";
import { AttributeGrid } from "@/components/common/display";
import AttributeInput from "./AttributeInput.vue";

/**
 * A list of inputs for a list of generic attributes.
 */
export default Vue.extend({
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
    layout(): AttributeLayoutSchema {
      return attributesStore.getLayoutByType(this.artifact.type);
    },
  },
});
</script>
