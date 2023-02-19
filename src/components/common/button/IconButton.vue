<template>
  <q-btn
    :color="props.color"
    :fab="props.fab"
    :class="props.isDisabled ? 'disable-events' : ''"
    :size="size"
    :hidden="props.isHidden"
    :data-cy="props.dataCy"
    flat
    :round="!props.fab"
    @click="emit('click')"
  >
    <icon
      :style="props.iconStyle"
      :variant="props.icon"
      :rotate="props.rotate"
    />
    <q-tooltip :delay="200">
      {{ tooltip }}
    </q-tooltip>
  </q-btn>
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
import { computed } from "vue";
import { IconVariant } from "@/types";
import Icon from "@/components/common/display/icon/Icon.vue";

const props = defineProps<{
  dataCy?: string;
  tooltip: string;
  icon?: IconVariant;
  color?: string;
  iconStyle?: string;
  fab?: boolean;
  small?: boolean;
  large?: boolean;
  isDisabled?: boolean;
  isHidden?: boolean;
  rotate?: number;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const size = computed(() => {
  if (props.small) {
    return "sm";
  } else if (props.large) {
    return "lg";
  } else {
    return "";
  }
});
</script>
