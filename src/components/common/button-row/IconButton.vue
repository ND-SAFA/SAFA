<template>
  <v-btn
    :icon="definition.type !== 'text'"
    :text="definition.type === 'text'"
    small
    color="secondary"
    @click="definition.handler"
    class="mr-2"
    :disabled="true"
  >
    <v-icon v-if="definition.type === 'icon'">
      {{ definition.icon }}
    </v-icon>
    <label v-else>{{ definition.label }}</label>
  </v-btn>
</template>

<script lang="ts">
import { IconDefinition } from "@/types";
import Vue, { PropType } from "vue";

export default Vue.extend({
  props: {
    definition: {
      type: Object as PropType<IconDefinition>,
      required: true,
    },
  },
  computed: {
    isDisabled() {
      const def: IconDefinition = this.definition;
      return def.isDisabled === undefined ? false : def.isDisabled;
    },
  },
});
</script>
