package edu.nd.crc.safa.features.chat.controller;

import java.util.List;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.chat.entities.dtos.ChatDTO;
import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
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
    public static final String DEFAULT_TITLE = "Untitled Chat";

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
    public Chat createChat(@RequestBody @Valid ChatDTO chatDTO) {
        SafaUser currentUser = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = fetchAssociatedProjectVersion(chatDTO, currentUser);
        String userTitle = chatDTO.getTitle();
        String title = userTitle == null || userTitle.isBlank() ? DEFAULT_TITLE : userTitle;
        return this.getServiceProvider().getChatService().createNewChat(currentUser, projectVersion, title);
    }


    /**
     * Updates chat (e.g. title)
     *
     * @param chatDTO The chat to update.
     * @return Updated chat.
     */
    @PutMapping(AppRoutes.Chat.CHAT_UPDATE)
    public Chat updateChat(@RequestBody @Valid ChatDTO chatDTO) {
        SafaUser currentUser = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = fetchAssociatedProjectVersion(chatDTO, currentUser);
        return this.getServiceProvider().getChatService().updateChat(chatDTO, currentUser, projectVersion);
    }

    /**
     * Retrieves all chats created by user or shared with user.
     *
     * @return List of chats accessible to user.
     */
    @GetMapping(AppRoutes.Chat.CHAT_GET)
    public List<Chat> getUserChats() {
        SafaUser currentUser = getCurrentUser();
        return this.getServiceProvider().getChatService().getUserChats(currentUser);
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
     * Retrieves project version in chat if user has sufficient permission to access that edit and generate on it.
     *
     * @param chatDTO The chat accessing the project version.
     * @param user    The user accessing project version.
     * @return The project version associated with chat.
     */
    private ProjectVersion fetchAssociatedProjectVersion(ChatDTO chatDTO, SafaUser user) {
        UUID versionId = chatDTO.getVersionId();
        if (versionId == null) {
            throw new SafaError("Version Id not defined on chat.");
        }
        return getResourceBuilder()
            .fetchVersion(chatDTO.getVersionId())
            .asUser(user)
            .withPermissions(Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE))
            .get();
    }
}
