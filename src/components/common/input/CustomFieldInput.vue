<template>
  <div v-if="columns.length > 0">
    <typography el="h1" variant="subtitle" value="Custom Fields" />
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
import { ArtifactModel, ColumnModel } from "@/types";
import { documentModule } from "@/store";
import { Typography } from "@/components/common/display";
import SingleCustomFieldInput from "./SingleCustomFieldInput.vue";

/**
 * A set of inputs for all custom fields defined in the current document.
 *
 * @emits-1 `change:custom` - Called when a custom field is changed.
 */
export default Vue.extend({
  name: "CustomFieldInput",
  components: { SingleCustomFieldInput, Typography },
  props: {
    value: {
      type: Object as PropType<ArtifactModel>,
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
    columns(): ColumnModel[] {
      return documentModule.tableColumns;
    },
  },
});
</script>
