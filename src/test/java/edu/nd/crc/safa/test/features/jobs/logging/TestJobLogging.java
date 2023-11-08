package edu.nd.crc.safa.test.features.jobs.logging;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntryAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.jobs.base.JobTestService;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestJobLogging extends ApplicationBaseTest {

    private static final String logMessageFormat = "test log message %d";
    private static final int logMessageArg = 5;
    private static final String logMessageExpectation = String.format(logMessageFormat, logMessageArg);
    private static final String logMessageUnformatted = "another test log message";

    @BeforeEach
    public void setup() {
        AuthorizationSetter.setSessionAuthorization(currentUserName, serviceProvider);
    }

    @Test
    public void test() throws Exception {

        JobDbEntity jobDbEntity = this.jobService.createNewJob(TestJob.class, "Job Name");
        TestJob job = new TestJob(jobDbEntity, serviceProvider);
        serviceProvider
            .getJobService()
            .executeJob(serviceProvider, job);

        JobTestService.verifyJobWasCompleted(serviceProvider, jobDbEntity.getId(), 5);

        List<List<JobLogEntryAppEntity>> allLogs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID)
            .withJob(jobDbEntity)
            .getAsType(new TypeReference<>() {
            });

        assertThat(allLogs.size()).isEqualTo(5);

        List<JobLogEntryAppEntity> step1Logs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
            .withJob(jobDbEntity)
            .withStepNum(0)
            .getAsType(new TypeReference<>() {
            });

        List<JobLogEntryAppEntity> step2Logs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
            .withJob(jobDbEntity)
            .withStepNum(1)
            .getAsType(new TypeReference<>() {
            });

        List<JobLogEntryAppEntity> step3Logs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
            .withJob(jobDbEntity)
            .withStepNum(2)
            .getAsType(new TypeReference<>() {
            });

        List<JobLogEntryAppEntity> step4Logs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
            .withJob(jobDbEntity)
            .withStepNum(3)
            .getAsType(new TypeReference<>() {
            });

        List<JobLogEntryAppEntity> step5Logs = SafaRequest
            .withRoute(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
            .withJob(jobDbEntity)
            .withStepNum(4)
            .getAsType(new TypeReference<>() {
            });

        assertThat(allLogs).isEqualTo(List.of(step1Logs, step2Logs, step3Logs, step4Logs, step5Logs));

        assertThat(step1Logs.size()).isEqualTo(1);
        assertThat(step2Logs.size()).isEqualTo(1);
        assertThat(step3Logs.size()).isEqualTo(1);
        assertThat(step4Logs.size()).isEqualTo(0);
        assertThat(step5Logs.size()).isEqualTo(0);

        assertThat(step1Logs.get(0).getEntry()).isEqualTo(logMessageExpectation);
        assertThat(step2Logs.get(0).getEntry()).isEqualTo(logMessageUnformatted);
        assertTrue(step3Logs.get(0).getEntry().startsWith("java.lang.Exception: This is a test exception\n"
            + "\tat edu.nd.crc.safa.test.features.jobs.logging.TestJobLogging$TestJob"
            + ".testLogException(TestJobLogging.java:"));
    }

    public static class TestJob extends AbstractJob {

        protected TestJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
            super(jobDbEntity, serviceProvider);
        }

        @IJobStep(position = 1, value = "Test Formatted")
        public void testLogMessageFormatted(JobLogger logger) {
            logger.log(logMessageFormat, logMessageArg);
        }

        @IJobStep(position = 2, value = "Test Unformatted")
        public void testLogMessageUnformatted(JobLogger logger) {
            logger.log(logMessageUnformatted);
        }

        @IJobStep(position = 3, value = "Test Exception")
        public void testLogException(JobLogger logger) {
            try {
                throw new Exception("This is a test exception");
            } catch (Exception e) {
                logger.logException(e);
            }
        }

        @IJobStep(position = 4, value = "Test No Log")
        public void testNoLog() {
        }

        @Override
        protected UUID getCompletedEntityId() {
            return null;
        }
    }
}
