package edu.nd.crc.safa.test.features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;

/**
 * Tests that concurrent users are notified when:
 * - member is added to the project
 * - member is deleted from a project
 */
class TestMembershipNotifications extends ApplicationBaseTest {

    @Test
    void membershipChangeNotifications() throws Exception {
        String newMemberEmail = "user@gmail.com";
        String newMemberPassword = "password";

        // Step - Create project version to collaborate on
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Subscribe to project notifications
        notificationService.initializeUser(currentUser, this.token);
        notificationService.subscribeToProject(currentUser, project);

        this.assertionService.verifyActiveMembers(List.of(currentUser), this.notificationService);

        // Step - Create two users
        authorizationService.createUser(newMemberEmail, newMemberPassword);
        authorizationService.loginUser(newMemberEmail, newMemberPassword, false);

        // Step - Add member to project
        creationService.shareProject(project, newMemberEmail, ProjectRole.VIEWER, status().isOk());

        // VP - Verify that single change was broadcast.
        EntityChangeMessage addMemberMessage = notificationService.getEntityMessage(currentUser);
        verifyMessageContent(addMemberMessage, NotificationAction.UPDATE);

        // Step - Remove member from project
        authorizationService.removeMemberFromProject(project, newMemberEmail);

        // VP - Verify that message is sent to update members after deletion
        EntityChangeMessage removeMemberMessage = notificationService.getEntityMessage(currentUser);
        verifyMessageContent(removeMemberMessage, NotificationAction.DELETE);
    }

    private void verifyMessageContent(EntityChangeMessage message,
                                      NotificationAction action) {
        // VP - Verify that only one change was broadcast.
        assertThat(message.getChanges()).hasSize(1);

        // VP - Verify that membership notification is received.
        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(NotificationEntity.MEMBERS);
        assertThat(change.getAction()).isEqualTo(action);
        assertThat(change.getEntityIds()).hasSize(1);
    }
}
