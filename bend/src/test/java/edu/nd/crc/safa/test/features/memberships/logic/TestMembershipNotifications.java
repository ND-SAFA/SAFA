package edu.nd.crc.safa.test.features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
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
        this.rootBuilder
            .build((s, b) -> b.project(getCurrentUser()).save("project"))
            .and()
            .notifications((s, n) -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToProject(getCurrentUser(), s.getProject("project")))
            .and()
            .actions(a -> a.verifyActiveMembers(getCurrentUser(), List.of(currentUserName)))
            .and()
            .actions(a -> a
                .createNewUser(newMemberEmail, newMemberPassword, false, this))
            .and()
            .request((s, r) -> r
                .project()
                .addUserToProject(s.getProject("project"), newMemberEmail, ProjectRole.VIEWER, getCurrentUser()))
            .and()
            .notifications((s, n) -> n
                .getEntityMessage(getCurrentUser()))
            .map(m -> verifyMessageContent(m, NotificationAction.UPDATE))
            .and()
            .authorize((s, a) -> a
                .removeMemberFromProject(s.getProject("project"), newMemberEmail))
            .and()
            .notifications((s, n) -> n
                .getEntityMessage(getCurrentUser()))
            .map(m -> verifyMessageContent(m, NotificationAction.DELETE));
    }

    private TestMembershipNotifications verifyMessageContent(EntityChangeMessage message,
                                                             NotificationAction action) {
        // VP - Verify that only one change was broadcast.
        assertThat(message.getChanges()).hasSize(1);

        // VP - Verify that membership notification is received.
        Change change = message.getChanges().get(0);
        assertThat(change.getEntity()).isEqualTo(NotificationEntity.MEMBERS);
        assertThat(change.getAction()).isEqualTo(action);
        assertThat(change.getEntityIds()).hasSize(1);
        return this;
    }
}
