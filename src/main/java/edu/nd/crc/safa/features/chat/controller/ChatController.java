package edu.nd.crc.safa.features.chat.controller;

import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.CreateChatRequestDTO;
import edu.nd.crc.safa.features.chat.entities.dtos.EditChatRequestDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatPermission;
import edu.nd.crc.safa.features.chat.services.ChatService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatController extends BaseController {

    public ChatController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Creates empty chat with access to project version.
     *
     * @param chatDTO Optional. Chat with initial title to create.
     * @return New Chat.
     */
    @PostMapping(AppRoutes.Chat.CHAT_CREATE)
    public ChatDTO createChat(@RequestBody @Valid CreateChatRequestDTO chatDTO) {
        SafaUser currentUser = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = fetchAndAuthenticateProjectVersion(chatDTO.getVersionId(), currentUser);
        String title = chatDTO.getTitle();
        return this.getServiceProvider().getChatService().createNewChat(currentUser, projectVersion, title);
    }


    /**
     * Updates chat (e.g. title)
     *
     * @param editRequest The chat to update.
     * @param chatId      ID of chat to edit.
     * @return Updated chat.
     */
    @PutMapping(AppRoutes.Chat.CHAT_UPDATE)
    public ChatDTO updateChatTitle(@RequestBody @Valid EditChatRequestDTO editRequest, @PathVariable UUID chatId) {
        SafaUser currentUser = getServiceProvider().getSafaUserService().getCurrentUser();
        Chat chat = getServiceProvider().getChatService().getChatById(chatId);
        verifyEditOnProjectVersion(currentUser, chat.getProjectVersion());
        return this.getServiceProvider().getChatService().updateChat(chat, editRequest.getTitle(), currentUser);
    }

    /**
     * Retrieves all chats created by user or shared with user.
     *
     * @param projectId Project ID used to retrieve chats for user.
     * @return List of chats accessible to user.
     */
    @GetMapping(AppRoutes.Chat.CHAT_GET)
    public List<ChatDTO> getUserChats(@PathVariable UUID projectId) {
        SafaUser user = getCurrentUser();
        Project project = getResourceBuilder()
            .fetchProject(projectId)
            .asUser(user)
            .withPermissions(Set.of(ProjectPermission.EDIT_DATA))
            .get();
        SafaUser currentUser = getCurrentUser();
        return this.getServiceProvider().getChatService().getUserChats(currentUser, project);
    }

    /**
     * Deletes chat.
     *
     * @param chatId ID of chat to delete.
     */
    @DeleteMapping(AppRoutes.Chat.CHAT_DELETE)
    public void deleteChat(@PathVariable UUID chatId) {
        SafaUser currentUser = getServiceProvider().getSafaUserService().getCurrentUser();
        this.getServiceProvider().getChatService().deleteChat(chatId, currentUser);
    }

    /**
     * Generates new title for chat.
     *
     * @param chatId ID of chat to generate title for.
     * @return Updated ChatDTO.
     */
    @PostMapping(AppRoutes.Chat.CHAT_TITLE)
    public ChatDTO generateChatTitle(@PathVariable UUID chatId) {
        ChatService chatService = getServiceProvider().getChatService();
        Chat chat = chatService.getChatById(chatId);
        ChatPermission chatPermission = chatService.verifyChatPermission(chat, getCurrentUser(), ChatPermission.EDIT);
        String newTitle = chatService.generateChatTitle(chat);
        chat.setTitle(newTitle);
        return ChatDTO.fromChat(chat, chatPermission);
    }

    /**
     * Retrieves project version in chat if user has sufficient permission to access that edit and generate on it.
     *
     * @param versionId Id of version to authenticate and fetch.
     * @param user      The user accessing project version.
     * @return The project version associated with chat.
     */
    private ProjectVersion fetchAndAuthenticateProjectVersion(UUID versionId, SafaUser user) {
        if (versionId == null) {
            throw new SafaError("Version Id not defined on chat.");
        }
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId).get();
        verifyEditOnProjectVersion(user, projectVersion);
        return projectVersion;
    }

    /**
     * Verifies that user has edit permission on project version.
     *
     * @param user           The user to check against project version.
     * @param projectVersion The project version.
     */
    private void verifyEditOnProjectVersion(SafaUser user, ProjectVersion projectVersion) {
        getResourceBuilder()
            .withVersion(projectVersion)
            .asUser(user)
            .withPermissions(Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE))
            .get();
    }
}
