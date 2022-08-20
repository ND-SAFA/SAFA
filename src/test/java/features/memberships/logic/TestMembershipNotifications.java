package features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

import features.base.ApplicationBaseTest;
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

        // Step - Create two users
        authorizationTestService.createUser(newMemberEmail, newMemberPassword);
        authorizationTestService.loginUser(newMemberEmail, newMemberPassword, false);

        // Step - Subscribe to project notifications
        notificationTestService
            .createNewConnection(defaultUser)
            .subscribeToProject(defaultUser, project);

        // Step - Add member to project
        creationTestService.shareProject(project, newMemberEmail, ProjectRole.VIEWER, status().isOk());

        // VP - Verify that single change was broadcast.
        EntityChangeMessage addMemberMessage = notificationTestService.getNextMessage(defaultUser);
        verifyMessageContent(addMemberMessage, Change.Action.UPDATE);

        // Step - Remove member from project
        authorizationTestService.removeMemberFromProject(project, newMemberEmail);

        // VP - Verify that message is sent to update members after deletion
        EntityChangeMessage removeMemberMessage = notificationTestService.getNextMessage(defaultUser);
        verifyMessageContent(removeMemberMessage, Change.Action.DELETE);
    }

    private void verifyMessageContent(EntityChangeMessage message,
                                      Change.Action action) {
        // VP - Verify that only one change was broadcast.
        assertThat(message.getChanges()).hasSize(1);

        // VP - Verify that membership notification is received.
        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(Change.Entity.MEMBERS);
        assertThat(change.getAction()).isEqualTo(action);
        assertThat(change.getEntityIds()).hasSize(1);
    }
}
