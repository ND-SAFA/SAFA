package edu.nd.crc.safa.features.chat.services;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactLookupTable;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendChatMessageResponse;
import edu.nd.crc.safa.features.chat.entities.gen.GenChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessageArtifact;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageArtifactRepository;
import edu.nd.crc.safa.features.chat.repositories.ChatMessageRepository;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ChatMessageService {
    private ChatMessageRepository chatMessageRepository;
    private ChatMessageArtifactRepository chatMessageArtifactRepository;
    private ArtifactService artifactService;
    private GenApi genApi;

    /**
     * Sends message in chat.
     *
     * @param chat    The chat to send message in.
     * @param message The message to send.
     * @param author  The author of the message
     * @return The response from the AI.
     */
    public SendChatMessageResponse sendChatMessage(Chat chat, String message, SafaUser author) {
        List<GenChatMessage> genChatMessages = getGenChatMessages(chat);

        ChatMessage userMessage = new ChatMessage();
        userMessage.setCreatedAt(LocalDateTime.now());
        userMessage.setContent(message);
        userMessage.setUser(true);
        userMessage.setChat(chat);
        userMessage.setAuthor(author);

        Pair<ChatMessage, List<ChatMessageArtifact>> response = generateChatResponse(
            userMessage,
            genChatMessages,
            chat.getProjectVersion());
        ChatMessage responseMessage = response.getValue0();
        List<ChatMessageArtifact> responseMessageArtifacts = response.getValue1();

        chatMessageRepository.save(userMessage);
        chatMessageRepository.save(responseMessage);
        chatMessageArtifactRepository.saveAll(responseMessageArtifacts);

        return new SendChatMessageResponse(
            ChatMessageDTO.asUserMessage(userMessage),
            ChatMessageDTO.asResponseMessage(
                responseMessage,
                responseMessageArtifacts.stream().map(r -> r.getArtifact().getArtifactId()).toList()
            )
        );
    }

    /**
     * Returns the messages for given chat, containing their associated artifact ids if they exist.
     *
     * @param chat The chat to retrieve messages for.
     * @return List of messages in chat.
     */
    public List<GenChatMessage> getGenChatMessages(Chat chat) {
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByCreatedAtAsc(chat);
        List<ChatMessageArtifact> chatMessageArtifacts = chatMessageArtifactRepository.findByMessageChat(chat);

        Map<ChatMessage, List<ChatMessageArtifact>> message2artifacts =
            ProjectDataStructures.createGroupLookup(chatMessageArtifacts, ChatMessageArtifact::getMessage);
        List<GenChatMessage> genChatMessages = new ArrayList<>();
        for (ChatMessage chatMessage : chatMessages) {
            List<String> artifactIds = new ArrayList<>();
            if (message2artifacts.containsKey(chatMessage)) {
                artifactIds.addAll(message2artifacts
                    .get(chatMessage)
                    .stream()
                    .map(c -> c.getArtifact().getName())
                    .toList());
            }
            genChatMessages.add(new GenChatMessage(chatMessage, artifactIds));
        }
        return genChatMessages;
    }

    /**
     * Retrieves messages in chat, along with their associated artifacts.
     *
     * @param chat The chat whose messages are retrieved.
     * @return List of messages in chat, sorted by position in chat.
     */
    public List<ChatMessageDTO> getChatMessages(Chat chat) {
        List<ChatMessageArtifact> chatMessageArtifacts = chatMessageArtifactRepository.findByMessageChat(chat);
        List<ChatMessage> chatMessages = chatMessageRepository.findByChatOrderByCreatedAtAsc(chat);
        List<ChatMessageDTO> chatMessageDTOS = new ArrayList<>();
        Map<UUID, List<ChatMessageArtifact>> message2artifacts = ProjectDataStructures
            .createGroupLookup(chatMessageArtifacts, c -> c.getMessage().getId());
        for (ChatMessage chatMessage : chatMessages) {
            List<ChatMessageArtifact> messageArtifacts = message2artifacts.getOrDefault(chatMessage.getId(),
                new ArrayList<>());
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
    private Pair<ChatMessage, List<ChatMessageArtifact>> generateChatResponse(ChatMessage userMessage,
                                                                              List<GenChatMessage> chatMessages,
                                                                              ProjectVersion projectVersion) {
        ChatMessage responseMessage = new ChatMessage();
        responseMessage.setChat(userMessage.getChat());
        responseMessage.setAuthor(userMessage.getAuthor());
        responseMessage.setUser(false);

        // Send to gen...
        ArtifactLookupTable artifactLookupTable = artifactService.getArtifactLookupTable(projectVersion);

        GenChatResponse genChatResponse = genApi.generateChatResponse(
            userMessage.getContent(), chatMessages, artifactLookupTable.getGenerationArtifacts());
        responseMessage.setContent(genChatResponse.getMessage());
        responseMessage.setCreatedAt(LocalDateTime.now());
        List<ChatMessageArtifact> responseMessageArtifacts = genChatResponse.getArtifactIds().stream()
            .map(genArtifact -> {
                ChatMessageArtifact chatMessageArtifact = new ChatMessageArtifact();
                chatMessageArtifact.setMessage(responseMessage);
                Artifact artifact = artifactLookupTable.getByName(genArtifact).getArtifact();
                chatMessageArtifact.setArtifact(artifact);
                return chatMessageArtifact;
            }).toList();
        return new Pair<>(responseMessage, responseMessageArtifacts);
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
