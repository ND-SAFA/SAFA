<template>
  <GenericModal
    size="xs"
    :isOpen="deleteDialogue"
    :title="title"
    @onClose="onCancel"
    :actionsHeight="0"
  >
    <template v-slot:body>
      <v-container class="mt-5 mb-0 pb-0">
        <v-row justify="center">
          <v-btn color="error" @click="onConfirm"> Delete Version </v-btn>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import { ProjectVersion } from "@/types/domain/project";
import { versionToString } from "@/util/to-string";
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/modals/GenericModal.vue";
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
      this.$emit("onConfirmDelete", this.$props.version);
    },
    onCancel() {
      this.$emit("onCancelDelete");
    },
  },
  watch: {
    version(version: ProjectVersion) {
      this.title = `Delete version: ${versionToString(version)}`;
    },
  },
});
</script>
