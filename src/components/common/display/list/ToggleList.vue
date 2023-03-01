<template>
  <list>
    <expansion-item
      :label="props.title"
      data-cy="generic-list-item"
      @click="$emit('click')"
    >
      <template v-if="slots.icon" #icon>
        <slot name="icon" />
      </template>
      <separator class="faded" />
      <slot />
      <separator class="faded" />
    </expansion-item>
  </list>
</template>

<script lang="ts">
/**
 * Displays a toggleable list.
 *
 * @emits-1 `click` - On activator click.
 */
export default {
  name: "ToggleList",
};
</script>

<script setup lang="ts">
import { useSlots } from "vue";
import ExpansionItem from "@/components/common/layout/ExpansionItem.vue";
import Separator from "../Separator.vue";
import List from "./List.vue";

const props = defineProps<{
  title: string;
}>();

defineEmits<{
  (e: "click"): void;
}>();

const slots = useSlots();
</script>
