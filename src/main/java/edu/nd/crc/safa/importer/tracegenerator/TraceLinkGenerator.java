package edu.nd.crc.safa.importer.tracegenerator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.tracegenerator.vsm.Controller;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceApproval;
import edu.nd.crc.safa.server.repositories.artifacts.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.traces.TraceLinkVersionRepository;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for generating trace links for given projects.
 */
@Component
public class TraceLinkGenerator {

    private final ArtifactVersionRepository artifactVersionRepository;
    private final TraceLinkVersionRepository traceLinkVersionRepository;
    private final ProjectRetrievalService projectRetrievalService;

    @Autowired
    public TraceLinkGenerator(TraceLinkVersionRepository traceLinkVersionRepository,
                              ArtifactVersionRepository artifactVersionRepository,
                              ProjectRetrievalService projectRetrievalService) {
        this.artifactVersionRepository = artifactVersionRepository;
        this.traceLinkVersionRepository = traceLinkVersionRepository;
        this.projectRetrievalService = projectRetrievalService;
    }

    public List<TraceAppEntity> generateTraceLinksToFile(ProjectVersion projectVersion,
                                                         Pair<ArtifactType, ArtifactType> artifactTypes) {
        String DELIMITER = "*";
        List<TraceAppEntity> generatedLinks = generateLinksBetweenTypes(projectVersion, artifactTypes);
        List<String> approvedLinks = projectRetrievalService
            .getTracesInProjectVersion(projectVersion)
            .stream()
            .filter(link -> link.approvalStatus.equals(TraceApproval.APPROVED))
            .map(link -> link.sourceName + DELIMITER + link.targetName)
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.sourceName + DELIMITER + t.targetName;
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }

    public List<TraceAppEntity> generateLinksBetweenTypes(ProjectVersion projectVersion,
                                                          Pair<ArtifactType, ArtifactType> artifactTypes) {
        List<ArtifactVersion> artifactsInVersion =
            this.artifactVersionRepository.getVersionEntitiesByProjectVersion(projectVersion);
        Map<Artifact, Collection<String>> sTokens = tokenizeArtifactOfType(artifactsInVersion,
            artifactTypes.getValue0());
        Map<Artifact, Collection<String>> tTokens = tokenizeArtifactOfType(artifactsInVersion,
            artifactTypes.getValue1());
        TraceLinkConstructor<Artifact, TraceAppEntity> traceLinkConstructor = (s, t, score) ->
            new TraceAppEntity(s.getName(), t.getName(), score);

        return generateLinksFromTokens(sTokens, tTokens, traceLinkConstructor);
    }

    public List<TraceAppEntity> generateLinksBetweenArtifactAppEntities(List<ArtifactAppEntity> sourceDocs,
                                                                        List<ArtifactAppEntity> targetDocs) {
        Map<String, Collection<String>> sourceTokens = tokenizeArtifactAppEntities(sourceDocs);
        Map<String, Collection<String>> targetTokens = tokenizeArtifactAppEntities(targetDocs);
        return generateLinksFromTokens(sourceTokens, targetTokens, TraceAppEntity::new);
    }

    private <Key, Link> List<Link> generateLinksFromTokens(Map<Key, Collection<String>> sTokens,
                                                           Map<Key, Collection<String>> tTokens,
                                                           TraceLinkConstructor<Key, Link> traceLinkConstructor) {
        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());

        List<Link> generatedLinks = new ArrayList<>();
        for (Key sourceKey : sTokens.keySet()) {
            for (Key targetKey : tTokens.keySet()) {
                double score = vsm.getSimilarityScore(sTokens.get(sourceKey), tTokens.get(targetKey));
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    Link value = traceLinkConstructor.createTraceLink(sourceKey, targetKey, score);
                    generatedLinks.add(value);
                }
            }
        }
        return generatedLinks;
    }

    private Map<Artifact, Collection<String>> tokenizeArtifactOfType(List<ArtifactVersion> artifacts,
                                                                     ArtifactType artifactType) {
        List<ArtifactVersion> artifactsWithType =
            artifacts
                .stream()
                .filter(a -> a.getArtifact().getType().equals(artifactType))
                .collect(Collectors.toList());
        return tokenizeArtifacts(artifactsWithType);
    }

    private Map<Artifact, Collection<String>> tokenizeArtifacts(List<ArtifactVersion> artifacts) {
        Map<Artifact, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactVersion artifactVersion : artifacts) {
            Artifact artifact = artifactVersion.getArtifact();
            artifactTokens.put(artifact, getWordsInArtifactBody(artifactVersion));
        }
        return artifactTokens;
    }

    public Map<String, Collection<String>> tokenizeArtifactAppEntities(List<ArtifactAppEntity> artifacts) {
        Map<String, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            artifactTokens.put(artifact.name, getWordsInArtifactAppEntity(artifact));
        }
        return artifactTokens;
    }

    private List<String> getWordsInArtifactBody(ArtifactVersion artifactVersion) {
        String[] artifactWords = artifactVersion.getContent().split(" ");
        return Arrays.asList(artifactWords);
    }

    private List<String> getWordsInArtifactAppEntity(ArtifactAppEntity artifact) {
        String[] artifactWords = artifact.getBody().split(" ");
        return Arrays.asList(artifactWords);
    }
}
