package edu.nd.crc.safa.test.features.chat;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
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

        List<Chat> userChats = getUserChats(projectVersion);
        assertThat(userChats.size()).isZero();

        Chat chat = createChat(projectVersion); // create

        userChats = getUserChats(projectVersion); // verify : create
        assertThat(userChats.size()).isEqualTo(1);

        chat.setTitle(NEW_TITLE); // update
        chat.setProjectVersion(projectVersion); // project version ignored in response  so empty here.
        chat = updateChat(ChatDTO.fromChat(chat), projectVersion);
        assertThat(chat.getTitle()).isEqualTo(NEW_TITLE);

        userChats = getUserChats(projectVersion); // verify: update
        Chat userChat = userChats.get(0);
        assertThat(userChat.getTitle()).isEqualTo(NEW_TITLE);

        deleteChat(userChat.getId()); // delete

        userChats = getUserChats(projectVersion); // verify: delete
        assertThat(userChats.size()).isEqualTo(0);
    }

    private Chat createChat(ProjectVersion projectVersion) {
        ChatDTO payload = new ChatDTO();
        payload.setVersionId(projectVersion.getVersionId());

        Chat chat = SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_CREATE)
            .postWithJsonObject(payload, Chat.class);

        assertThat(chat.getId()).isNotNull();
        assertThat(chat.getTitle()).isNotNull();
        return chat;
    }

    private Chat updateChat(ChatDTO chatDTO, ProjectVersion projectVersion) {
        Chat chat = SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_UPDATE)
            .withVersion(projectVersion)
            .putWithJsonObject(chatDTO, Chat.class);

        assertThat(chat.getId()).isNotNull();
        assertThat(chat.getTitle()).isNotNull();
        return chat;
    }

    private List<Chat> getUserChats(ProjectVersion projectVersion) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_GET)
            .withVersion(projectVersion)
            .getAsArray(Chat.class);
    }

    private void deleteChat(UUID chatId) throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_DELETE)
            .withCustomReplacement("chatId", chatId)
            .deleteWithJsonObject();
    }
}
