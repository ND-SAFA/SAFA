package edu.nd.crc.safa.features.chat.services;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.gen.GenChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatPermission;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatShare;
import edu.nd.crc.safa.features.chat.repositories.ChatRepository;
import edu.nd.crc.safa.features.chat.repositories.ChatShareRepository;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ChatService {
    private ChatRepository chatRepository;
    private ChatShareRepository chatShareRepository;
    private ChatMessageService chatMessageService;
    private GenApi genApi;
    private ArtifactService artifactService;

    /**
     * Generates a new title for chat.
     *
     * @param chat The chat to generate title for.
     * @return Response containing new title.
     */
    public String generateChatTitle(Chat chat) {
        List<GenChatMessage> genChatMessages = chatMessageService.getGenChatMessages(chat);
        List<GenerationArtifact> generationArtifacts =
            artifactService
                .getArtifactLookupTable(chat.getProjectVersion())
                .getGenerationArtifacts();
        String generatedTitle = genApi.generateChatTitle(genChatMessages, generationArtifacts).getTitle();
        chat.setTitle(generatedTitle);
        this.chatRepository.save(chat);
        return generatedTitle;
    }

    /**
     * Creates new empty chat.
     *
     * @param user           Owner of chat.
     * @param projectVersion The project version used to access to chat.
     * @param title          The title of the chat.
     * @return Chat created
     */
    @NotNull
    public ChatDTO createNewChat(SafaUser user, ProjectVersion projectVersion, String title) {
        Chat chat = new Chat();
        chat.setUpdatedAt(LocalDateTime.now());
        chat.setOwner(user);
        chat.setProjectVersion(projectVersion);
        chat.setTitle(title);
        chat = chatRepository.save(chat);
        return ChatDTO.fromChat(chat, ChatPermission.OWNER);
    }

    /**
     * Updates chat with new title, if one exists.
     *
     * @param chat     The chat being updated.
     * @param newTitle New title to set chat to.
     * @param user     The user making request to update chat.
     * @return The updated chat.
     */
    public ChatDTO updateChat(Chat chat, String newTitle, SafaUser user) {
        ChatPermission permission = verifyChatPermission(chat, user, ChatPermission.EDIT);

        if (newTitle == null || newTitle.isBlank()) {
            throw new SafaError("Unable to save chat with empty title.");
        }

        chat.setTitle(newTitle);

        chat = chatRepository.save(chat);
        return ChatDTO.fromChat(chat, permission);
    }

    /**
     * Retrieves all chats accessible to user.
     *
     * @param user    The user whose chats are queried for.
     * @param project The project to retrieve chats within.
     * @return Chats owned by or shared with user.
     */
    public List<ChatDTO> getUserChats(SafaUser user, Project project) {
        List<ChatDTO> projectChats = chatRepository.findByOwnerAndProjectVersionProject(user, project)
            .stream().map(c -> ChatDTO.fromChat(c, ChatPermission.OWNER)).collect(Collectors.toList());
        List<ChatDTO> sharedChats = chatShareRepository
            .findByUserAndChatProjectVersionProject(user, project)
            .stream()
            .map(cs -> ChatDTO.fromChat(cs.getChat(), cs.getPermission()))
            .toList();
        projectChats.addAll(sharedChats);
        projectChats.sort((chat1, chat2) -> chat2.getUpdatedAt().compareTo(chat1.getUpdatedAt()));
        return projectChats;
    }

    /**
     * Deletes chat.
     *
     * @param chatId ID of chat to delete.
     * @param user   The user requesting chat to be deleted.
     */
    public void deleteChat(UUID chatId, SafaUser user) {
        Chat chat = getChatById(chatId);
        if (!chat.isOwner(user)) {
            throw new SafaError("Insufficient permission to delete chat.");
        }
        chatRepository.delete(chat);
    }

    /**
     * Verifies that user has at least the requested permission on chat.
     *
     * @param chat                The chat to check permission against.
     * @param user                The user whose permission is checked.
     * @param requestedPermission The minimum acceptable permission
     * @return The permission level that user has on the chat.
     */
    public ChatPermission verifyChatPermission(Chat chat, SafaUser user, ChatPermission requestedPermission) {
        Optional<ChatShare> chatShareOptional = chatShareRepository.findByChatAndUser(chat, user);
        if (chat.isOwner(user)) {
            return ChatPermission.OWNER;
        }

        if (chatShareOptional.isEmpty()) {
            throw new SafaError("User does not have permission to chat.");
        }
        ChatShare chatShare = chatShareOptional.get();
        ChatPermission chatPermission = chatShare.getPermission();
        if (!chatPermission.hasPermission(requestedPermission)) {
            throw new MissingPermissionException(requestedPermission);
        }
        return chatShare.getPermission();
    }

    /**
     * Retrieves chat by ID.
     *
     * @param chatId ID of chat to retrieve.
     * @return The chat with given ID.
     */
    @NotNull
    public Chat getChatById(UUID chatId) {
        Optional<Chat> chatOptional = chatRepository.findById(chatId);
        if (chatOptional.isEmpty()) {
            throw new SafaError("Could not find chat with ID.");
        }
        return chatOptional.get();
    }

    /**
     * `Touches` file setting a new last updated time.
     *
     * @param chat The chat to update.
     */
    public void touchChat(Chat chat) {
        chat.setUpdatedAt(LocalDateTime.now());
        this.chatRepository.save(chat);
    }
}
