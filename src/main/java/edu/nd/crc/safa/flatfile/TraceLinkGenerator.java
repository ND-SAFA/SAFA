package edu.nd.crc.safa.flatfile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.constants.ProjectPaths;
import edu.nd.crc.safa.database.entities.Artifact;
import edu.nd.crc.safa.database.entities.ArtifactBody;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;
import edu.nd.crc.safa.database.entities.ProjectVersion;
import edu.nd.crc.safa.database.entities.TraceLink;
import edu.nd.crc.safa.database.repositories.ArtifactBodyRepository;
import edu.nd.crc.safa.database.repositories.ArtifactRepository;
import edu.nd.crc.safa.database.repositories.TraceLinkRepository;
import edu.nd.crc.safa.server.error.ServerError;
import edu.nd.crc.safa.vsm.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for generating trace links for given projects.
 */
@Component
public class TraceLinkGenerator {

    private TraceLinkRepository traceLinkRepository;
    private ArtifactBodyRepository artifactBodyRepository;
    private ArtifactRepository artifactRepository;

    @Autowired
    public TraceLinkGenerator(TraceLinkRepository traceLinkRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ArtifactRepository artifactRepository) {
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.artifactRepository = artifactRepository;
    }

    public void generateTraceLink(Project project,
                                  ProjectVersion projectVersion,
                                  ArtifactType sourceType,
                                  ArtifactType targetType,
                                  String outputFileName) throws ServerError {
        List<ArtifactBody> sourceArtifacts = this.artifactBodyRepository
            .findByProjectAndProjectVersionAndArtifactType(project, projectVersion, sourceType);
        List<ArtifactBody> targetArtifacts = this.artifactBodyRepository
            .findByProjectAndProjectVersionAndArtifactType(project, projectVersion, targetType);

        Map<String, Collection<String>> sTokens = splitArtifactsIntoWords(sourceArtifacts);
        Map<String, Collection<String>> tTokens = splitArtifactsIntoWords(targetArtifacts);

        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());
        List<String> lines = new ArrayList<>();
        String GENERATED_FILES_HEADER = "Source,Target,Score";
        lines.add(GENERATED_FILES_HEADER);
        for (String sid : sTokens.keySet()) {
            for (String tid : tTokens.keySet()) {
                Artifact sourceArtifact = this.artifactRepository.findByProjectAndArtifactTypeAndName(project,
                    sourceType, sid);
                Artifact targetArtifact = this.artifactRepository.findByProjectAndArtifactTypeAndName(project,
                    sourceType, tid);
                double score = vsm.getRelevance(sTokens.get(sid), tTokens.get(tid));
                TraceLink generatedLink = new TraceLink(sourceArtifact, targetArtifact);
                generatedLink.setIsGenerated(score);
                this.traceLinkRepository.save(generatedLink); // TODO : add check for save error
                lines.add(String.format("%s,%s,%s", sid, tid, score));
            }
        }

        try {
            String pathToOutputFile = ProjectPaths.getPathToGeneratedFile(project, outputFileName);
            Files.write(Paths.get(pathToOutputFile), lines);
        } catch (IOException e) {
            throw new ServerError("error writing trace matrix file", e);
        }
    }

    private Map<String, Collection<String>> splitArtifactsIntoWords(List<ArtifactBody> artifacts) {
        Map<String, Collection<String>> artifactTokens = new HashMap<>();
        for (ArtifactBody artifact : artifacts) {
            String artifactName = artifact.getName();
            artifactTokens.put(artifactName, getArtifactWords(artifact));
        }
        return artifactTokens;
    }

    private List<String> getArtifactWords(ArtifactBody artifactBody) {
        String[] artifactWords = artifactBody.getContent().split(" ");
        return Arrays.asList(artifactWords);
    }
}
