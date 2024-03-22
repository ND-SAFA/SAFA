<template>
  <q-expansion-item :label="props.label" :caption="props.caption">
    <template v-if="slots.icon" #header>
      <q-item-section avatar>
        <slot name="icon" />
      </q-item-section>

      <q-item-section data-cy="generic-list-item">
        {{ label }}
      </q-item-section>
    </template>
    <q-card class="q-my-md transparent">
      <slot />
    </q-card>
  </q-expansion-item>
</template>

<script lang="ts">
/**
 * A generic expansion item.
 */
export default {
  name: "ExpansionItem",
};
</script>

<script setup lang="ts">
import { useSlots } from "vue";
import { ExpansionItemProps } from "@/types";

const props = defineProps<ExpansionItemProps>();

const slots = useSlots();
</script>
