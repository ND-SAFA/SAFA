package edu.nd.crc.safa.importer.flatfiles;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.server.db.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.server.db.repositories.TraceLinkRepository;
import edu.nd.crc.safa.vsm.Controller;

import org.javatuples.Pair;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for generating trace links for given projects.
 */
@Component
public class TraceLinkGenerator {

    private final TraceLinkRepository traceLinkRepository;
    private final ArtifactBodyRepository artifactBodyRepository;

    @Autowired
    public TraceLinkGenerator(TraceLinkRepository traceLinkRepository,
                              ArtifactBodyRepository artifactBodyRepository) {
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
    }

    public void generateTraceLinksToFile(ProjectVersion projectVersion,
                                         Pair<ArtifactType, ArtifactType> artifactTypes) {
        List<TraceLink> generatedLinks = generateLinksBetweenTypes(projectVersion, artifactTypes);
        for (TraceLink traceLink : generatedLinks) {
            Optional<TraceLink> alreadyApprovedLink = this.traceLinkRepository
                .getApprovedLinkIfExist(traceLink.getSourceArtifact(), traceLink.getTargetArtifact());
            if (!alreadyApprovedLink.isPresent()) {
                this.traceLinkRepository.save(traceLink);
            }
        }
    }

    public List<TraceLink> generateLinksBetweenTypes(ProjectVersion projectVersion,
                                                     Pair<ArtifactType, ArtifactType> artifactTypes) {
        Map<Artifact, Collection<String>> sTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue0());
        Map<Artifact, Collection<String>> tTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue1());

        return generateLinksFromTokens(sTokens, tTokens);
    }

    private List<TraceLink> generateLinksFromTokens(Map<Artifact, Collection<String>> sTokens,
                                                    Map<Artifact, Collection<String>> tTokens) {
        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());

        List<TraceLink> generatedLinks = new ArrayList<>();
        for (Artifact sourceArtifact : sTokens.keySet()) {
            for (Artifact targetArtifact : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sourceArtifact), tTokens.get(targetArtifact));
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    TraceLink generatedLink = new TraceLink(sourceArtifact, targetArtifact, score);
                    generatedLinks.add(generatedLink);
                }
            }
        }
        return generatedLinks;
    }

    private Map<Artifact, Collection<String>> tokenizeArtifactOfType(ProjectVersion projectVersion,
                                                                     ArtifactType artifactType) {
        List<ArtifactBody> sourceArtifactBodies = this.artifactBodyRepository
            .findByProjectVersionAndArtifactType(projectVersion, artifactType);
        return splitArtifactsIntoWords(sourceArtifactBodies);
    }

    private Map<Artifact, Collection<String>> splitArtifactsIntoWords(List<ArtifactBody> artifacts) {
        Map<Artifact, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactBody artifactBody : artifacts) {
            Artifact artifact = artifactBody.getArtifact();
            artifactTokens.put(artifact, getArtifactWords(artifactBody));
        }
        return artifactTokens;
    }

    private List<String> getArtifactWords(ArtifactBody artifactBody) {
        String[] artifactWords = artifactBody.getContent().split(" ");
        return Arrays.asList(artifactWords);
    }
}
