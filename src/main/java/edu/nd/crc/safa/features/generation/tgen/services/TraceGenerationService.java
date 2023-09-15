package edu.nd.crc.safa.features.generation.tgen.services;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.generation.tgen.entities.ArtifactLevelRequest;
import edu.nd.crc.safa.features.generation.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.generation.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating trace links for given projects.
 */
@Service
@AllArgsConstructor
@Scope("singleton")
public class TraceGenerationService {
    private static final String DELIMITER = "*";
    private ITraceGenerationController traceGenerationController;

    /**
     * Retrieves artifacts associated with the source and target types defined in the tracing request.
     *
     * @param tracingRequest   The request detailing the artifacts to trace and the model to do so with.
     * @param projectAppEntity The project app entity containing artifacts and links.
     * @return TracingPayload detailing the artifacts and the method to trace with.
     */
    public static GenerationDataset extractPayload(TracingRequest tracingRequest,
                                                   ProjectAppEntity projectAppEntity) {
        List<TraceLayer> layers = new ArrayList<>();
        List<GenerationArtifact> generationArtifacts = new ArrayList<>();

        for (ArtifactLevelRequest artifactLevelRequest : tracingRequest.getArtifactLevels()) {
            String childType = artifactLevelRequest.getSource();
            String parentType = artifactLevelRequest.getTarget();

            List<GenerationArtifact> childArtifacts = projectAppEntity
                .getByArtifactType(childType)
                .stream()
                .map(GenerationArtifact::new)
                .collect(Collectors.toList());
            List<GenerationArtifact> parentArtifacts = projectAppEntity
                .getByArtifactType(parentType)
                .stream()
                .map(GenerationArtifact::new)
                .collect(Collectors.toList());
            generationArtifacts.addAll(childArtifacts);
            generationArtifacts.addAll(parentArtifacts);
            layers.add(new TraceLayer(childType, parentType));
        }
        return new GenerationDataset(generationArtifacts, layers);
    }

    public List<TraceAppEntity> generateTraceLinks(TraceGenerationRequest traceGenerationRequest,
                                                   ProjectAppEntity projectAppEntity) {
        List<TraceAppEntity> generatedTraces = new ArrayList<>();
        for (TracingRequest tracingRequest : traceGenerationRequest.getRequests()) {
            GenerationDataset tracingPayload = extractPayload(tracingRequest, projectAppEntity);
            generatedTraces.addAll(generateLinksWithMethod(tracingPayload));
        }
        return generatedTraces;
    }

    public List<TraceAppEntity> generateLinksWithMethod(GenerationDataset tracingPayload) {
        return new ArrayList<>(traceGenerationController.generateLinks(tracingPayload, null));
    }

    public List<TraceAppEntity> filterDuplicateGeneratedLinks(List<TraceAppEntity> manualLinks,
                                                              List<TraceAppEntity> generatedLinks) {
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.getApprovalStatus() == ApprovalStatus.APPROVED)
            .map(link -> link.getSourceName() + DELIMITER + link.getTargetName())
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.getSourceName() + DELIMITER + t.getTargetName();
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }
}
