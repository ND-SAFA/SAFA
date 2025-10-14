package edu.nd.crc.safa.test.features.chat;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.gen.GenChatTitleResponse;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestGenerateChatTitle extends GenerationalTest {

    /**
     * Tests that chat is able to send messages and respond to them using GEN api.
     *
     * @throws Exception If HTTP error.
     */
    @Test
    void testSendChatMessage() throws Exception {
        String generatedTitle = "this is generated title";

        // Create project, version, and artifact.
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(currentUser)).get();
        ChatTestData testData = new ChatTestData();
        testData.createProject(this.rootBuilder, projectVersion);

        // create chat
        ChatDTO chat = getServiceProvider().getChatService().createNewChat(currentUser,
            projectVersion,
            ChatTestData.chatTitle
        );

        mockChatResponse(generatedTitle);
        ChatDTO updatedChat = SafaRequest
            .withRoute(AppRoutes.Chat.CHAT_TITLE)
            .withCustomReplacement("chatId", chat.getId())
            .postWithoutBody(ChatDTO.class);

        assertThat(updatedChat.getTitle()).isEqualTo(generatedTitle);

        ChatDTO retrievedChat = ChatTestData.retrieveChat(chat.getId());
        assertThat(retrievedChat.getTitle()).isEqualTo(generatedTitle);
    }

    /**
     * Mocks the GEN response.
     *
     * @param newTitle Title to generate for chat.
     */
    private void mockChatResponse(String newTitle) {
        GenChatTitleResponse genResponse = new GenChatTitleResponse();
        genResponse.setTitle(newTitle);
        getServer().setResponse(genResponse);
    }
}
