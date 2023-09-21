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
import edu.nd.crc.safa.test.services.CommonRequestService;

import org.junit.jupiter.api.Test;

class TestJobRetrieval extends ApplicationBaseTest {
    String otherUserName = "other-usename@email.com";
    String otherPassword = "other-password";

    /**
     * Verifies that user is able to retrieve jobs they created.
     */
    @Test
    void testUserJobs() throws Exception {
        Project project = createBothJobs(false, defaultUser);
        assertJobs(project, 1, 0);
    }

    /**
     * Verifies that linked project job appears for user.
     */
    @Test
    void testProjectJobs() throws Exception {
        Project project = createBothJobs(true, defaultUser);
        assertJobs(project, 1, 1);
    }

    @Test
    void otherUserJobs() throws Exception {
        Project project = createBothJobs(true, defaultUser);
        assertJobs(project, 1, 1);

        // Setup new user
        this.authorizationService.createUser(otherUserName, otherPassword);
        creationService.shareProject(project, otherUserName, ProjectRole.VIEWER);
        authorizationService.loginUser(otherUserName, otherPassword);

        assertJobs(project, 0, 1);
    }

    private Project createBothJobs(boolean linkJobToProject, String userName) {
        AuthorizationSetter.setSessionAuthorization(userName, this.serviceProvider);
        Project project = this.dbEntityBuilder.newProjectWithReturn(projectName);
        JobDbEntity job = this.jobService.createNewJob(HGenJob.class, "hgen");

        if (linkJobToProject) {
            job.setCompletedEntityId(project.getProjectId());
            this.serviceProvider.getJobRepository().save(job);
        }
        return project;
    }

    private void assertJobs(Project project, int nUser, int nProject) throws Exception {
        List<JobAppEntity> userJobs = CommonRequestService.getUserJobs();
        List<JobAppEntity> projectJobs = CommonRequestService.getProjectJobs(project);

        assertEquals(nUser, userJobs.size());
        assertEquals(nProject, projectJobs.size());
    }
}
