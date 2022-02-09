<template>
  <v-select
    v-model="select"
    :items="items"
    label="Document"
    outlined
    color="secondary"
    dense
    hide-details
    dark
    style="width: 200px"
  >
    <template v-slot:item="{ item }">
      <v-row dense align="center">
        <v-col>
          {{ item }}
        </v-col>
        <v-col class="flex-grow-0">
          <generic-icon-button
            icon-id="mdi-dots-horizontal"
            :tooltip="`Edit ${item}`"
            @click="handleEdit(item)"
          />
        </v-col>
      </v-row>
    </template>
    <template v-slot:append-item>
      <v-btn text block color="primary" @click="handleAddDocument">
        <v-icon>mdi-plus</v-icon>
        Add Document
      </v-btn>
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import GenericIconButton from "@/components/common/generic/GenericIconButton.vue";

export default Vue.extend({
  name: "DocumentSelector",
  components: { GenericIconButton },
  data: () => ({
    select: "Default",
    items: ["Default", "Doc A", "Doc B"],
  }),
  watch: {
    select(item: string) {
      console.log(item);
    },
  },
  methods: {
    handleAddDocument() {
      console.log("Add Document");
    },
    handleEdit(item: string) {
      console.log("Edit", item);
    },
  },
});
</script>
