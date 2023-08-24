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
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.generation.summary.GenArtifactSummaryRequest;
import edu.nd.crc.safa.features.generation.summary.TGenSummaryResponse;
import edu.nd.crc.safa.features.generation.tgen.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.generation.tgen.TGenTraceGenerationResponse;
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
    private final ApiController apiController;
    private final ArtifactSummaryApi artifactSummaryApi;
    private final GenerateLinksApi generateLinksApi;

    /**
     * Generates project summary.
     *
     * @param request The request containing project artifacts.
     * @param logger  The job logger.
     * @return The project summary.
     */
    public String generateProjectSummary(ProjectSummaryRequest request, JobLogger logger) {
        String endpoint = TGenConfig.getEndpoint("project-summary");
        ProjectSummaryResponse response = apiController.performJob(endpoint, request,
            ProjectSummaryResponse.class, logger);
        return response.getSummary();
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
    public TGenSummaryResponse generateArtifactSummaries(GenArtifactSummaryRequest request, JobLogger logger) {
        return artifactSummaryApi.sendSummarizeRequest(request, logger);
    }

    /**
     * Performs a completion request to TGen.
     *
     * @param request The request containing prompt.
     * @return The completion string.
     */
    public TGenPromptResponse generatePrompt(TGenPromptRequest request) {
        String generatePromptEndpoint = TGenConfig.getEndpoint("complete");
        return this.requestService.sendPost(generatePromptEndpoint, request, TGenPromptResponse.class);
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
    public TGenTraceGenerationResponse performSearch(TGenPredictionRequestDTO searchRequest, JobLogger logger) {
        int candidates = searchRequest.getDataset().getNumOfCandidates();
        apiController.log(logger, String.format("Number of candidates: %s", candidates));
        String searchEndpoint = TGenConfig.getEndpoint("predict-sync");
        return this.requestService.sendPost(searchEndpoint, searchRequest, TGenTraceGenerationResponse.class);
    }

    /**
     * Terminates the task with given ID.
     *
     * @param taskId The ID of the task to terminate.
     */
    public void cancelJob(UUID taskId) {
        if (taskId == null) {
            throw new AssertionError("Cannot terminate task with ID equal to null.");
        }
        String cancelEndpoint = TGenConfig.getEndpoint("cancel");
        TGenTask task = new TGenTask();
        task.setTaskId(taskId);
        this.requestService.sendPost(cancelEndpoint, task, TGenStatus.class);
    }
}
