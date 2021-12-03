package unit.project.sharing;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.json.JSONObject;
import org.springframework.test.web.servlet.ResultMatcher;
import unit.ApplicationBaseTest;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class BaseSharingTest extends ApplicationBaseTest {

    protected final String otherUserEmail = "doesNotExist@gmail.com";
    protected final String otherUserPassword = "somePassword";

    protected Project createAndShareProject(String projectName) throws Exception {
        // Step - Create other user to share project with.
        SafaUser otherUser = new SafaUser();
        otherUser.setEmail(this.otherUserEmail);
        otherUser.setPassword(this.otherUserPassword);
        this.safaUserRepository.save(otherUser);

        // Step - Create project to share
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Share project
        shareProject(project, otherUser.getEmail(), ProjectRole.VIEWER, status().is2xxSuccessful());

        return project;
    }

    protected JSONObject shareProject(Project project,
                                      String email,
                                      ProjectRole role,
                                      ResultMatcher httpResult) throws Exception {
        ProjectMembershipRequest request = new ProjectMembershipRequest(email, role);
        String url = RouteBuilder.withRoute(AppRoutes.Projects.addProjectMember).withProject(project).get();
        return sendPost(url, toJson(request), httpResult);
    }
}
