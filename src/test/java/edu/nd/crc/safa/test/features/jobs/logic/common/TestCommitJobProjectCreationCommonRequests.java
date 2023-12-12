package edu.nd.crc.safa.test.features.jobs.logic.common;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.builders.AbstractJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.utilities.ProjectOwner;

import lombok.Setter;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestCommitJobProjectCreationCommonRequests extends ApplicationBaseTest {

    @Autowired
    ProjectMembershipService projectMemberService;

    @Test
    void testCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommitDefinition, getCurrentUser(), false, false);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(getCurrentUser()).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    void testFailedCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(null, projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommitDefinition, getCurrentUser(), false, true);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(getCurrentUser()).size());

        // Job should not be successful
        assertEquals(-1, result.getCurrentProgress());
    }

    @Test
    void testCommitIntoNewProject() throws Exception {
        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, getCurrentUser(), true, false);
        JobAppEntity result = jobBuilder.perform();

        // New project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(getCurrentUser()).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    void testFailedCommitIntoNewProject() throws Exception {
        assertEquals(0, projectMemberService.getProjectsForUser(getCurrentUser()).size());

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, getCurrentUser(), true, true);
        JobAppEntity result = jobBuilder.perform();

        // New project should be deleted
        assertEquals(0, projectMemberService.getProjectsForUser(getCurrentUser()).size());

        // Job should not be successful
        assertEquals(-1, result.getCurrentProgress());
    }

    public static class DummyCommitJob extends CommitJob {

        @Setter
        boolean failStep = false;

        @Setter
        boolean allowProjectCreation = false;

        SafaUser user;

        protected DummyCommitJob(SafaUser user,
                                 JobDbEntity jobDbEntity,
                                 ServiceProvider serviceProvider,
                                 ProjectCommitDefinition projectCommitDefinition) {
            super(user, jobDbEntity, serviceProvider, projectCommitDefinition, true);
            setProjectCommitDefinition(projectCommitDefinition);
            this.user = user;
        }

        @IJobStep(value = "Creation Optional Project", position = 1)
        public void makeProject() {
            if (allowProjectCreation) {
                createProjectAndCommit(new ProjectOwner(this.user), "test project name", "test project desc");
            }
        }

        @IJobStep(value = "", position = 2)
        public void fail() throws Exception {
            if (failStep) {
                throw new Exception();
            }
        }
    }

    private static class DummyCommitJobBuilder extends AbstractJobBuilder {

        private final boolean allowProjectCreation;
        private final boolean fail;
        private ProjectCommitDefinition commit;

        public DummyCommitJobBuilder(ServiceProvider serviceProvider,
                                     ProjectCommitDefinition commit,
                                     SafaUser user,
                                     boolean allowProjectCreation,
                                     boolean fail) {

            super(user, serviceProvider);
            this.commit = commit;
            this.allowProjectCreation = allowProjectCreation;
            this.fail = fail;
        }

        @Override
        public AbstractJob constructJobForWork() {
            if (this.commit == null) {
                this.commit = new ProjectCommitDefinition();
            }
            DummyCommitJob job = new DummyCommitJob(getUser(),
                this.getJobDbEntity(),
                this.getServiceProvider(),
                this.commit);
            job.setAllowProjectCreation(allowProjectCreation);
            job.setFailStep(fail);
            return job;
        }

        @Override
        public String getJobName() {
            return "dummy job";
        }

        @Override
        public Class<? extends AbstractJob> getJobType() {
            return DummyCommitJob.class;
        }
    }
}
