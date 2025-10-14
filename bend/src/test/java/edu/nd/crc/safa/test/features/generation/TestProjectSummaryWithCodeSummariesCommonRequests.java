package edu.nd.crc.safa.test.features.generation;

import edu.nd.crc.safa.test.services.requests.GenCommonRequests;
import edu.nd.crc.safa.test.verifiers.TGenTestVerifier;

import org.junit.jupiter.api.Test;

class TestProjectSummaryWithCodeSummariesCommonRequests extends GenerationalTest {

    /**
     * Tests that summaries generated during project summary are saved.
     */
    @Test
    void testCodeSummariesGetGenerated() throws Exception {
        createProject();
        mockProjectSummaryResponse();
        GenCommonRequests.performProjectSummary(getProjectVersion());
        refreshProject();
        TGenTestVerifier.verifyCodeHasSummaries(this);
    }
}
