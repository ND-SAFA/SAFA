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

import lombok.Setter;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestCommitJobProjectCreation extends ApplicationBaseTest {

    @Autowired
    ProjectMembershipService projectMemberService;

    @Test
    public void testCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommitDefinition, currentUser, false, false);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(currentUser).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    public void testFailedCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommitDefinition, currentUser, false, true);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(currentUser).size());

        // Job should not be successful
        assertEquals(-1, result.getCurrentProgress());
    }

    @Test
    public void testCommitIntoNewProject() throws Exception {
        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, currentUser, true, false);
        JobAppEntity result = jobBuilder.perform();

        // New project should be created
        assertEquals(1, projectMemberService.getProjectsForUser(currentUser).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    public void testFailedCommitIntoNewProject() throws Exception {
        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, currentUser, true, true);
        JobAppEntity result = jobBuilder.perform();

        // New project should be deleted
        assertEquals(0, projectMemberService.getProjectsForUser(currentUser).size());

        // Job should not be successful
        assertEquals(-1, result.getCurrentProgress());
    }

    public static class DummyCommitJob extends CommitJob {

        @Setter
        boolean failStep = false;

        @Setter
        boolean allowProjectCreation = false;

        SafaUser newProjectOwner;

        protected DummyCommitJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider,
                                 ProjectCommitDefinition projectCommitDefinition, SafaUser newProjectOwner) {
            super(jobDbEntity, serviceProvider);
            this.newProjectOwner = newProjectOwner;
            setProjectCommitDefinition(projectCommitDefinition);
        }

        @IJobStep(value = "", position = 1)
        public void makeProject() {
            if (getProjectCommitDefinition() == null) {
                if (allowProjectCreation) {
                    createProject(newProjectOwner, "test project name", "test project desc");
                } else {
                    throw new AssertionError("Not allowed to create a new project");
                }
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

        private final ProjectCommitDefinition commit;
        private final boolean allowProjectCreation;
        private final boolean fail;

        public DummyCommitJobBuilder(ServiceProvider serviceProvider,
                                     ProjectCommitDefinition commit,
                                     SafaUser user,
                                     boolean allowProjectCreation,
                                     boolean fail) {

            super(serviceProvider, user);
            this.commit = commit;
            this.allowProjectCreation = allowProjectCreation;
            this.fail = fail;
        }

        @Override
        public AbstractJob constructJobForWork() {
            DummyCommitJob job = new DummyCommitJob(this.getJobDbEntity(), this.getServiceProvider(),
                this.commit, this.getUser());
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
