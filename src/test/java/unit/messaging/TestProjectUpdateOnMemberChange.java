package unit.messaging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.app.ProjectMessage;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;

import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that notifications are sent to subscribed users when a member is
 * added or removed from a project.
 */
public class TestProjectUpdateOnMemberChange extends ApplicationBaseTest {

    @Test
    public void canSendAndReceiveMessagesBetweenClients() throws Exception {
        String projectName = "add-member-websocket-message";

        String projectMemberUsername = "user@gmail.com";
        String projectMemberPassword = "password";

        // Step - Create project version to collaborate on
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);

        // Step - Create two users
        createUser(projectMemberUsername, projectMemberPassword);
        loginUser(projectMemberUsername, projectMemberPassword, false);

        // Step - Create two client and subscript to version
        createNewConnection(currentUsername)
            .subscribeToProject(currentUsername, project);

        // Step - Upload flat files
        shareProject(project, projectMemberUsername, ProjectRole.VIEWER, status().isOk());

        // VP - Artifact and traces received
        String message = getNextMessage(currentUsername);
        assertThat(message).isEqualTo(ProjectMessage.MEMBERS.toString());

        // Step - Remove member from project
        removeMemberFromProject(project, projectMemberUsername);

        // VP - Verify that message is sent to update members after deletion
        message = getNextMessage(currentUsername);
        assertThat(message).isEqualTo(ProjectMessage.MEMBERS.toString());
    }
}
