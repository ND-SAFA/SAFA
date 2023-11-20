package edu.nd.crc.safa.test.features.jobs;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.builders.AbstractJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.SimplePermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestJobPermissions extends AbstractPermissionViolationTest {

    @MockBean
    private GenApi genApi;

    @Test
    public void testGetProjectJobs() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jobs.Meta.GET_PROJECT_JOBS)
                .withProject(project)
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }

    @Test
    public void testDeleteJob() throws Exception {
        JobAppEntity job = new TestJobBuilder(getCurrentUser(), serviceProvider).perform();
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jobs.Meta.DELETE_JOB)
                .withJob(job)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of((SimplePermission) () -> "delete_job")
        );
    }

    @Test
    public void testFlatFileUpdate() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jobs.Projects.UPDATE_PROJECT_VIA_FLAT_FILES)
                .withVersion(projectVersion)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA)
        );
    }

    @Test
    public void testGenerateTraces() {
        TGenRequestAppEntity body = new TGenRequestAppEntity();
        body.addTracingRequest("child", "parent");
        body.setProjectVersion(projectVersion);
        test(
            () -> SafaRequest.withRoute(AppRoutes.Jobs.Traces.GENERATE)
                .postWithJsonObject(body, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE)
        );
    }

    @Override
    public ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }

    private static class TestJob extends AbstractJob {

        protected TestJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
            super(jobDbEntity, serviceProvider);
        }

        @Override
        protected UUID getCompletedEntityId() {
            return UUID.randomUUID();
        }
    }

    private static class TestJobBuilder extends AbstractJobBuilder {

        protected TestJobBuilder(SafaUser user, ServiceProvider serviceProvider) {
            super(user, serviceProvider);
        }

        @Override
        protected AbstractJob constructJobForWork() throws IOException {
            return new TestJob(getJobDbEntity(), getServiceProvider());
        }

        @Override
        protected String getJobName() {
            return "Test Job";
        }

        @Override
        protected Class<? extends AbstractJob> getJobType() {
            return TestJob.class;
        }
    }
}
