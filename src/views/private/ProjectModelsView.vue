<template>
  <private-page>
    <template v-slot:page>
      <back-button />
      <typography el="h1" variant="title" value="Project Models" />
      <v-divider />
      <under-construction-alert />
      <generic-selector
        is-open
        show-expand
        :has-select="false"
        :headers="headers"
        :items="items"
        item-key="id"
        class="model-table mt-5"
        @item:add="handleAdd"
        @item:edit="handleEdit"
        @item:delete="handleDelete"
        @refresh="handleRefresh"
      >
        <template v-slot:expanded-item="{ item }">
          <div class="my-2">
            <typography
              el="h2"
              variant="subtitle"
              value="Default Trace Directions"
            />
            <flex-box
              v-for="(direction, idx) in item.defaultTraceDirections"
              :key="idx"
            >
              <attribute-chip artifact-type :value="direction.source" />
              <v-icon>mdi-arrow-right</v-icon>
              <attribute-chip artifact-type :value="direction.target" />
            </flex-box>
            <typography
              t="2"
              el="h2"
              variant="subtitle"
              value="Training Runs"
            />
            <typography secondary value="There are no training runs." />
            <typography
              t="2"
              el="h2"
              variant="subtitle"
              value="Evaluation Runs"
            />
            <typography secondary value="There are no evaluation runs." />
          </div>
        </template>
      </generic-selector>
      <generic-modal
        :is-open="isAddOpen || isEditOpen"
        :title="modelTitle"
        @close="handleClose"
      >
        <template v-slot:body>
          <flex-box t="4">
            <v-text-field
              filled
              v-model="currentName"
              label="Model Name"
              class="mr-1"
              hide-details
            />
            <gen-method-input
              only-trainable
              v-model="currentModel"
              style="max-width: 200px"
            />
          </flex-box>
        </template>
        <template v-slot:actions>
          <v-spacer />
          <v-btn :disabled="isSaveDisabled" color="primary" @click="handleSave">
            Save
          </v-btn>
        </template>
      </generic-modal>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { ConfirmationType, ModelType } from "@/types";
import { logStore } from "@/hooks";
import {
  BackButton,
  GenericModal,
  GenericSelector,
  GenMethodInput,
  PrivatePage,
  Typography,
  FlexBox,
  UnderConstructionAlert,
  AttributeChip,
} from "@/components";

interface GenModel {
  id: number;
  name: string;
  model: ModelType;
  defaultTraceDirections: {
    source: string;
    target: string;
  }[];
}

const testItems = (): GenModel[] => [
  {
    id: 1,
    name: "My Natural Language Model",
    model: ModelType.NLBert,
    defaultTraceDirections: [{ source: "Requirements", target: "Hazards" }],
  },
  {
    id: 2,
    name: "My Code Model",
    model: ModelType.PLBert,
    defaultTraceDirections: [{ source: "Code", target: "Requirements" }],
  },
];

/**
 * Displays project models.
 */
export default Vue.extend({
  name: "ProjectModelsView",
  components: {
    AttributeChip,
    UnderConstructionAlert,
    FlexBox,
    GenMethodInput,
    GenericModal,
    GenericSelector,
    Typography,
    BackButton,
    PrivatePage,
  },
  data() {
    return {
      isAddOpen: false,
      isEditOpen: false,
      headers: [
        { text: "Name", value: "name" },
        { text: "Model", value: "model" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      items: testItems(),
      currentItem: undefined as GenModel | undefined,
    };
  },
  computed: {
    modelTitle(): string {
      if (this.isAddOpen) {
        return "Create Model";
      } else {
        return "Edit Model";
      }
    },
    isSaveDisabled(): boolean {
      return (this.currentItem?.name.length || 0) === 0;
    },
    currentName: {
      get(): string {
        return this.currentItem?.name || "";
      },
      set(newName: string) {
        if (!this.currentItem) return;

        this.currentItem.name = newName;
      },
    },
    currentModel: {
      get(): ModelType {
        return this.currentItem?.model || ModelType.NLBert;
      },
      set(newModel: ModelType) {
        if (!this.currentItem) return;

        this.currentItem.model = newModel;
      },
    },
  },
  methods: {
    handleClose() {
      this.isAddOpen = false;
      this.isEditOpen = false;
    },
    handleAdd() {
      this.currentItem = {
        id: (this.items[this.items.length - 1]?.id || 0) + 1,
        name: "",
        model: ModelType.NLBert,
        defaultTraceDirections: [],
      };
      this.isAddOpen = true;
    },
    handleEdit(item: GenModel) {
      this.currentItem = item;
      this.isEditOpen = true;
    },
    handleDelete(item: GenModel) {
      logStore.$patch({
        confirmation: {
          type: ConfirmationType.INFO,
          title: "Delete Model",
          body: `Are you sure you want to delete "${item.name}"?`,
          statusCallback: (isConfirmed: boolean) => {
            if (!isConfirmed) return;

            this.items = this.items.filter(({ id }) => item.id !== id);
          },
        },
      });
    },
    handleSave() {
      if (!this.currentItem) return;

      const matchingIdx = this.items.indexOf(this.currentItem);

      if (matchingIdx !== -1) {
        Vue.set(this.items, matchingIdx, this.currentItem);
      } else {
        this.items.push(this.currentItem);
      }

      this.currentItem = undefined;
      this.handleClose();
    },
    handleRefresh() {
      this.items = testItems();
    },
  },
});
</script>
