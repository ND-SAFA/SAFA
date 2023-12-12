package edu.nd.crc.safa.features.generation.api;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryRequest;
import edu.nd.crc.safa.features.generation.projectsummary.ProjectSummaryResponse;
import edu.nd.crc.safa.features.generation.prompt.PromptResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.generation.summary.GenArtifactSummaryRequest;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.generation.tgen.TGenRequest;
import edu.nd.crc.safa.features.generation.tgen.TGenResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
@Service
@AllArgsConstructor
public class GenApi implements ITraceGenerationController {
    private final RequestService requestService;
    private final ArtifactSummaryApi artifactSummaryApi;
    private final GenerateLinksApi generateLinksApi;
    private final ApiController apiController;

    /**
     * Generates project summary.
     *
     * @param request The request containing project artifacts.
     * @param logger  The job logger.
     * @return The project summary.
     */
    public ProjectSummaryResponse generateProjectSummary(ProjectSummaryRequest request, JobLogger logger) {
        String endpoint = TGenConfig.getEndpoint("project-summary");
        return apiController.performJob(endpoint, request,
            ProjectSummaryResponse.class, logger);
    }

    /**
     * Creates hierarchy of artifacts for artifacts.
     *
     * @param request   The request detailing clusters of artifacts.
     * @param jobLogger The logger to store logs under.
     * @return The generated artifacts per cluster.
     */
    public HGenResponse generateHierarchy(TGenHGenRequest request, JobLogger jobLogger) {
        String summarizeEndpoint = TGenConfig.getEndpoint("hgen");
        return apiController.performJob(summarizeEndpoint, request, HGenResponse.class, jobLogger);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and associated parameters.
     * @param logger  Optional logger for relaying log messages.
     * @return TGen response.
     */
    public SummaryResponse generateArtifactSummaries(GenArtifactSummaryRequest request, JobLogger logger) {
        return artifactSummaryApi.sendSummarizeRequest(request, logger);
    }

    /**
     * Performs a completion request to TGen.
     *
     * @param request The request containing prompt.
     * @return The completion string.
     */
    public PromptResponse generatePrompt(TGenPromptRequest request) {
        String generatePromptEndpoint = TGenConfig.getEndpoint("complete");
        return this.requestService.sendPost(generatePromptEndpoint, request, PromptResponse.class);
    }

    /**
     * Generates trace links between the linked layers in the dataset.
     *
     * @param dataset The dataset to trace.
     * @param logger  The logger used to store trace logs.
     * @return The list of trace links.
     */
    public List<TraceAppEntity> generateLinks(GenerationDataset dataset, JobLogger logger) {
        return generateLinksApi.generateLinks(dataset, logger);
    }

    /**
     * Performs search on the linked layers in the dataset.
     *
     * @param searchRequest The search request containing the dataset.
     * @param logger        The logger to store the logs under.
     * @return The response containing the predicted links.
     */
    public TGenResponse performSearch(TGenRequest searchRequest, JobLogger logger) {
        int candidates = searchRequest.getDataset().getNumOfCandidates();
        apiController.log(logger, String.format("Number of candidates: %s", candidates));
        String searchEndpoint = TGenConfig.getEndpoint("tgen-sync");
        return this.requestService.sendPost(searchEndpoint, searchRequest, TGenResponse.class);
    }

    /**
     * Terminates the task with given ID.
     *
     * @param taskId The ID of the task to terminate.
     */
    public void cancelJob(UUID taskId) {
        if (taskId == null) {
            return;
        }
        String cancelEndpoint = TGenConfig.getEndpoint("cancel");
        TGenTask task = new TGenTask();
        task.setTaskId(taskId);
        TGenStatus status = this.requestService.sendPost(cancelEndpoint, task, TGenStatus.class);
    }
}
