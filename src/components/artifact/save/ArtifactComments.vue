<template>
  <panel-card
    v-if="permissionStore.isNASA"
    borderless
    collapsable
    title="Feedback"
  >
    <template #title-actions>
      <text-button
        :label="showResolved ? 'Hide Resolved' : 'Show Resolved'"
        icon="comment-resolve"
        text
        small
        @click="showResolved = !showResolved"
      />
    </template>

    <list-item
      v-for="comment in allComments"
      :key="comment.id"
      dense
      :class="
        comment.type === 'flag'
          ? 'artifact-comment artifact-flag'
          : 'artifact-comment'
      "
      :action-cols="3"
    >
      <popup-edit-input
        :value="editedComment ? editedComment.content : ''"
        multiline
        full-width
        :editing="editedComment && editedComment.id === comment.id"
        @open="handleEditComment(comment)"
        @close="handleCloseEditedComment"
        @save="handleSaveEditedComment"
      >
        <template #icon>
          <icon
            :variant="comment.type === 'flag' ? 'flag' : 'account'"
            size="sm"
            class="q-mr-md"
            :color="comment.type === 'flag' ? 'secondary' : undefined"
          />
        </template>
        <typography :value="comment.userId" />
        <typography
          secondary
          small
          :value="timestampToDisplay(comment.updatedAt)"
          l="2"
          ellipsis
        />
        <template #actions>
          <icon-button
            v-if="comment.status !== 'resolved'"
            small
            icon="comment-resolve"
            color="text"
            tooltip="Resolve"
            @click="handleResolveComment(comment)"
          />
          <icon-button
            v-if="comment.status !== 'resolved'"
            small
            icon="delete"
            tooltip="Delete"
            @click="handleDeleteComment(comment)"
          />
          <icon-button
            v-if="comment.status === 'resolved'"
            small
            icon="comment"
            color="text"
            class="show-on-hover-child"
            tooltip="Unresolve"
            @click="handleResolveComment(comment)"
          />
          <typography
            v-if="comment.status === 'resolved'"
            secondary
            small
            value="Resolved"
            l="1"
          />
        </template>
        <template #body>
          <typography :value="comment.content" el="p" />
        </template>
      </popup-edit-input>
    </list-item>

    <q-input
      v-model="newComment"
      autogrow
      type="textarea"
      placeholder="Add a comment..."
      class="q-ml-md bd-transparent"
    >
      <template #before>
        <icon variant="account" size="sm" />
      </template>
      <template #append>
        <q-btn-dropdown
          flat
          auto-close
          dense
          size="sm"
          :icon="commentType === 'conversation' ? 'comment' : 'flag'"
        >
          <flex-box column>
            <text-button
              label="Comment"
              icon="comment"
              small
              text
              block
              @click="commentType = 'conversation'"
            />
            <text-button
              label="Flag"
              icon="flag"
              small
              block
              text
              align="start"
              @click="commentType = 'flag'"
            />
          </flex-box>
        </q-btn-dropdown>
        <icon-button
          small
          :disabled="!newComment"
          tooltip="Add comment"
          icon="forward"
          @click="handleAddComment"
        />
      </template>
    </q-input>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays artifact comments, flags, and health checks.
 */
export default {
  name: "ArtifactComments",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { BasicCommentSchema, CommentSchema } from "@/types";
import { timestampToDisplay } from "@/util";
import {
  artifactStore,
  commentApiStore,
  commentStore,
  permissionStore,
  selectionStore,
} from "@/hooks";
import {
  PanelCard,
  ListItem,
  FlexBox,
  Icon,
  Typography,
  IconButton,
  TextButton,
  PopupEditInput,
} from "@/components/common";

const showResolved = ref(false);
const newComment = ref("");
const commentType = ref<"conversation" | "flag">("conversation");
const editedComment = ref<BasicCommentSchema | null>(null);

const artifactId = computed(() => selectionStore.selectedArtifactId);
const artifact = computed(() => artifactStore.selectedArtifact);

const allComments = computed(() =>
  commentStore.getCommentsAndFlags(artifactId.value, showResolved.value)
);

/**
 * Resets the comment input fields.
 */
function handleReset() {
  newComment.value = "";
  commentType.value = "conversation";
  editedComment.value = null;
}

/**
 * Adds a new comment to the artifact.
 */
function handleAddComment() {
  if (!artifact.value) return;

  commentApiStore.handleAddComment(
    artifact.value,
    newComment.value,
    commentType.value,
    {
      onSuccess: handleReset,
    }
  );
}

/**
 * Resolves a comment, hiding it from the list.
 * @param comment - The comment to resolve.
 */
function handleResolveComment(comment: BasicCommentSchema) {
  if (!artifact.value) return;

  commentApiStore.handleResolveComment(artifact.value, comment);
}

/**
 * Enables a comments edit mode,
 * or disables comment editing if already enabled on the given comment.
 * @param comment - The comment to edit.
 */
function handleEditComment(comment: BasicCommentSchema) {
  if (!editedComment.value || editedComment.value.id !== comment.id) {
    editedComment.value = comment;
  } else {
    editedComment.value = null;
  }
}

/**
 * Closes the edited comment.
 */
function handleCloseEditedComment() {
  editedComment.value = null;
}

/**
 * Saves the edited comment.
 */
function handleSaveEditedComment(content: string) {
  if (!editedComment.value || !artifact.value) return;

  editedComment.value.content = content;

  commentApiStore.handleEditComment(artifact.value, editedComment.value, {
    onSuccess: handleReset,
  });
}

/**
 * Deletes a comment.
 * @param comment - The comment to delete.
 */
function handleDeleteComment(comment: CommentSchema) {
  if (!artifact.value) return;

  commentApiStore.handleDeleteComment(artifact.value, comment.id);
}

onMounted(() => {
  commentApiStore.handleLoadComments(artifactId.value);
});

watch(
  () => artifactId.value,
  () => {
    handleReset();
    commentApiStore.handleLoadComments(artifactId.value);
  }
);
</script>
