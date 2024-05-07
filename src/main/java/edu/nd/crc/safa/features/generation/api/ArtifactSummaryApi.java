package edu.nd.crc.safa.features.generation.api;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.features.generation.summary.SummaryRequest;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ArtifactSummaryApi {
    private static final int SUMMARY_ARTIFACT_THRESHOLD = 1;
    private final GenApiController genApiController;
    private final RequestService requestService;

    /**
     * Performs summarization request. Decides whether to use sync or async endpoint based on threshold.
     *
     * @param payload The request containing artifacts to summarize.
     * @param logger  Optional. Job logger to store logs under.
     * @return Summary response.
     */
    public SummaryResponse sendSummarizeRequest(SummaryRequest payload, JobLogger logger) {
        String predictEndpoint;

        int nArtifacts = payload.getArtifacts().size();
        genApiController.log(logger, String.format("Summarizing %s artifacts.", nArtifacts));
        if (nArtifacts <= SUMMARY_ARTIFACT_THRESHOLD) {
            predictEndpoint = TGenConfig.getEndpoint("summarize-sync");
            return this.genApiController.performRequest(predictEndpoint, payload, SummaryResponse.class);
        } else {
            predictEndpoint = TGenConfig.getEndpoint("summarize");
            return genApiController.performJob(predictEndpoint, payload, SummaryResponse.class, logger);
        }
    }
}
