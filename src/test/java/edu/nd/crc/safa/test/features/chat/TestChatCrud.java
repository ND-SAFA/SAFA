package edu.nd.crc.safa.test.features.chat;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.CreateChatRequestDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.EditChatRequestDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestChatCrud extends ApplicationBaseTest {

    /**
     * Tests ability to create, retrieve, update, and delete chats.
     *
     * @throws Exception If HTTP error.
     */
    @Test
    void testChatCrud() throws Exception {
        String NEW_TITLE = "New title";
        SafaUser currentUser = getCurrentUser();

        ProjectVersion projectVersion =
            this.rootBuilder.actions(a -> a.createProjectWithVersion(getCurrentUser())).get();

        List<ChatDTO> userChats = getUserChats(projectVersion);
        assertThat(userChats.size()).isZero();

        ChatDTO chat = createChat(projectVersion); // create
        verifyChat(chat, CreateChatRequestDTO.DEFAULT_TITLE, ChatPermission.OWNER);

        userChats = getUserChats(projectVersion); // verify : create
        assertThat(userChats.size()).isEqualTo(1);

        chat.setTitle(NEW_TITLE); // update
        chat = updateChat(chat.getId(), NEW_TITLE);
        assertThat(chat.getTitle()).isEqualTo(NEW_TITLE);

        userChats = getUserChats(projectVersion); // verify: update
        ChatDTO userChat = userChats.get(0);
        assertThat(userChat.getTitle()).isEqualTo(NEW_TITLE);
        verifyChat(userChats.get(0), NEW_TITLE, ChatPermission.OWNER);

        deleteChat(userChat.getId()); // delete

        userChats = getUserChats(projectVersion); // verify: delete
        assertThat(userChats.size()).isEqualTo(0);
    }

    private ChatDTO createChat(ProjectVersion projectVersion) {
        ChatDTO payload = new ChatDTO();
        payload.setVersionId(projectVersion.getVersionId());

        return SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_CREATE)
            .postWithJsonObject(payload, ChatDTO.class);
    }

    private ChatDTO updateChat(UUID chatId, String newTitle) {
        EditChatRequestDTO request = new EditChatRequestDTO();
        request.setTitle(newTitle);
        return SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_UPDATE)
            .withCustomReplacement("chatId", chatId)
            .putWithJsonObject(request, ChatDTO.class);
    }

    private void verifyChat(ChatDTO chat, String title, ChatPermission chatPermission) {
        assertThat(chat.getId()).isNotNull();
        assertThat(chat.getTitle()).isNotNull().isEqualTo(title);
        assertThat(chat.getPermission()).isEqualTo(chatPermission);
    }

    private List<ChatDTO> getUserChats(ProjectVersion projectVersion) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_GET)
            .withProject(projectVersion.getProject())
            .getAsArray(ChatDTO.class);
    }

    private void deleteChat(UUID chatId) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_DELETE)
            .withCustomReplacement("chatId", chatId)
            .deleteWithJsonObject();
    }
}
