<template>
  <q-expansion-item :label="props.label" :caption="props.caption">
    <template v-if="slots.icon" #header>
      <q-item-section avatar>
        <slot name="icon" />
      </q-item-section>

      <q-item-section>
        {{ label }}
      </q-item-section>
    </template>
    <q-card class="q-my-md">
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

const props = defineProps<{
  label: string;
  caption?: string;
}>();

const slots = useSlots();
</script>
