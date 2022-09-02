package edu.nd.crc.safa.features.tgen.generator;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.tgen.entities.ArtifactTypeTraceGenerationRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationMethod;
import edu.nd.crc.safa.features.tgen.method.TBert;
import edu.nd.crc.safa.features.tgen.method.vsm.VSMController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

import lombok.AllArgsConstructor;
import org.apache.commons.lang3.NotImplementedException;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating trace links for given projects.
 */
@Service
@AllArgsConstructor
public class TraceGenerationService {
    private static final String DELIMITER = "*";
    private final SafaRequestBuilder safaRequestBuilder;

    public List<TraceAppEntity> generateTraceLinks(List<ArtifactAppEntity> artifacts,
                                                   List<ArtifactTypeTraceGenerationRequestDTO> requests) {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();

        for (ArtifactTypeTraceGenerationRequestDTO request : requests) {
            String sourceArtifactType = request.getSourceTypeName();
            String targetArtifactType = request.getTargetTypeName();

            List<ArtifactAppEntity> sourceArtifacts = artifacts
                .stream()
                .filter(a -> a.getType().equalsIgnoreCase(sourceArtifactType))
                .collect(Collectors.toList());
            List<ArtifactAppEntity> targetArtifacts = artifacts
                .stream()
                .filter(a -> a.getType().equalsIgnoreCase(targetArtifactType))
                .collect(Collectors.toList());
            generatedLinks.addAll(generateLinksWithMethod(
                sourceArtifacts,
                targetArtifacts,
                request.getTraceGenerationMethod()));
        }
        return generatedLinks;
    }

    public List<TraceAppEntity> generateLinksWithMethod(List<ArtifactAppEntity> sourceArtifacts,
                                                        List<ArtifactAppEntity> targetArtifacts,
                                                        TraceGenerationMethod traceGenerationMethod) {
        ITraceLinkGeneration generationMethod = buildGenerationMethod(traceGenerationMethod);
        return generationMethod.generateLinks(sourceArtifacts, targetArtifacts);
    }

    public List<TraceAppEntity> filterDuplicateGeneratedLinks(List<TraceAppEntity> manualLinks,
                                                              List<TraceAppEntity> generatedLinks) {
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.getApprovalStatus().equals(ApprovalStatus.APPROVED))
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

    private ITraceLinkGeneration buildGenerationMethod(TraceGenerationMethod traceGenerationMethod) {
        switch (traceGenerationMethod) {
            case VSM:
                return new VSMController();
            case TBERT:
                return new TBert(safaRequestBuilder);
            default:
                throw new NotImplementedException("Trace method not implemented:" + traceGenerationMethod);
        }
    }


}
