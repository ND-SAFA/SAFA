package edu.nd.crc.safa.test.features.notifications;

import java.util.List;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;


class TestProjectSubscriptionMessageCommonRequests extends ApplicationBaseTest {

    /**
     * Tests server's ability to contain active members working on a project.
     */
    @Test
    void testSubscription() {
        String otherUserName = "other@gmail.com";
        List<String> expectedEmails = List.of(currentUserName, otherUserName);
        this.rootBuilder
            .log("Creating base project.")
            .build((s, v) -> v
                .project(getCurrentUser())
                .save("project"))
            .and("Root User: Subscribing to project.")
            .notifications((s, n) -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToProject(getCurrentUser(), s.getProject("project")))
            .and("Root User: Save project message.")
            .actions(a -> a.verifyActiveMembers(getCurrentUser(), List.of(currentUserName)))
            .and("Creating new user.")
            .actions(a -> a
                .createNewUser(otherUserName, otherUserName, false, this))
            .and("Root User: Sharing project with new user")
            .request((s, r) -> r.project().addUserToProject(s.getProject("project"), otherUserName,
                ProjectRole.VIEWER, getCurrentUser()))
            .and()
            .notifications((s, n) -> n
                    .getEntityMessage(getCurrentUser()))
            .and("New User: Subscribing to new project and saving project message.")
            .notifications((s, n) -> n
                .subscribeToProject(s.getIUser(otherUserName), s.getProject("project"))
                .getEntityMessage(s.getIUser(otherUserName))).save("otherUserMessage")
            .and("Root User: Saving project message/")
            .notifications((s, n) -> n
                .getEntityMessage(getCurrentUser())).save("currentUserMessage")
            .and("Verifying that project messages contain two active users.")
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("otherUserMessage"), expectedEmails)
                    .verifyMemberNotification(s.getMessage("currentUserMessage"), expectedEmails)));
    }
}
