package edu.nd.crc.safa.features.errors.services;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.errors.entities.app.ErrorApplicationEntity;
import edu.nd.crc.safa.features.errors.repositories.CommitErrorRepository;
import edu.nd.crc.safa.features.projects.entities.app.ProjectParsingErrors;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for collecting all parsing errors in a project version.
 */
@Service
@AllArgsConstructor
public class CommitErrorRetrievalService {
    private final CommitErrorRepository commitErrorRepository;

    /**
     * Retrieves, collections, and separates errors generated during given project version.
     *
     * @param projectVersion The ProjectVersion which returned errors are associated with.
     * @return Separated errors by ApplicationActivity.
     */
    public ProjectParsingErrors collectErrorsInVersion(ProjectVersion projectVersion) {

        List<ErrorApplicationEntity> timErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntityType.TIM)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> artifactErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntityType.ARTIFACTS)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> traceErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntityType.TRACES)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());

        return new ProjectParsingErrors(timErrors, artifactErrors, traceErrors);
    }
}
