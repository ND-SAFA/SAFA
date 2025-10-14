package edu.nd.crc.safa.test.features.jobs;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.HGenJob;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Test;

class TestJobRetrieval extends ApplicationBaseTest {
    String otherUserName = "other-usename@email.com";
    String otherPassword = "other-password";

    /**
     * Verifies that user is able to retrieve jobs they created.
     */
    @Test
    void testUserJobs() throws Exception {
        Project project = createBothJobs(false, currentUserName);
        assertJobs(project, 1, 0);
    }

    /**
     * Verifies that linked project job appears for user.
     */
    @Test
    void testProjectJobs() throws Exception {
        Project project = createBothJobs(true, currentUserName);
        assertJobs(project, 1, 1);
    }

    @Test
    void otherUserJobs() throws Exception {
        Project project = createBothJobs(true, currentUserName);
        assertJobs(project, 1, 1);

        // Setup new user
        this.rootBuilder
            .log("Creating new user")
            .authorize(a -> a.createUser(otherUserName, otherPassword))
            .and("Sharing project with new user")
            .request(r -> r.project().addUserToProject(project, otherUserName, ProjectRole.VIEWER, getCurrentUser()))
            .and("Setting current user as the new user.")
            .authorize(a -> a.loginUser(otherUserName, otherPassword, this));

        assertJobs(project, 0, 1);
    }

    private Project createBothJobs(boolean linkJobToProject, String userName) {
        AuthorizationSetter.setSessionAuthorization(userName, this.serviceProvider);
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        JobDbEntity job = this.jobService.createNewJob(HGenJob.class, "hgen");

        if (linkJobToProject) {
            job.setProject(project);
            this.serviceProvider.getJobRepository().save(job);
        }
        return project;
    }

    private void assertJobs(Project project, int nUser, int nProject) throws Exception {
        List<JobAppEntity> userJobs = CommonProjectRequests.getUserJobs();
        List<JobAppEntity> projectJobs = CommonProjectRequests.getProjectJobs(project);

        assertEquals(nUser, userJobs.size(), "User Jobs");
        assertEquals(nProject, projectJobs.size(), "Project Jobs");
    }
}
