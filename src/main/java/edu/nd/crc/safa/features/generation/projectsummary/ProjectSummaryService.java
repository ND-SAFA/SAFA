package edu.nd.crc.safa.features.generation.projectsummary;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.generation.GenerationApi;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ProjectSummaryService {
    SafaRequestBuilder safaRequestBuilder;
    ProjectRepository projectRepository;

    /**
     * Summarizes project and saves summary to project.
     *
     * @param project   The project to store summary under.
     * @param artifacts The artifacts of the project to summarize.
     * @param logger    Optional. Job logger to store logs under.
     */
    public void generateProjectSummary(Project project, List<ArtifactAppEntity> artifacts, JobLogger logger) {
        if (project.getSpecification() != null) {
            if (logger != null) {
                logger.log("Loading previous project specification.");
            }
            return;
        }
        String projectSummary = this.summarizeProject(artifacts, logger);
        if (project.getDescription().isEmpty()) {
            project.setDescription(projectSummary);
        }
        project.setSpecification(projectSummary);
        projectRepository.save(project);
    }

    /**
     * Creates project summary.
     *
     * @param artifacts The artifacts in the project.
     * @param jobLogger Optional. Job logger to store logs under.
     * @return The project summary.
     */
    public String summarizeProject(List<ArtifactAppEntity> artifacts, JobLogger jobLogger) {
        Map<String, String> projectArtifactMap = ProjectDataStructures.createArtifactLayer(artifacts);
        GenerationApi api = new GenerationApi(this.safaRequestBuilder);
        ProjectSummaryRequest request = new ProjectSummaryRequest(projectArtifactMap);
        return api.generateProjectSummary(request, jobLogger);
    }
}
