<template>
  <q-page
    v-if="doDisplay"
    class="bg-background"
    :padding="!props.fullWindow"
    :style-fn="() => style"
  >
    <slot />
  </q-page>
  <q-page v-else>
    <div class="full-width" style="margin-top: 40vh">
      <div class="q-mx-auto width-fit">
        <q-circular-progress
          rounded
          indeterminate
          size="60px"
          :thickness="0.2"
          color="primary"
        />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
/**
 * Displays a page with top and sidebars.
 */
export default {
  name: "PrivatePage",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { sessionStore } from "@/hooks";

const props = defineProps<{
  fullWindow?: boolean;
}>();

const doDisplay = computed(() => sessionStore.doesSessionExist);
const style = computed(() =>
  props.fullWindow ? "" : "padding-left: 10vw; padding-right: 10vw"
);
</script>
