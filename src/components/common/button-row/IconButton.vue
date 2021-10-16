<template>
  <v-btn
    :icon="definition.type !== 'text'"
    :text="definition.type === 'text'"
    small
    color="secondary"
    @click="definition.handler"
    class="mr-2"
  >
    <v-icon v-if="definition.type === 'icon'">
      {{ definition.icon }}
    </v-icon>
    <label v-else>{{ definition.label }}</label>
  </v-btn>
</template>

<script lang="ts">
import { ButtonDefinition } from "@/types/common-components";
import Vue, { PropType } from "vue";
export default Vue.extend({
  props: {
    definition: Object as PropType<ButtonDefinition>,
  },
});
</script>
