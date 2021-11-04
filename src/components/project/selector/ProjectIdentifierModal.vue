<template>
  <GenericModal
    :isOpen="isOpen"
    :title="title"
    size="s"
    :actionsHeight="50"
    @onClose="onClose"
  >
    <template v-slot:body>
      <ProjectCreator
        v-bind:name.sync="name"
        v-bind:description.sync="description"
      />
    </template>
    <template v-slot:actions>
      <v-container>
        <v-row justify="center">
          <v-btn @click="onSave" color="primary">
            <v-icon>mdi-check</v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import { ProjectIdentifier } from "@/types/domain/project";
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import ProjectCreator from "@/components/project/shared/ProjectIdentifierInput.vue";

export default Vue.extend({
  components: {
    GenericModal,
    ProjectCreator,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
    title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      name: "",
      description: "",
    };
  },
  mounted() {
    this.clearData();
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        if (this.project !== undefined) {
          this.name = this.project.name;
          this.description = this.project.description;
        } else {
          this.clearData();
        }
      }
    },
  },
  methods: {
    clearData() {
      this.name = "";
      this.description = "";
    },
    onClose() {
      this.$emit("onClose");
    },
    onSave() {
      const project: ProjectIdentifier | undefined = this.$props.project;
      const projectId = project === undefined ? "" : project.projectId;

      this.$emit("onSave", {
        projectId: projectId,
        name: this.name,
        description: this.description,
      } as ProjectIdentifier);
    },
  },
});
</script>
