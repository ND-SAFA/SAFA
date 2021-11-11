<template>
  <generic-modal
    title="Server Errors"
    :isOpen="isOpen"
    :actionsHeight="0"
    :isLoading="isLoading"
    @close="onClose"
  >
    <template v-slot:body>
      <v-list disabled>
        <v-list-item v-for="(error, errorIndex) in errors" :key="errorIndex">
          <v-list-item-content class="pa-0">
            <code class="word-break-all">
              {{ error }}
            </code>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { PanelType } from "@/types";
import { appModule } from "@/store";
import { GenericModal } from "@/components/common/generic";

export default Vue.extend({
  components: {
    GenericModal,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  props: {
    isOpen: Boolean,
    errors: Array as PropType<string[]>,
  },
  methods: {
    onClose() {
      appModule.closePanel(PanelType.errorDisplay);
    },
  },
});
</script>
