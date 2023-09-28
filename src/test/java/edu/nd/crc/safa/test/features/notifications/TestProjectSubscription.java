package edu.nd.crc.safa.test.features.notifications;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;


class TestProjectSubscription extends ApplicationBaseTest {

    /**
     * Tests server's ability to contain active members working on a project.
     */
    @Test
    void testSubscription() throws Exception {
        ProjectVersion projectVersion = creationService.createProjectWithNewVersion(projectName);

        this.notificationService.initializeUser(currentUser, this.token);
        this.notificationService.subscribeToProject(currentUser, projectVersion.getProject());

        verifyMemberNotification(currentUser, List.of(currentUserName));

        String otherUserName = "other@gmail.com";
        IUser otherUser = createNewUser(otherUserName, "password");
        this.notificationService.subscribeToProject(otherUser, projectVersion.getProject());

        verifyMemberNotification(otherUser, List.of(currentUserName, otherUserName));
        verifyMemberNotification(currentUser, List.of(currentUserName, otherUserName));
    }

    private void verifyMemberNotification(IUser user, List<String> emails) throws Exception {
        EntityChangeMessage memberNotification = this.notificationService.getEntityMessage(user);
        assertEquals(1, memberNotification.getChanges().size());
        Change change = memberNotification.getChanges().get(0);
        assertEquals(emails.size(), change.getEntities().size());
        List<String> projectMembers = change
            .getEntities()
            .stream()
            .map(a -> (UserAppEntity) a)
            .map(UserAppEntity::getEmail)
            .collect(Collectors.toList());
        assertEquals(emails, projectMembers);
    }

    private IUser createNewUser(String userName, String password) throws Exception {
        UserAppEntity otherUser = this.authorizationService.createUser(userName, password);
        String otherToken = this.authorizationService.loginUser(userName, password);
        this.notificationService.initializeUser(otherUser, otherToken);
        return otherUser;
    }
}
