<template>
  <v-tooltip bottom z-index="10000">
    <template #activator="{ props }">
      <v-btn
        v-bind="props"
        :color="color"
        :icon="!fab"
        :fab="fab"
        :class="isDisabled ? 'disable-events' : ''"
        :small="small"
        :large="large"
        :hidden="isHidden"
        :data-cy="dataCy"
        variant="text"
        @click.native="emit('click')"
      >
        <v-icon :style="iconStyle">{{ iconId }}</v-icon>
      </v-btn>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script lang="ts">
/**
 * A generic icon button.
 */
export default {
  name: "IconButton",
};
</script>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from "vue";

const props = defineProps<{
  dataCy?: string;
  tooltip: string;
  iconId: string;
  color?: string;
  iconStyle?: string;
  fab?: boolean;
  small?: boolean;
  large?: boolean;
  isDisabled?: boolean;
  isHidden?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const isDisabled = computed(() => props.isDisabled || false);
</script>
