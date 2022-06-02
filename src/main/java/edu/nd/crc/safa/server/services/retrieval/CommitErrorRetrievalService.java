package edu.nd.crc.safa.server.services.retrieval;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.ProjectParsingErrors;
import edu.nd.crc.safa.server.entities.app.ErrorApplicationEntity;
import edu.nd.crc.safa.server.entities.db.ProjectEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.CommitErrorRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for collecting all parsing errors in a project version.
 */
@Service
public class CommitErrorRetrievalService {
    private final CommitErrorRepository commitErrorRepository;

    @Autowired
    public CommitErrorRetrievalService(CommitErrorRepository commitErrorRepository) {
        this.commitErrorRepository = commitErrorRepository;
    }

    /**
     * Retrieves, collections, and separates errors generated during given project version.
     *
     * @param projectVersion The ProjectVersion which returned errors are associated with.
     * @return Separated errors by ApplicationActivity.
     */
    public ProjectParsingErrors collectErrorsInVersion(ProjectVersion projectVersion) {

        List<ErrorApplicationEntity> timErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntity.TIM)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> artifactErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntity.ARTIFACTS)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> traceErrors = this.commitErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ProjectEntity.TRACES)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());

        return new ProjectParsingErrors(timErrors, artifactErrors, traceErrors);
    }
}
