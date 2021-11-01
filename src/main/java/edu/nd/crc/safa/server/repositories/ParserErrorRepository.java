package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.ApplicationActivity;
import edu.nd.crc.safa.server.entities.db.ParserError;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ParserErrorRepository extends CrudRepository<ParserError, UUID> {

    List<ParserError> findByProjectVersion(ProjectVersion projectVersion);

    List<ParserError> findByProjectVersionAndApplicationActivity(ProjectVersion projectVersion,
                                                                 ApplicationActivity activity); //
    // TODO:
    // unit test
}
