package edu.nd.crc.safa.importer.tracegenerator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.common.ProjectVariables;
import edu.nd.crc.safa.importer.tracegenerator.vsm.Controller;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.TraceAppEntity;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for generating trace links for given projects.
 */
@Component
public class TraceLinkGenerator {

    @Autowired
    public TraceLinkGenerator() {
    }

    public List<TraceAppEntity> generateLinksBetweenArtifactAppEntities(List<ArtifactAppEntity> sourceDocs,
                                                                        List<ArtifactAppEntity> targetDocs) {
        Map<String, Collection<String>> sourceTokens = tokenizeArtifactAppEntities(sourceDocs);
        Map<String, Collection<String>> targetTokens = tokenizeArtifactAppEntities(targetDocs);
        TraceLinkConstructor<String, TraceAppEntity> traceLinkConstructor = (s, t, score) -> new TraceAppEntity()
            .asGeneratedTrace(score)
            .betweenArtifacts(s, t);
        return generateLinksFromTokens(sourceTokens, targetTokens, traceLinkConstructor);
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
