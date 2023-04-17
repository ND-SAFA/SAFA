package edu.nd.crc.safa.features.models.tgen.generator;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.models.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.models.tgen.entities.ArtifactLevelRequest;
import edu.nd.crc.safa.features.models.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.models.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.models.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.models.tgen.method.bert.BertMethodIdentifier;
import edu.nd.crc.safa.features.models.tgen.method.bert.TBert;
import edu.nd.crc.safa.features.models.tgen.method.vsm.VSMController;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
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

    private final Map<BaseGenerationModels, BertMethodIdentifier> bertModelIdentifiers = Map.of(
        BaseGenerationModels.AutomotiveBert, new BertMethodIdentifier("NL_BERT", "thearod5/automotive"),
        BaseGenerationModels.PLBert, new BertMethodIdentifier("PL_BERT", "thearod5/pl-bert"),
        BaseGenerationModels.NLBert, new BertMethodIdentifier("NL_BERT", "thearod5/nl-bert")
    );

    public static TracingPayload extractPayload(TracingRequest tracingRequest,
                                                ProjectAppEntity projectAppEntity) {
        List<ArtifactLevel> artifactLevels = new ArrayList<>();
        for (ArtifactLevelRequest artifactLevelRequest : tracingRequest.getArtifactLevels()) {
            List<ArtifactAppEntity> sources = projectAppEntity.getByArtifactType(artifactLevelRequest.getSource());
            List<ArtifactAppEntity> targets = projectAppEntity.getByArtifactType(artifactLevelRequest.getTarget());
            ArtifactLevel artifactLevel = new ArtifactLevel(sources, targets);
            artifactLevels.add(artifactLevel);
        }
        return new TracingPayload(
            tracingRequest.getMethod(),
            tracingRequest.getModel(),
            artifactLevels
        );
    }

    public List<TraceAppEntity> generateTraceLinks(TraceGenerationRequest traceGenerationRequest,
                                                   ProjectAppEntity projectAppEntity) {
        List<TraceAppEntity> generatedTraces = new ArrayList<>();
        for (TracingRequest tracingRequest : traceGenerationRequest.getRequests()) {
            TracingPayload tracingPayload = extractPayload(tracingRequest, projectAppEntity);
            generatedTraces.addAll(generateLinksWithMethod(tracingPayload));
        }
        return generatedTraces;
    }

    public List<TraceAppEntity> generateLinksWithMethod(TracingPayload tracingPayload) {
        ITraceLinkGeneration generationMethod = buildGenerationMethod(tracingPayload.getMethod());
        return new ArrayList<>(generationMethod.generateLinksWithBaselineState(tracingPayload));
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

    public TBert getBertModel(BaseGenerationModels generationModel, SafaRequestBuilder safaRequestBuilder) {
        BertMethodIdentifier methodIdentifier = bertModelIdentifiers.get(generationModel);
        if (methodIdentifier == null) {
            throw new NotImplementedException("Trace method not implemented:" + generationModel);
        }
        return new TBert(safaRequestBuilder, methodIdentifier);
    }

    private ITraceLinkGeneration buildGenerationMethod(BaseGenerationModels baseGenerationModels) {
        switch (baseGenerationModels) {
            case VSM:
                return new VSMController();
            case PLBert:
            case NLBert:
            case AutomotiveBert:
                return getBertModel(baseGenerationModels, safaRequestBuilder);
            default:
                throw new NotImplementedException("Trace method not implemented:" + baseGenerationModels);
        }
    }
}
