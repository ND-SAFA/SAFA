package edu.nd.crc.safa.features.chat.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendMessageResponseDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessageArtifact;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageArtifactRepository;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageRepository;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ChatMessageService {
    private ChatMessageRepository chatMessageRepository;
    private ChatMessageArtifactRepository chatMessageArtifactRepository;
    private ArtifactService artifactService;
    private ArtifactVersionRepository artifactVersionRepository;
    private GenApi genApi;

    /**
     * Sends message in chat.
     *
     * @param chat    The chat to send message in.
     * @param message The message to send.
     * @param author  The author of the message
     * @return The response from the AI.
     */
    public SendMessageResponseDTO sendChatMessage(Chat chat, String message, SafaUser author) {
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByCreatedAsc(chat);

        ChatMessage userMessage = new ChatMessage();

        userMessage.setContent(message);
        userMessage.setUser(true);
        userMessage.setChat(chat);
        userMessage.setAuthor(author);

        chatMessageRepository.save(userMessage);

        ChatMessageDTO responseMessage = generateChatResponse(userMessage, chatMessages, chat.getProjectVersion());

        return new SendMessageResponseDTO(
            ChatMessageDTO.asUserMessage(userMessage),
            responseMessage
        );
    }

    /**
     * Retrieves messages in chat, along with their associated artifacts.
     *
     * @param chat The chat whose messages are retrieved.
     * @return List of messages in chat, sorted by position in chat.
     */
    public List<ChatMessageDTO> getChatMessages(Chat chat) {
        List<ChatMessageArtifact> chatMessageArtifacts = chatMessageArtifactRepository.findByMessageChat(chat);
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByCreatedAsc(chat);
        List<ChatMessageDTO> chatMessageDTOS = new ArrayList<>();
        Map<UUID, List<ChatMessageArtifact>> message2artifacts = ProjectDataStructures
            .groupEntitiesByProperty(chatMessageArtifacts, c -> c.getMessage().getId());
        for (ChatMessage chatMessage : chatMessages) {
            List<ChatMessageArtifact> messageArtifacts = message2artifacts.getOrDefault(chatMessage.getId(), new ArrayList<>());
            ChatMessageDTO dto = createChatMessageDTO(chatMessage, messageArtifacts);
            chatMessageDTOS.add(dto);
        }
        return chatMessageDTOS;
    }

    /**
     * Generates a response for the user message.
     *
     * @param userMessage    The user message being responded to.
     * @param chatMessages   Previous messages in chat.
     * @param projectVersion Project version used to retrieve artifacts going into response context.
     * @return DTO of response to user message.
     */
    private ChatMessageDTO generateChatResponse(ChatMessage userMessage,
                                                List<ChatMessage> chatMessages,
                                                ProjectVersion projectVersion) {
        ChatMessage responseMessage = new ChatMessage();
        responseMessage.setChat(userMessage.getChat());
        responseMessage.setAuthor(userMessage.getAuthor());
        responseMessage.setUser(false);

        // Send to gen...
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        artifactService.versionToAppEntity(artifactVersions);
        Map<UUID, List<ArtifactVersion>> artifactId2version = ProjectDataStructures.groupEntitiesByProperty(
            artifactVersions, ArtifactVersion::getBaseEntityId);

        List<GenerationArtifact> genArtifacts = artifactVersions
            .stream()
            .map(GenerationArtifact::new)
            .toList();
        GenChatResponse genChatResponse = genApi.generateChatResponse(userMessage.getContent(), chatMessages, genArtifacts);
        responseMessage.setContent(genChatResponse.getMessage());

        responseMessage = chatMessageRepository.save(responseMessage);

        ChatMessage finalResponseMessage = responseMessage; // variables used in lambda must be final.
        List<ChatMessageArtifact> chatMessageArtifacts = genChatResponse.getArtifactIds().stream()
            .map(artifactId -> {
                ChatMessageArtifact chatMessageArtifact = new ChatMessageArtifact();
                chatMessageArtifact.setMessage(finalResponseMessage);
                Artifact artifact = artifactId2version.get(artifactId).get(0).getArtifact();
                chatMessageArtifact.setArtifact(artifact);
                return chatMessageArtifact;
            }).toList();

        chatMessageArtifactRepository.saveAll(chatMessageArtifacts);

        return ChatMessageDTO.asResponseMessage(responseMessage, genChatResponse.getArtifactIds());
    }

    /**
     * Creates DTO representing message in chat.
     *
     * @param chatMessage      The chat message to represent.
     * @param messageArtifacts Artifacts used to create message.
     * @return DTO.
     */
    private ChatMessageDTO createChatMessageDTO(ChatMessage chatMessage,
                                                List<ChatMessageArtifact> messageArtifacts) {
        List<UUID> messageArtifactIds = messageArtifacts
            .stream()
            .map(ChatMessageArtifact::getArtifact)
            .map(Artifact::getArtifactId)
            .toList();
        List<UUID> artifactIds = new ArrayList<>(messageArtifactIds);

        ChatMessageDTO dto;
        if (chatMessage.isUser()) {
            dto = ChatMessageDTO.asUserMessage(chatMessage);
        } else {
            dto = ChatMessageDTO.asResponseMessage(chatMessage, artifactIds);
        }
        return dto;
    }

}
