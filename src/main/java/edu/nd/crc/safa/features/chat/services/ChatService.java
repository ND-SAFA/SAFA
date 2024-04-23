package edu.nd.crc.safa.features.chat.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatShare;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatSharePermission;
import edu.nd.crc.safa.features.chat.repositories.ChatRepository;
import edu.nd.crc.safa.features.chat.repositories.ChatShareRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
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
        chat.setOwner(user);
        chat.setProjectVersion(projectVersion);
        chat.setTitle(title);
        chat = chatRepository.save(chat);
        return ChatDTO.fromChat(chat, ChatSharePermission.OWNER);
    }

    /**
     * Updates chat with new title, if one exists.
     *
     * @param chatDTO        The chat to update.
     * @param user           The user making request to update chat.
     * @param projectVersion The project version being queried in chat.
     * @return The updated chat.
     */
    public ChatDTO updateChat(ChatDTO chatDTO, SafaUser user, ProjectVersion projectVersion) {
        Chat chat = getChatById(chatDTO.getId());
        if (!chat.isOwner(user)) {
            throw new SafaError("Chat is not owned by user making request.");
        }

        ChatSharePermission permission = verifyChatPermission(chat, user, ChatSharePermission.EDIT);

        String userTitle = chatDTO.getTitle();
        if (userTitle == null || userTitle.isBlank()) {
            throw new SafaError("Unable to save chat with empty title.");
        }

        chat.setTitle(userTitle);
        chat.setProjectVersion(projectVersion);

        chat = chatRepository.save(chat);
        return ChatDTO.fromChat(chat, permission);
    }

    /**
     * Retrieves all chats accessible to user.
     *
     * @param user The user whose chats are queried for.
     * @return Chats owned by or shared with user.
     */
    public List<ChatDTO> getUserChats(SafaUser user) {
        List<ChatDTO> ownedChats = chatRepository.findByOwner(user)
            .stream().map(c -> ChatDTO.fromChat(c, ChatSharePermission.OWNER)).toList();
        List<ChatDTO> chatDTOS = new ArrayList<>(ownedChats);
        List<ChatDTO> sharedChats = chatShareRepository
            .findByUser(user)
            .stream()
            .map(cs -> ChatDTO.fromChat(cs.getChat(), cs.getPermission()))
            .toList();
        chatDTOS.addAll(sharedChats);
        return chatDTOS;
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
     */
    public ChatSharePermission verifyChatPermission(Chat chat, SafaUser user, ChatSharePermission requestedPermission) {
        Optional<ChatShare> chatShareOptional = chatShareRepository.findByChatAndUser(chat, user);
        if (chat.isOwner(user)) {
            return ChatSharePermission.OWNER;
        }

        if (chatShareOptional.isEmpty()) {
            throw new SafaError("User does not have permission to chat.");
        }
        ChatShare chatShare = chatShareOptional.get();
        ChatSharePermission chatPermission = chatShare.getPermission();
        if (!chatPermission.hasPermission(requestedPermission)) {
            throw new SafaError("User does not have sufficient permissions to chat.");
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
}
