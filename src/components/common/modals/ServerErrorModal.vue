<template>
  <GenericModal
    title="Server Errors"
    :isOpen="isOpen"
    :actionsHeight="0"
    :isLoading="isLoading"
    @onClose="onClose"
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
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import { appModule } from "@/store";
import { PanelType } from "@/types";

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
