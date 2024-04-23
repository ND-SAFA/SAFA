package edu.nd.crc.safa.features.chat.controller;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.CreateChatMessageDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.SendMessageResponseDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatMessageController extends BaseController {
    public ChatMessageController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Sends message in chat.
     *
     * @param createChatMessageDTO DTO containing user message being sent in chat.
     * @param chatId               ID of chat where message is being sent.
     * @return Saved user and response messages.
     */
    @PostMapping(AppRoutes.Chat.Message.MESSAGE_CREATE)
    public SendMessageResponseDTO sendMessageInChat(@RequestBody CreateChatMessageDTO createChatMessageDTO,
                                                    @PathVariable UUID chatId) {
        SafaUser currentUser = getCurrentUser();
        ServiceProvider serviceProvider = this.getServiceProvider();
        Chat chat = serviceProvider.getChatService().getChatById(chatId);
        return serviceProvider.getChatMessageService().sendChatMessage(chat,
            createChatMessageDTO.getMessage(),
            currentUser);
    }

    /**
     * Retrieves messages in chat with given id.
     *
     * @param chatId ID of chat to retrieve messages for.
     * @return List of messages in chat.
     */
    @GetMapping(AppRoutes.Chat.Message.MESSAGE_GET)
    public List<ChatMessageDTO> getChatMessages(@PathVariable UUID chatId) {
        SafaUser currentUser = getCurrentUser();
        Chat chat = getServiceProvider().getChatService().getChatById(chatId);
        if (!chat.isOwner(currentUser)) {
            throw new SafaError("User cannot send messages in chats they do not own.");
        }
        return getServiceProvider().getChatMessageService().getChatMessages(chat);
    }
}
