<template>
  <modal title="Server Errors" :is-open="isOpen" @close="handleClose">
    <list :items="props.errors">
      <template #item="{ item }">
        <list-item>
          <code style="word-break: break-all">
            {{ item }}
          </code>
        </list-item>
      </template>
    </list>
  </modal>
</template>

<script lang="ts">
/**
 * Renders server errors.
 */
export default {
  name: "ServerErrorModal",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore } from "@/hooks";
import List from "@/components/common/display/list/List.vue";
import ListItem from "@/components/common/display/list/ListItem.vue";
import Modal from "./Modal.vue";

const props = defineProps<{
  /**
   * The errors to display.
   */
  errors: string[];
}>();

const isOpen = computed(() => appStore.isErrorDisplayOpen);

/**
 * Closes the error display.
 */
function handleClose() {
  appStore.toggleErrorDisplay();
}
</script>
