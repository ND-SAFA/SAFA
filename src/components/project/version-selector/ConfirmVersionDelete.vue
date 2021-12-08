<template>
  <generic-modal
    size="xxs"
    :is-open="deleteDialogue"
    :title="title"
    @close="onCancel"
    :actions-height="0"
  >
    <template v-slot:body>
      <v-btn color="error" @click="onConfirm" block class="mt-3">Delete</v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectVersion } from "@/types";
import { versionToString } from "@/util";
import { GenericModal } from "@/components/common";

/**
 * A modal for confirming version deletion.
 *
 * @emits-1 `confirm` (ProjectVersion) - On delete confirm.
 * @emits-2 `cancel` - On delete cancel.
 */
export default Vue.extend({
  components: { GenericModal },
  props: {
    deleteDialogue: {
      type: Boolean,
      required: true,
    },
    version: {
      type: Object as PropType<ProjectVersion>,
      required: false,
    },
  },
  data() {
    return {
      title: "",
    };
  },
  methods: {
    onConfirm() {
      this.$emit("confirm", this.$props.version);
    },
    onCancel() {
      this.$emit("cancel");
    },
  },
  watch: {
    version(version: ProjectVersion) {
      this.title = `Delete version: ${versionToString(version)}`;
    },
  },
});
</script>
