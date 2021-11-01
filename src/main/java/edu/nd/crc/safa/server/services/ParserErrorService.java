package edu.nd.crc.safa.server.services;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.app.ErrorApplicationEntity;
import edu.nd.crc.safa.server.entities.db.ApplicationActivity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ParserErrorRepository;
import edu.nd.crc.safa.server.messages.ProjectErrors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ParserErrorService {
    ParserErrorRepository parserErrorRepository;

    @Autowired
    public ParserErrorService(ParserErrorRepository parserErrorRepository) {
        this.parserErrorRepository = parserErrorRepository;
    }

    /**
     * Retrieves, collections, and separates errors generated during given project version.
     *
     * @param projectVersion The ProjectVersion which returned errors are associated with.
     * @return Separated errors by ApplicationActivity.
     */
    public ProjectErrors collectionProjectErrors(ProjectVersion projectVersion) {

        List<ErrorApplicationEntity> timErrors = this.parserErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ApplicationActivity.PARSING_TIM)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> artifactErrors = this.parserErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ApplicationActivity.PARSING_ARTIFACTS)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        List<ErrorApplicationEntity> traceErrors = this.parserErrorRepository
            .findByProjectVersionAndApplicationActivity(projectVersion, ApplicationActivity.PARSING_TRACES)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        return new ProjectErrors(timErrors, artifactErrors, traceErrors);
    }
}
