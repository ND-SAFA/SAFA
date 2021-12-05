package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for providing an interface to modify artifacts in a project by calculating
 * and storing their changes between the previous version.
 *
 * @author Alberto Rodriguez
 */
@Service
public class ArtifactVersionService {

    ArtifactRepository artifactRepository;
    ArtifactTypeRepository artifactTypeRepository;
    ArtifactVersionRepository artifactVersionRepository;
    ProjectVersionRepository projectVersionRepository;
    ParserErrorRepository parserErrorRepository;

    DeltaService deltaService;

    @Autowired
    public ArtifactVersionService(ArtifactRepository artifactRepository,
                                  ArtifactTypeRepository artifactTypeRepository,
                                  ArtifactVersionRepository artifactVersionRepository,
                                  ProjectVersionRepository projectVersionRepository,
                                  ParserErrorRepository parserErrorRepository,
                                  DeltaService deltaService) {
        this.artifactRepository = artifactRepository;
        this.artifactTypeRepository = artifactTypeRepository;
        this.artifactVersionRepository = artifactVersionRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.parserErrorRepository = parserErrorRepository;
        this.deltaService = deltaService;
    }

    /**
     * Calculates the changes in each artifact body from the previous versions and stores
     * changes at given ProjectVersion.
     *
     * @param projectVersion   The ProjectVersion associated with calculated artifact changes.
     * @param projectArtifacts List of artifact's in a project whose version will be stored.
     * @throws SafaError Throws error if any database related errors arise during saving the new artifacts/
     */
    public void setArtifactsAtVersion(ProjectVersion projectVersion,
                                      List<ArtifactAppEntity> projectArtifacts) throws SafaError {
        List<ParserError> parserErrors = this.artifactVersionRepository
            .setAppEntitiesAtProjectVersion(projectVersion, projectArtifacts);
        for (ParserError parserError : parserErrors) {
            parserError.setApplicationActivity(ProjectParsingActivities.PARSING_ARTIFACTS);
            this.parserErrorRepository.save(parserError);
        }
    }

    /**
     * Deletes artifact with given name within given project.
     *
     * @param projectVersion The version to record the deletion happening in.
     * @param artifactName   The name of the artifact to be deleted.
     * @return ServerResponse with success message.
     */
    public ServerResponse deleteArtifactBody(
        ProjectVersion projectVersion,
        String artifactName) {
        Optional<ArtifactVersion> bodyToRemove = this.artifactVersionRepository.findByProjectVersionAndArtifactName(projectVersion,
            artifactName);
        bodyToRemove.ifPresentOrElse(artifactBody -> {
            artifactBody.setModificationType(ModificationType.REMOVED);
            artifactBody.setSummary("");
            artifactBody.setContent("");
            this.artifactVersionRepository.save(artifactBody);
        }, () -> {
            Project project = projectVersion.getProject();
            Optional<Artifact> artifactQuery = this.artifactRepository.findByProjectAndName(project, artifactName);
            artifactQuery.ifPresent((artifact -> {
                ArtifactVersion artifactVersion = new ArtifactVersion(
                    projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "", "");
                this.artifactVersionRepository.save(artifactVersion);
            }));
        });
        return new ServerResponse(String.format("%s successfully deleted.", artifactName));
    }
}
