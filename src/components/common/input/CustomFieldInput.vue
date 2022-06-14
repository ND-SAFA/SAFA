<template>
  <div>
    <h1 class="text-h6">Custom Fields</h1>
    <v-divider class="mb-2" />
    <single-custom-field-input
      v-for="column in columns"
      :column="column"
      :value="value"
      :key="column.id"
      @change:custom="$emit('change:custom')"
    />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, DocumentColumn } from "@/types";
import { documentModule } from "@/store";
import SingleCustomFieldInput from "./SingleCustomFieldInput.vue";

/**
 * A set of inputs for all custom fields defined in the current document.
 *
 * @emits-1 `change:custom` - Called when a custom field is changed.
 */
export default Vue.extend({
  name: "CustomFieldInput",
  components: { SingleCustomFieldInput },
  props: {
    value: {
      type: Object as PropType<Artifact>,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
      showPassword: false,
    };
  },
  computed: {
    /**
     * @return The current document columns.
     */
    columns(): DocumentColumn[] {
      return documentModule.tableColumns;
    },
  },
});
</script>
