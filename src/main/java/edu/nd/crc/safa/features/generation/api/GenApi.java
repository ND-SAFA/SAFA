package edu.nd.crc.safa.features.generation.api;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.chat.entities.dtos.gen.GenChatMessage;
import edu.nd.crc.safa.features.chat.entities.dtos.gen.GenChatRequest;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;
import edu.nd.crc.safa.features.chat.entities.persistent.GenChatResponse;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.generation.summary.SummaryRequest;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.generation.tgen.TGenRequest;
import edu.nd.crc.safa.features.generation.tgen.TGenResponse;
import edu.nd.crc.safa.features.health.HealthConstants;
import edu.nd.crc.safa.features.health.HealthGenRequest;
import edu.nd.crc.safa.features.health.HealthGenResponse;
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
    private final GenApiController genApiController;

    /**
     * Generates health check for target artifacts.
     *
     * @param projectArtifacts List of artifacts in project.
     * @param targetArtifact   Target artifact to generate health checks for.
     * @return Health checks generated for artifact.
     */
    public HealthGenResponse generateHealthChecks(List<GenerationArtifact> projectArtifacts,
                                                  GenerationArtifact targetArtifact) {
        GenerationDataset dataset = new GenerationDataset(projectArtifacts);
        HealthGenRequest request = new HealthGenRequest(dataset, targetArtifact.getId(), HealthConstants.CONCEPT_TYPE);
        String chatEndpoint = TGenConfig.getEndpoint(HealthConstants.ENDPOINT);
        return genApiController.performJob(chatEndpoint, request, HealthGenResponse.class, null);
    }

    /**
     * Sends request to GEN to response to chat message.
     *
     * @param userMessageContent User message to respond to.
     * @param chatMessages       Previous messages in chat.
     * @param artifacts          Projects artifacts used in context.
     * @return Gen chat response.
     */
    public GenChatResponse generateChatResponse(String userMessageContent,
                                                List<ChatMessage> chatMessages,
                                                List<GenerationArtifact> artifacts) {
        GenerationDataset dataset = new GenerationDataset(artifacts);
        List<GenChatMessage> chatHistory = chatMessages
            .stream()
            .map(GenChatMessage::new)
            .collect(Collectors.toList());
        chatHistory.add(GenChatMessage.fromUserMessage(userMessageContent));
        GenChatRequest request = new GenChatRequest(dataset, chatHistory);
        String chatEndpoint = TGenConfig.getEndpoint("chat");
        return genApiController.performJob(chatEndpoint, request, GenChatResponse.class, null);
    }

    /**
     * Generates project summary.
     *
     * @param request The request containing project artifacts.
     * @param logger  The job logger.
     * @return The project summary.
     */
    public SummaryResponse generateProjectSummary(SummaryRequest request, JobLogger logger) {
        return artifactSummaryApi.sendSummarizeRequest(request, logger);
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
        return genApiController.performJob(summarizeEndpoint, request, HGenResponse.class, jobLogger);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and associated parameters.
     * @param logger  Optional logger for relaying log messages.
     * @return TGen response.
     */
    public SummaryResponse generateArtifactSummaries(SummaryRequest request, JobLogger logger) {
        return artifactSummaryApi.sendSummarizeRequest(request, logger);
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
        genApiController.log(logger, String.format("Number of candidates: %s", candidates));
        String searchEndpoint = TGenConfig.getEndpoint("tgen-sync");
        return this.genApiController.sendGenRequest(searchEndpoint, searchRequest, TGenResponse.class);
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
        TGenStatus status = this.genApiController.sendGenRequest(cancelEndpoint, task, TGenStatus.class);
    }
}
