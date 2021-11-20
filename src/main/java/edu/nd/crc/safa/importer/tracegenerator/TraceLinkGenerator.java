package edu.nd.crc.safa.importer.tracegenerator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.importer.tracegenerator.vsm.Controller;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;
import edu.nd.crc.safa.server.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.services.TraceLinkService;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for generating trace links for given projects.
 */
@Component
public class TraceLinkGenerator {

    private final TraceLinkService traceLinkService;
    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    public TraceLinkGenerator(TraceLinkService traceLinkService,
                              TraceLinkRepository traceLinkRepository,
                              ArtifactBodyRepository artifactBodyRepository) {
        this.traceLinkService = traceLinkService;
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
    }

    public List<TraceLink> generateTraceLinksToFile(ProjectVersion projectVersion,
                                                    Pair<ArtifactType, ArtifactType> artifactTypes) {
        List<TraceLink> generatedLinks = generateLinksBetweenTypes(projectVersion, artifactTypes);
        return generatedLinks
            .stream()
            .filter(t -> {
                Optional<TraceLink> alreadyApprovedLink = traceLinkService.queryForLinkBetween(
                    t.getSourceArtifact(),
                    t.getTargetArtifact());
                return !alreadyApprovedLink.isPresent();
            })
            .collect(Collectors.toList());
    }

    public List<TraceLink> generateLinksBetweenTypes(ProjectVersion projectVersion,
                                                     Pair<ArtifactType, ArtifactType> artifactTypes) {
        Map<Artifact, Collection<String>> sTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue0());
        Map<Artifact, Collection<String>> tTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue1());

        return generateLinksFromTokens(sTokens, tTokens, TraceLink::new);
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
                double score = vsm.getRelevance(sTokens.get(sourceKey), tTokens.get(targetKey));
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    Link value = traceLinkConstructor.createTracelink(sourceKey, targetKey, score);
                    generatedLinks.add(value);
                }
            }
        }
        return generatedLinks;
    }

    private Map<Artifact, Collection<String>> tokenizeArtifactOfType(ProjectVersion projectVersion,
                                                                     ArtifactType artifactType) {
        List<ArtifactBody> sourceArtifactBodies = this.artifactBodyRepository
            .findByProjectVersionAndArtifactType(projectVersion, artifactType);
        return tokenizeArtifacts(sourceArtifactBodies);
    }

    private Map<Artifact, Collection<String>> tokenizeArtifacts(List<ArtifactBody> artifacts) {
        Map<Artifact, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactBody artifactBody : artifacts) {
            Artifact artifact = artifactBody.getArtifact();
            artifactTokens.put(artifact, getWordsInArtifactBody(artifactBody));
        }
        return artifactTokens;
    }

    public Map<String, Collection<String>> tokenizeArtifactAppEntities(List<ArtifactAppEntity> artifacts) {
        Map<String, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            artifactTokens.put(artifact.getName(), getWordsInArtifactAppEntity(artifact));
        }
        return artifactTokens;
    }

    private List<String> getWordsInArtifactBody(ArtifactBody artifactBody) {
        String[] artifactWords = artifactBody.getContent().split(" ");
        return Arrays.asList(artifactWords);
    }

    private List<String> getWordsInArtifactAppEntity(ArtifactAppEntity artifact) {
        String[] artifactWords = artifact.getBody().split(" ");
        return Arrays.asList(artifactWords);
    }
}
