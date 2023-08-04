<template>
  <q-page class="bg-background full-height row items-center justify-center">
    <q-card flat bordered class="q-pa-sm card-page">
      <q-card-section class="q-pb-none">
        <div class="q-mx-auto width-max q-mb-md">
          <safa-icon />
        </div>
        <slot name="form" />
      </q-card-section>
      <q-card-actions class="q-px-md">
        <slot name="actions" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script lang="ts">
/**
 * Presents the page within a card containing SAFA title, a slot for a form,
 * and a slot for its actions.
 */
export default {
  name: "CardPage",
};
</script>

<script setup lang="ts">
import { SafaIcon } from "@/components/common/display";
</script>
