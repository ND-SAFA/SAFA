package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.CommitError;
import edu.nd.crc.safa.server.entities.db.ProjectParsingActivities;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CommitErrorRepository extends CrudRepository<CommitError, UUID> {

    List<CommitError> findByProjectVersion(ProjectVersion projectVersion);

    List<CommitError> findByProjectVersionAndApplicationActivity(ProjectVersion projectVersion,
                                                                 ProjectParsingActivities activity); //
    // TODO:
    // unit test
}
