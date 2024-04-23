package edu.nd.crc.safa.test.features.chat;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendChatMessageRequest;
import edu.nd.crc.safa.features.chat.entities.dtos.SendChatMessageResponse;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;

import org.junit.jupiter.api.Test;

class TestChatMessage extends GenerationalTest {

    /**
     * Tests that chat is able to send messages and respond to them using GEN api.
     *
     * @throws Exception If HTTP error.
     */
    @Test
    void testSendChatMessage() throws Exception {

        String artifactBody = "artifact body";
        String artifactType = "artifact type";
        String userMessageText = "this is the user message.";
        String artifactName = "RE-8";
        String responseText = "Response";
        String chatTitle = "Hello";

        // Create project, version, and artifact.
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(currentUser)).get();
        ArtifactAppEntity artifact = new ArtifactAppEntity();
        artifact.setBody(artifactBody);
        artifact.setType(artifactType);
        artifact.setName(artifactName);
        ArtifactAppEntity artifactAdded = this.rootBuilder.actions(a -> a.commit(
                CommitBuilder
                    .withVersion(projectVersion)
                    .withAddedArtifact(artifact)
            ).getArtifact(ModificationType.ADDED, 0))
            .get();
        List<String> artifactNames = List.of(artifactAdded.getName());
        List<UUID> artifactIds = List.of(artifactAdded.getId());

        // create chat
        Chat chat = getServiceProvider().getChatService().createNewChat(currentUser, projectVersion, chatTitle);

        // verify no messages in chat.
        List<ChatMessageDTO> chatMessages = SafaRequest
            .withRoute(AppRoutes.Chat.Message.MESSAGE_GET)
            .withCustomReplacement("chatId", chat.getId())
            .getAsArray(ChatMessageDTO.class);
        assertThat(chatMessages.size()).isEqualTo(0);

        // mock: chat response
        mockChatResponse(responseText, artifactNames);

        // step 1 - create message
        SendChatMessageRequest request = new SendChatMessageRequest();
        request.setMessage(userMessageText);

        SendChatMessageResponse response = SafaRequest
            .withRoute(AppRoutes.Chat.Message.MESSAGE_CREATE)
            .withCustomReplacement("chatId", chat.getId())
            .postWithJsonObject(request, SendChatMessageResponse.class);

        // verify response
        ChatMessageDTO userMessage = response.getUserMessage();
        verifyUserMessage(userMessage, userMessageText);

        ChatMessageDTO responseMessage = response.getResponseMessage();
        verifyResponseMessage(responseMessage, responseText, artifactIds);

        // verify - retrieve message and response in chat
        chatMessages = SafaRequest
            .withRoute(AppRoutes.Chat.Message.MESSAGE_GET)
            .withCustomReplacement("chatId", chat.getId())
            .getAsArray(ChatMessageDTO.class);

        assertThat(chatMessages.size()).isEqualTo(2);
        verifyUserMessage(chatMessages.get(0), userMessageText);
        verifyResponseMessage(chatMessages.get(1), responseText, artifactIds);
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
        getServer().setResponse(genResponse);
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
        assertThat(message.getUserMessage()).isNull();
        assertThat(message.getResponseMessage()).isEqualTo(responseText);
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
        assertThat(message.getUserMessage()).isEqualTo(userMessageText);
        assertThat(message.getResponseMessage()).isNull();
        assertThat(message.getArtifactIds().size()).isEqualTo(0);
    }
}
