package edu.nd.crc.safa.importer.flatfiles;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.db.entities.sql.TraceLink;
import edu.nd.crc.safa.db.repositories.sql.ArtifactBodyRepository;
import edu.nd.crc.safa.db.repositories.sql.ArtifactRepository;
import edu.nd.crc.safa.db.repositories.sql.TraceLinkRepository;
import edu.nd.crc.safa.server.responses.ServerError;
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
    private final ArtifactRepository artifactRepository;

    @Autowired
    public TraceLinkGenerator(TraceLinkRepository traceLinkRepository,
                              ArtifactBodyRepository artifactBodyRepository,
                              ArtifactRepository artifactRepository) {
        this.traceLinkRepository = traceLinkRepository;
        this.artifactBodyRepository = artifactBodyRepository;
        this.artifactRepository = artifactRepository;
    }

    public void generateTraceLinksToFile(ProjectVersion projectVersion,
                                         Pair<ArtifactType, ArtifactType> artifactTypes,
                                         String outputFileName) throws ServerError {
        Project project = projectVersion.getProject();
        List<TraceLink> generatedLinks = generateLinksBetweenTypes(projectVersion, artifactTypes);
        this.traceLinkRepository.saveAll(generatedLinks);

        try {
            String pathToOutputFile = ProjectPaths.getPathToGeneratedFile(project, outputFileName);
            writeLinksToFile(generatedLinks, pathToOutputFile);
        } catch (IOException e) {
            throw new ServerError("error writing trace matrix file", e);
        }
    }

    public List<TraceLink> generateLinksBetweenTypes(ProjectVersion projectVersion,
                                                     Pair<ArtifactType, ArtifactType> artifactTypes)
        throws ServerError {

        Map<Artifact, Collection<String>> sTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue0());
        Map<Artifact, Collection<String>> tTokens = tokenizeArtifactOfType(projectVersion,
            artifactTypes.getValue1());

        return generateLinksFromTokens(sTokens, tTokens);
    }

    private List<TraceLink> generateLinksFromTokens(Map<Artifact, Collection<String>> sTokens,
                                                    Map<Artifact, Collection<String>> tTokens) throws ServerError {
        Controller vsm = new Controller();
        vsm.buildIndex(tTokens.values());

        List<TraceLink> generatedLinks = new ArrayList<>();
        for (Artifact sourceArtifact : sTokens.keySet()) {
            for (Artifact targetArtifact : tTokens.keySet()) {
                double score = vsm.getRelevance(sTokens.get(sourceArtifact), tTokens.get(targetArtifact));
                if (score > ProjectVariables.TRACE_THRESHOLD) {
                    TraceLink generatedLink = new TraceLink(sourceArtifact, targetArtifact);
                    generatedLink.setIsGenerated(score);
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

    private void writeLinksToFile(List<TraceLink> generatedLinks,
                                  String pathToOutputFile) throws IOException {
        List<String> lines = new ArrayList<>();
        String GENERATED_FILES_HEADER = "Source,Target,Score";
        lines.add(GENERATED_FILES_HEADER);
        for (TraceLink generatedLink : generatedLinks) {
            lines.add(String.format("%s,%s,%s",
                generatedLink.getSourceName(),
                generatedLink.getTargetName(),
                generatedLink.getScore()));
        }
        Files.write(Paths.get(pathToOutputFile), lines);
    }
}
