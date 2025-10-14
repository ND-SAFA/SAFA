package edu.nd.crc.safa.test.features.flatfiles.errors;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.logging.services.JobLoggingService;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.test.features.jobs.base.AbstractUpdateProjectViaFlatFileTestCommonRequests;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Test that project with missing artifact file propagates error.
 */
class TestMissingArtifactFile extends AbstractUpdateProjectViaFlatFileTestCommonRequests {
    final int PARSE_STEP_INDEX = 0;

    @Autowired
    JobService jobService;

    @Autowired
    JobLoggingService jobLogService;

    @Test
    void createProjectWithMissingArtifactFile() throws Exception {
        JSONObject response = updateProjectViaFlatFiles(ProjectPaths.Resources.Tests.MISSING_DATA_FILE,
            status().is2xxSuccessful());

        assertThat(response.getInt("currentProgress")).isEqualTo(-1);
        assertThat(response.getString("status")).isEqualTo("FAILED");

        String jobIdString = response.getString("id");
        UUID jobId = UUID.fromString(jobIdString);
        JobDbEntity job = jobService.getJobById(jobId);

        String missingMessage = "Requirement.csv: Could not find CSV file";
        List<List<JobLogEntry>> logs = jobLogService.getLogsForJob(job);

        List<JobLogEntry> step1Logs = logs.get(PARSE_STEP_INDEX);

        boolean messageFound = step1Logs.stream().anyMatch(log -> log.getEntry().contains(missingMessage));
        assertThat(messageFound).isTrue();
    }
}
