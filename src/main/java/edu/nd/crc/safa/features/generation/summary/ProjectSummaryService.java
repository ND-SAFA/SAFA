package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ProjectSummaryService {
    private final GenApi genApi;
    private final ProjectRepository projectRepository;
    private final CommitService commitService;
    private final SafaUserService safaUserService;
    private final SummaryService summaryService;

    /**
     * Summarizes project and saves summary to project. If any artifacts were summarized, those are saved to.
     *
     * @param user           The user saving the project summary and artifact summaries.
     * @param projectVersion The project to store summary under.
     * @param artifacts      The artifacts of the project to summarize.
     * @param logger         Optional. Job logger to store logs under.
     * @return Project summary and artifacts with summaries included.
     */
    public Pair<String, List<ArtifactAppEntity>> summarizeProjectEntities(SafaUser user,
                                                                          ProjectVersion projectVersion,
                                                                          List<ArtifactAppEntity> artifacts,
                                                                          JobLogger logger) {
        Project project = projectVersion.getProject();
        String projectSummary = project.getSpecification();
        boolean hasProjectSummary = projectSummary != null && !projectSummary.isEmpty();
        boolean hasCodeSummaries = hasCodeSummaries(artifacts);

        SummaryResponse summarizationResponse = this.summarizeProject(artifacts, logger);

        // Save project summary
        projectSummary = summarizationResponse.getSummary();
        saveProjectSummary(project, projectSummary, logger);

        // Save artifact summaries
        saveArtifactSummaries(user, projectVersion, artifacts, summarizationResponse, logger);
        return new Pair<>(projectSummary, artifacts);
    }

    /**
     * Creates project summary.
     *
     * @param artifacts The artifacts in the project.
     * @param jobLogger Optional. Job logger to store logs under.
     * @return The project summary.
     */
    public SummaryResponse summarizeProject(List<ArtifactAppEntity> artifacts,
                                            JobLogger jobLogger) {
        artifacts = artifacts.stream().filter(a -> a.getTraceString().length() > 0).collect(Collectors.toList());
        List<GenerationArtifact> generationArtifacts = artifacts
            .stream()
            .map(GenerationArtifact::new)
            .collect(Collectors.toList());
        SummaryRequest request = new SummaryRequest(generationArtifacts);
        return this.genApi.generateProjectSummary(request, jobLogger);
    }

    public boolean hasCodeSummaries(List<ArtifactAppEntity> codeArtifacts) {
        for (ArtifactAppEntity artifact : codeArtifacts) {
            if (artifact.isCode() && artifact.getSummary().isEmpty()) {
                return false;
            }
        }
        return true;
    }

    private void saveArtifactSummaries(SafaUser user,
                                       ProjectVersion projectVersion,
                                       List<ArtifactAppEntity> artifacts,
                                       SummaryResponse summarizationResponse,
                                       JobLogger logger) {
        Map<String, ArtifactAppEntity> artifactMap = ProjectDataStructures.createArtifactNameMap(artifacts);
        List<GenerationArtifact> summarizedArtifacts = summarizationResponse.getArtifacts();
        boolean hasSummaries = summarizedArtifacts != null && !summarizedArtifacts.isEmpty();
        int nSummaries = hasSummaries ? summarizedArtifacts.size() : 0;
        if (hasSummaries) {
            for (GenerationArtifact summarizedArtifact : summarizedArtifacts) {
                String summary = summarizedArtifact.getSummary();
                if (summary == null || summary.isBlank()) {
                    logger.log("Artifact " + summarizedArtifact.getId() + " came back without summary.");
                    continue;
                }
                ArtifactAppEntity artifact = artifactMap.get(summarizedArtifact.getId());
                artifact.setSummary(summary);
            }
            commitService.saveArtifacts(user, projectVersion, artifacts, ModificationType.MODIFIED);

        }
        logger.log(String.format("Saved  %s artifact summaries.", nSummaries));
    }

    private void saveProjectSummary(Project project, String projectSummary, JobLogger logger) {
        project.setSpecification(projectSummary);
        this.projectRepository.save(project);
        logger.log("Project summary (%s) was saved.", projectSummary.length());
    }
}
