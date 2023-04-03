package edu.nd.crc.safa.test.features.jobs.logic.common;

import static org.junit.jupiter.api.Assertions.assertEquals;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.builders.AbstractJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import lombok.Setter;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestCommitJobProjectCreation extends ApplicationBaseTest {

    @Autowired
    ProjectService projectService;

    @Test
    public void testCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommit projectCommit = new ProjectCommit(projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommit, currentUser, false, false);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectService.getProjectsForUser(currentUser).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    public void testFailedCommitIntoExistingProject() throws Exception {
        ProjectVersion projectVersion = dbEntityBuilder.newProject(projectName).newVersionWithReturn(projectName);
        ProjectCommit projectCommit = new ProjectCommit(projectVersion, true);

        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, projectCommit, currentUser, false, true);
        JobAppEntity result = jobBuilder.perform();

        // No new project should be created
        assertEquals(1, projectService.getProjectsForUser(currentUser).size());

        // Job should not be successful
        assertEquals(-1, result.getCurrentProgress());
    }

    @Test
    public void testCommitIntoNewProject() throws Exception {
        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, currentUser, true, false);
        JobAppEntity result = jobBuilder.perform();

        // New project should be created
        assertEquals(1, projectService.getProjectsForUser(currentUser).size());

        // Job should be successful
        assertEquals(100, result.getCurrentProgress());
    }

    @Test
    public void testFailedCommitIntoNewProject() throws Exception {
        DummyCommitJobBuilder jobBuilder =
            new DummyCommitJobBuilder(serviceProvider, null, currentUser, true, true);
        JobAppEntity result = jobBuilder.perform();

        // New project should be deleted
        assertEquals(0, projectService.getProjectsForUser(currentUser).size());

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
                                 ProjectCommit projectCommit, SafaUser newProjectOwner) {
            super(jobDbEntity, serviceProvider);
            this.newProjectOwner = newProjectOwner;
            setProjectCommit(projectCommit);
        }

        @IJobStep(value = "", position = 1)
        public void makeProject() {
            if (getProjectCommit() == null) {
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

    private static class DummyCommitJobBuilder extends AbstractJobBuilder<ProjectVersion> {

        private final ProjectCommit commit;
        private final boolean allowProjectCreation;
        private final boolean fail;

        public DummyCommitJobBuilder(ServiceProvider serviceProvider,
                                     ProjectCommit commit,
                                     SafaUser user,
                                     boolean allowProjectCreation,
                                     boolean fail) {

            super(serviceProvider);
            this.commit = commit;
            this.allowProjectCreation = allowProjectCreation;
            this.fail = fail;
            this.user = user;
        }

        @Override
        public ProjectVersion constructIdentifier() {
            return null;
        }

        @Override
        public AbstractJob constructJobForWork() {
            DummyCommitJob job = new DummyCommitJob(this.jobDbEntity, this.serviceProvider, this.commit, this.user);
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
