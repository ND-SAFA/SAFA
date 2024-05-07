package edu.nd.crc.safa.test.features.chat;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendChatMessageRequest;
import edu.nd.crc.safa.features.chat.entities.dtos.SendChatMessageResponse;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestChatMessage extends GenerationalTest {

    /**
     * Tests that chat is able to send messages and respond to them using GEN api.
     *
     * @throws Exception If HTTP error.
     */
    @Test
    void testSendChatMessage() throws Exception {


        // Create project, version, and artifact.
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(currentUser)).get();
        ChatTestData testData = new ChatTestData();

        testData.createProject(this.rootBuilder, projectVersion);

        // create chat
        ChatDTO chat = getServiceProvider().getChatService().createNewChat(currentUser, projectVersion,
            ChatTestData.chatTitle);

        // verify no messages in chat.
        ChatDTO chatDTO = ChatTestData.retrieveChat(chat.getId());
        assertThat(chatDTO.getMessages().size()).isEqualTo(0);

        // mock: chat response
        mockChatResponse(ChatTestData.responseText, testData.getArtifactNames());

        // step 1 - create message
        SendChatMessageRequest request = new SendChatMessageRequest();
        request.setMessage(ChatTestData.userMessageText);

        SendChatMessageResponse response = SafaRequest
            .withRoute(AppRoutes.Chat.Message.MESSAGE_SEND)
            .withCustomReplacement("chatId", chat.getId())
            .postWithJsonObject(request, SendChatMessageResponse.class);

        // verify response
        ChatMessageDTO userMessage = response.getUserMessage();
        verifyUserMessage(userMessage, ChatTestData.userMessageText);

        ChatMessageDTO responseMessage = response.getResponseMessage();
        verifyResponseMessage(responseMessage, ChatTestData.responseText, testData.getArtifactIds());

        // verify - retrieve message and response in chat
        chatDTO = ChatTestData.retrieveChat(chat.getId());

        assertThat(chatDTO.getMessages().size()).isEqualTo(2);
        verifyUserMessage(chatDTO.getMessages().get(0), ChatTestData.userMessageText);
        verifyResponseMessage(chatDTO.getMessages().get(1), ChatTestData.responseText, testData.getArtifactIds());
    }

    /**
     * Mocks the GEN response.
     *
     * @param responseContent The content of the response message.
     * @param artifactNames   Names of artifacts.
     */
    private void mockChatResponse(String responseContent, List<String> artifactNames) {
        GenChatResponse genResponse = new GenChatResponse();
        genResponse.setMessage(responseContent);
        genResponse.setArtifactIds(artifactNames);
        getServer().setJobResponse(genResponse);
    }

    /**
     * Verifies that message matches message text and response message properties.
     *
     * @param message      The message to verify.
     * @param responseText The expected text.
     * @param artifactIds  The expected list of artifacts ids in response.
     */
    private void verifyResponseMessage(ChatMessageDTO message, String responseText, List<UUID> artifactIds) {
        assertThat(message.getId()).isNotNull();
        assertThat(message.isUser()).isFalse();
        assertThat(message.getMessage()).isEqualTo(responseText);
        List<UUID> messageArtifactIds = message.getArtifactIds();
        assertThat(messageArtifactIds.size()).isEqualTo(artifactIds.size());
        for (UUID artifactId : artifactIds) {
            assertThat(messageArtifactIds.contains(artifactId)).isTrue();
        }
    }

    /**
     * Verifies that message matches message text and user message properties.
     *
     * @param message         The message to verify.
     * @param userMessageText The expected text.
     */
    private void verifyUserMessage(ChatMessageDTO message, String userMessageText) {
        assertThat(message.getId()).isNotNull();
        assertThat(message.isUser()).isTrue();
        assertThat(message.getMessage()).isEqualTo(userMessageText);
        assertThat(message.getArtifactIds().size()).isEqualTo(0);
    }
}
