package edu.nd.crc.safa.features.tgen.generator;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.tgen.entities.ArtifactTypeTraceGenerationRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.tgen.method.bert.NLBert;
import edu.nd.crc.safa.features.tgen.method.bert.PLBert;
import edu.nd.crc.safa.features.tgen.method.vsm.VSMController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

import lombok.AllArgsConstructor;
import org.apache.commons.lang3.NotImplementedException;
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
    private final SafaRequestBuilder safaRequestBuilder;

    public List<TraceAppEntity> generateTraceLinks(List<ArtifactAppEntity> artifacts,
                                                   List<ArtifactTypeTraceGenerationRequestDTO> requests) {
        List<TraceAppEntity> generatedLinks = new ArrayList<>();

        for (ArtifactTypeTraceGenerationRequestDTO request : requests) {
            String sourceArtifactType = request.getSource();
            String targetArtifactType = request.getTarget();

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
                request.getMethod()));
        }
        return generatedLinks;
    }

    public List<TraceAppEntity> generateLinksWithMethod(List<ArtifactAppEntity> sourceArtifacts,
                                                        List<ArtifactAppEntity> targetArtifacts,
                                                        BaseGenerationModels baseGenerationModels) {
        ITraceLinkGeneration generationMethod = buildGenerationMethod(baseGenerationModels);
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

    public ITraceLinkGeneration buildGenerationMethod(BaseGenerationModels baseGenerationModel) {
        switch (baseGenerationModel) {
            case VSM:
                return new VSMController();
            case PLBert:
                return new PLBert(safaRequestBuilder);
            case NLBert:
                return new NLBert(safaRequestBuilder);
            default:
                throw new NotImplementedException("Trace method not implemented:" + baseGenerationModel);
        }
    }
}
