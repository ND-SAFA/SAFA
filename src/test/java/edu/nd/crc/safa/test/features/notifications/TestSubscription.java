package edu.nd.crc.safa.test.features.notifications;

import static org.junit.Assert.assertEquals;

import edu.nd.crc.safa.features.notifications.MemberNotification;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;

public class TestSubscription extends ApplicationBaseTest {
    @Test
    public void testSubscription() throws Exception {
        ProjectVersion projectVersion = creationService.createDefaultProject(projectName);

        this.notificationService
            .createNewConnection(defaultUser, token)
            .subscribeUser(defaultUser, currentUser.getUserId());

        this.notificationService
            .subscribeProject(defaultUser, projectVersion.getProject())

        MemberNotification memberNotification = this.notificationService.getNextMessage(defaultUser, MemberNotification.class);
        assertEquals(1, memberNotification.getEntity().size());
        UserAppEntity user = memberNotification.getEntity().get(0);
        assertEquals(defaultUser, user.getEmail());

        String otherUserName = "other@gmail.com";
        String otherPassword = "password";

        this.authorizationService.createUser(otherUserName, otherPassword);
        String otherToken = this.authorizationService.loginUser(otherUserName, otherPassword);
        this.notificationService
            .createNewConnection(otherUserName, otherToken)
            .subscribeUser()
    }
}
