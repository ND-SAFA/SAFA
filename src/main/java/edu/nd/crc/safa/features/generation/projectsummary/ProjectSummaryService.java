package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.summary.SummaryService;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.json.JSONObject;
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
     * @param projectVersion The project to store summary under.
     * @param artifacts      The artifacts of the project to summarize.
     * @param logger         Optional. Job logger to store logs under.
     * @return Project summary and artifacts with summaries included.
     */
    public Pair<String, List<ArtifactAppEntity>> summarizeProjectEntities(ProjectVersion projectVersion,
                                                                          List<ArtifactAppEntity> artifacts,
                                                                          JobLogger logger) {
        Project project = projectVersion.getProject();
        String projectSummary = project.getSpecification();
        boolean hasProjectSummary = projectSummary != null && !projectSummary.isEmpty();
        boolean hasCodeSummaries = hasCodeSummaries(artifacts);

        if (hasProjectSummary) {
            if (!hasCodeSummaries) {
                summaryService.addSummariesToCode(artifacts, projectSummary, logger);
            }
        } else {
            JSONObject kwargs = new JSONObject();
            kwargs.put("do_resummarize_project", !hasCodeSummaries);
            kwargs.put("summarize_artifacts", !hasCodeSummaries);
            ProjectSummaryResponse summarizationResponse = this.summarizeProject(artifacts, kwargs, logger);

            // Save project summary
            projectSummary = summarizationResponse.getSummary();
            saveProjectSummary(project, projectSummary);

            // Save artifact summaries
            saveArtifactSummaries(projectVersion, artifacts, summarizationResponse);
        }
        return new Pair<>(projectSummary, artifacts);
    }

    /**
     * Creates project summary.
     *
     * @param artifacts The artifacts in the project.
     * @param jobLogger Optional. Job logger to store logs under.
     * @return The project summary.
     */
    public ProjectSummaryResponse summarizeProject(List<ArtifactAppEntity> artifacts,
                                                   JSONObject kwargs,
                                                   JobLogger jobLogger) {
        artifacts = artifacts.stream().filter(a -> a.getTraceString().length() > 0).collect(Collectors.toList());
        ProjectSummaryRequest request = new ProjectSummaryRequest(artifacts.stream().map(GenerationArtifact::new)
            .collect(Collectors.toList()), kwargs);
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

    private void saveArtifactSummaries(ProjectVersion projectVersion,
                                       List<ArtifactAppEntity> artifacts,
                                       ProjectSummaryResponse summarizationResponse) {
        Map<String, ArtifactAppEntity> artifactMap = ProjectDataStructures.createArtifactNameMap(artifacts);
        List<GenerationArtifact> summarizedArtifacts = summarizationResponse.getArtifacts();
        if (summarizedArtifacts != null && !summarizedArtifacts.isEmpty()) {
            for (GenerationArtifact summarizedArtifact : summarizedArtifacts) {
                ArtifactAppEntity artifact = artifactMap.get(summarizedArtifact.getId());
                artifact.setSummary(summarizedArtifact.getSummary());
            }
            commitService.saveArtifacts(projectVersion, artifacts, ModificationType.MODIFIED);
        }
    }

    private void saveProjectSummary(Project project, String projectSummary) {
        if (project.getDescription().isEmpty()) {
            project.setDescription(projectSummary);
        }
        project.setSpecification(projectSummary);
        this.projectRepository.save(project);
    }
}
