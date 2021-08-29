package edu.nd.crc.safa.services;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.entities.application.ErrorApplicationEntity;
import edu.nd.crc.safa.entities.database.ApplicationActivity;
import edu.nd.crc.safa.entities.database.ProjectVersion;
import edu.nd.crc.safa.repositories.ParserErrorRepository;
import edu.nd.crc.safa.responses.ProjectErrors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ParserErrorService {
    ParserErrorRepository parserErrorRepository;

    @Autowired
    public ParserErrorService(ParserErrorRepository parserErrorRepository) {
        this.parserErrorRepository = parserErrorRepository;
    }

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
            .findByProjectVersionAndApplicationActivity(projectVersion, ApplicationActivity.PARSING_TRACE_MATRIX)
            .stream()
            .map(ErrorApplicationEntity::new)
            .collect(Collectors.toList());
        return new ProjectErrors(timErrors, artifactErrors, traceErrors);
    }
}
