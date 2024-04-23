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
    public Chat createNewChat(SafaUser user, ProjectVersion projectVersion, String title) {
        Chat chat = new Chat();
        chat.setOwner(user);
        chat.setProjectVersion(projectVersion);
        chat.setTitle(title);
        return chatRepository.save(chat);
    }

    /**
     * Updates chat with new title, if one exists.
     *
     * @param chatDTO        The chat to update.
     * @param user           The user making request to update chat.
     * @param projectVersion The project version being queried in chat.
     * @return The updated chat.
     */
    public Chat updateChat(ChatDTO chatDTO, SafaUser user, ProjectVersion projectVersion) {
        Chat chat = getChatById(chatDTO.getId());
        if (!chat.isOwner(user)) {
            throw new SafaError("Chat is not owned by user making request.");
        }

        verifyChatPermission(chat, user, ChatSharePermission.EDIT);

        String userTitle = chatDTO.getTitle();
        if (userTitle == null || userTitle.isBlank()) {
            throw new SafaError("Unable to save chat with empty title.");
        }

        chat.setTitle(userTitle);
        chat.setProjectVersion(projectVersion);

        return chatRepository.save(chat);
    }

    /**
     * Retrieves all chats accessible to user.
     *
     * @param user The user whose chats are queried for.
     * @return Chats owned by or shared with user.
     */
    public List<Chat> getUserChats(SafaUser user) {
        List<Chat> ownedChats = chatRepository.findByOwner(user);
        List<ChatShare> sharedChats = chatShareRepository.findByUser(user);

        List<Chat> userChats = new ArrayList<>(ownedChats);
        userChats.addAll(sharedChats.stream().map(ChatShare::getChat).toList());
        return userChats;
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
    public void verifyChatPermission(Chat chat, SafaUser user, ChatSharePermission requestedPermission) {
        Optional<ChatShare> chatShareOptional = chatShareRepository.findByChatAndUser(chat, user);
        if (chat.isOwner(user)) {
            return;
        }

        if (chatShareOptional.isEmpty()) {
            throw new SafaError("User does not have permission to chat.");
        }
        ChatShare chatShare = chatShareOptional.get();
        ChatSharePermission chatPermission = chatShare.getPermission();
        if (!chatPermission.hasPermission(requestedPermission)) {
            throw new SafaError("User does not have sufficient permissions to chat.");
        }
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
