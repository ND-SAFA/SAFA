<template>
  <q-drawer
    model-value
    persistent
    bordered
    :breakpoint="0"
    :width="260"
    class="bg-background"
  >
    <flex-box full-width justify="between" align="center" t="1" class="q-pa-sm">
      <typography variant="subtitle" value="Chats" />
      <text-button
        text
        :disabled="chatApiStore.loading"
        label="Create"
        icon="add"
        data-cy="button-add-attribute"
        @click="chatStore.addChat()"
      />
    </flex-box>
    <list-item
      v-for="chat in chatStore.chats"
      :key="chat.id"
      :title="chat.title"
      :clickable="!chatApiStore.loading"
      :focused="chatStore.currentChat?.id === chat.id"
      :action-cols="1"
      @click="chatApiStore.handleLoadProjectChatMessages(chat)"
    >
      <template #actions>
        <icon-button
          small
          icon="delete"
          tooltip="Delete chat"
          @click="chatApiStore.handleDeleteProjectChat(chat.id)"
        />
      </template>
    </list-item>
  </q-drawer>
</template>

<script lang="ts">
/**
 * Displays a list of chats for the current project.
 */
export default {
  name: "ProjectChatList",
};
</script>

<script setup lang="ts">
import { chatApiStore, chatStore } from "@/hooks";
import {
  IconButton,
  ListItem,
  Typography,
  FlexBox,
  TextButton,
} from "@/components/common";
</script>
