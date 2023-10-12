package edu.nd.crc.safa.test.features.notifications;

import java.util.List;

import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;


class TestProjectSubscriptionCommonRequests extends ApplicationBaseTest {

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
                .project(currentUser)
                .save("project"))
            .and("Root User: Subscribing to project.")
            .notifications((s, n) -> n
                .initializeUser(currentUser, this.token)
                .subscribeToProject(currentUser, s.getProject("project")))
            .and("Root User: Save project message.")
            .notifications(n -> n.getEntityMessage(currentUser)).save("root-project-message")
            .and("Verify project message has root as active user.")
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("root-project-message"), List.of(currentUserName))))
            .and("Creating new user.")
            .actions(a -> a
                .createNewUser(otherUserName, otherUserName))
            .and("New User: Authenticating.")
            .authorize(a -> a.loginUser(otherUserName, otherUserName).save("token"))
            .and("New User: Subscribing to new project and saving project message.")
            .notifications((s, n) -> n
                .subscribeToProject(s.getIUser(otherUserName), s.getProject("project"))
                .getEntityMessage(s.getIUser(otherUserName))).save("otherUserMessage")
            .and("Root User: Saving project message/")
            .notifications((s, n) -> n.getEntityMessage(currentUser)).save("currentUserMessage")
            .and("Verifying that project messages contain two active users.")
            .verify((s, v) -> v
                .notifications(n -> n
                    .verifyMemberNotification(s.getMessage("otherUserMessage"), expectedEmails)
                    .verifyMemberNotification(s.getMessage("currentUserMessage"), expectedEmails)));
    }
}
