package edu.nd.crc.safa.test.features.generation;

import edu.nd.crc.safa.test.services.CommonRequestService;
import edu.nd.crc.safa.test.verifiers.TGenTestVerifier;

import org.junit.jupiter.api.Test;

class TestProjectSummaryWithCodeSummaries extends GenerationalTest {

    /**
     * Tests that summaries generated during project summary are saved.
     */
    @Test
    void testCodeSummariesGetGenerated() throws Exception {
        createProject();
        mockProjectSummaryResponse();
        CommonRequestService.Gen.performProjectSummary(getProjectVersion());
        refreshProject();
        TGenTestVerifier.verifyCodeHasSummaries(this);
    }
}
