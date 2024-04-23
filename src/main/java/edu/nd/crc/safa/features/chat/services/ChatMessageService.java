package edu.nd.crc.safa.features.chat.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendMessageResponseDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessageArtifact;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageArtifactRepository;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ChatMessageService {
    private ChatMessageRepository chatMessageRepository;
    private ChatMessageArtifactRepository chatMessageArtifactRepository;
    
    /**
     * Sends message in chat.
     *
     * @param chat    The chat to send message in.
     * @param message The message to send.
     * @param author  The author of the message
     * @return The response from the AI.
     */
    public SendMessageResponseDTO sendChatMessage(Chat chat, String message, SafaUser author) {
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByPositionAsc(chat);

        ChatMessage userMessage = new ChatMessage();

        userMessage.setMessage(message);
        userMessage.setUser(true);
        userMessage.setChat(chat);
        userMessage.setAuthor(author);
        userMessage.setPosition(chatMessages.size());

        chatMessageRepository.save(userMessage);

        ChatMessageDTO responseMessage = createChatResponse(userMessage, chatMessages, chat.getProjectVersion());

        SendMessageResponseDTO chatOutput = new SendMessageResponseDTO();
        chatOutput.setMessage(ChatMessageDTO.asUserMessage(userMessage));
        chatOutput.setResponse(responseMessage);

        return chatOutput;
    }

    /**
     * Retrieves messages in chat, along with their associated artifacts.
     *
     * @param chat The chat whose messages are retrieved.
     * @return List of messages in chat, sorted by position in chat.
     */
    public List<ChatMessageDTO> getChatMessages(Chat chat) {
        List<ChatMessageArtifact> chatMessageArtifacts = chatMessageArtifactRepository.findByMessageChat(chat);
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByPositionAsc(chat);
        List<ChatMessageDTO> chatMessageDTOS = new ArrayList<>();
        Map<UUID, List<ChatMessageArtifact>> message2artifacts = createMessageArtifactLookupTable(chatMessageArtifacts);
        for (ChatMessage chatMessage : chatMessages) {
            List<ChatMessageArtifact> messageArtifacts = message2artifacts.computeIfAbsent(chatMessage.getId(),
                uuid -> new ArrayList<>());
            ChatMessageDTO dto = createChatMessageDTO(chatMessage, messageArtifacts);
            chatMessageDTOS.add(dto);
        }
        return chatMessageDTOS;
    }

    private ChatMessageDTO createChatResponse(ChatMessage userMessage,
                                              List<ChatMessage> chatMessages,
                                              ProjectVersion projectVersion) {
        ChatMessage responseMessage = new ChatMessage();
        responseMessage.setAuthor(userMessage.getAuthor());
        responseMessage.setPosition(userMessage.getPosition() + 1);
        responseMessage.setUser(false);

        GenChatResponse genChatResponse = getResponseFromGen(userMessage.getMessage(), chatMessages, projectVersion);
        responseMessage.setMessage(genChatResponse.getMessage());

        return ChatMessageDTO.asResponseMessage(responseMessage, genChatResponse.getArtifactIds());
    }

    private GenChatResponse getResponseFromGen(String message,
                                               List<ChatMessage> chatMessages,
                                               ProjectVersion projectVersion) {
        GenChatResponse genChatResponse = new GenChatResponse(); // TODO: Replace with implementation.
        genChatResponse.setMessage(message);
        genChatResponse.setArtifactIds(new ArrayList<>());
        return genChatResponse;
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

    /**
     * Creates table used to lookup which artifacts are referenced in each message.
     *
     * @param chatMessageArtifacts The artifacts referenced in chat.
     * @return map of message ID to its artifacts.
     */
    @NotNull
    private Map<UUID, List<ChatMessageArtifact>> createMessageArtifactLookupTable(
        List<ChatMessageArtifact> chatMessageArtifacts) {
        Map<UUID, List<ChatMessageArtifact>> message2artifacts = new HashMap<>();
        for (ChatMessageArtifact chatMessageArtifact : chatMessageArtifacts) {
            UUID chatMessageId = chatMessageArtifact.getMessage().getId();
            if (message2artifacts.containsKey(chatMessageId)) {
                message2artifacts.get(chatMessageId).add(chatMessageArtifact);
            } else {
                List<ChatMessageArtifact> chatMessageArtifactList = new ArrayList<>();
                chatMessageArtifactList.add(chatMessageArtifact);
                message2artifacts.put(chatMessageId, chatMessageArtifactList);
            }
        }
        return message2artifacts;
    }
}
