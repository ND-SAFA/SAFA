package edu.nd.crc.safa.features.notifications.members;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.users.entities.IUser;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.MessageChannel;

public class ActiveMembersStore {
    private static final Logger log = LoggerFactory.getLogger(ActiveMembersStore.class);
    private final ConcurrentHashMap<String, ActiveProjectMembership> subscriptionMap = new ConcurrentHashMap<>();
    private final ConcurrentHashMap<UUID, Set<IUser>> projectMap = new ConcurrentHashMap<>();

    /**
     * Adds user to project and links session with user/project membership.
     *
     * @param projectSubscriptionMessage The session containing subscription of user to project.
     */
    public void subscribe(ProjectSubscriptionMessage projectSubscriptionMessage) {
        addProjectSubscriptionToSessionMap(projectSubscriptionMessage);
        addProjectSubscriptionToProjectMap(projectSubscriptionMessage);
        sendActiveUsersInProject(
            projectSubscriptionMessage.getUser(),
            projectSubscriptionMessage.getProjectId(),
            projectSubscriptionMessage.getMessageChannel()
        );
    }

    /**
     * Removes user from project associated with subscription.
     *
     * @param subscriptionId ID of subscription containing project x user relationship.
     * @param messageChannel The channel that the message was received in.
     */
    public void unsubscribe(String subscriptionId, MessageChannel messageChannel) {
        if (!subscriptionMap.containsKey(subscriptionId)) {
            log.debug(String.format("Subscription map does not contain ID: %s", subscriptionId));
            return;
        }
        ActiveProjectMembership activeProjectMembership = subscriptionMap.get(subscriptionId);
        IUser user = activeProjectMembership.getUser();
        UUID projectId = activeProjectMembership.getProjectId();

        Set<IUser> projectUsers = projectMap.get(projectId);
        projectUsers.remove(user);
        sendActiveUsersInProject(user, projectId, messageChannel);
    }

    /**
     * Removes all references to user and sends updates to affected projects.
     *
     * @param user           The user to remove.
     * @param messageChannel The message channel used to send updates.
     */
    public void disconnect(IUser user, MessageChannel messageChannel) {
        List<String> keys = this.subscriptionMap
            .entrySet()
            .stream()
            .filter(e -> e.getValue().getUser().equals(user))
            .map(Map.Entry::getKey).collect(Collectors.toList());
        keys.forEach(this.subscriptionMap::remove);

        for (Map.Entry<UUID, Set<IUser>> entry : this.projectMap.entrySet()) {
            UUID projectId = entry.getKey();
            if (entry.getValue().remove(user)) {
                sendActiveUsersInProject(user, projectId, messageChannel);
            }
        }
    }

    private void addProjectSubscriptionToProjectMap(ProjectSubscriptionMessage projectSubscriptionMessage) {
        UUID projectId = projectSubscriptionMessage.getProjectId();
        projectMap.computeIfAbsent(projectId, id -> new HashSet<>());
        projectMap.get(projectId).add(projectSubscriptionMessage.getUser());
    }

    private void addProjectSubscriptionToSessionMap(ProjectSubscriptionMessage projectSubscriptionMessage) {
        IUser user = projectSubscriptionMessage.getUser();
        UUID projectId = projectSubscriptionMessage.getProjectId();

        if (!subscriptionMap.containsKey(projectSubscriptionMessage.getSubscriptionId())) {
            ActiveProjectMembership activeProjectMembership = new ActiveProjectMembership(user, projectId);
            subscriptionMap.put(projectSubscriptionMessage.getSubscriptionId(), activeProjectMembership);
        }
    }

    private void sendActiveUsersInProject(IUser sender, UUID projectId, MessageChannel messageChannel) {
        Change newActiveMembers = createChange(projectMap.get(projectId));
        EntityChangeMessage message = new EntityChangeMessage(sender, newActiveMembers);
        WebSocketMessageService.sendToProject(projectId, messageChannel, message);
    }

    private Change createChange(Set<IUser> activeUsers) {
        Change change = new Change();
        change.setAction(NotificationAction.UPDATE);
        change.setEntities(new ArrayList<>(activeUsers));
        change.setEntity(NotificationEntity.ACTIVE_MEMBERS);
        return change;
    }
}
