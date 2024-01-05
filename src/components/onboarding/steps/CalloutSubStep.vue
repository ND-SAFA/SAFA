<template>
  <q-banner rounded class="bd-secondary q-mt-md">
    <template #avatar>
      <icon :variant="props.icon" color="secondary" size="md" />
    </template>
    <typography :value="props.message" />
    <template #action>
      <slot name="action" />
      <text-button
        v-if="!slots.action"
        text
        color="secondary"
        icon="calendar"
        @click="onboardingStore.handleScheduleCall"
      >
        Schedule a Call
      </text-button>
    </template>
  </q-banner>
</template>

<script lang="ts">
/**
 * A substep in the onboarding process that displays a callout message.
 */
export default {
  name: "CalloutSubStep",
};
</script>

<script setup lang="ts">
import { useSlots } from "vue";
import { IconVariant } from "@/types";
import { onboardingStore } from "@/hooks";
import { Icon, TextButton, Typography } from "@/components";

const props = defineProps<{ icon: IconVariant; message: string }>();

const slots = useSlots();
</script>
