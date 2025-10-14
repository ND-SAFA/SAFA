package edu.nd.crc.safa.features.errors.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.context.annotation.Scope;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
@Scope("singleton")
public interface CommitErrorRepository extends CrudRepository<CommitError, UUID> {

    List<CommitError> findByProjectVersion(ProjectVersion projectVersion);

    List<CommitError> findByProjectVersionAndApplicationActivity(ProjectVersion projectVersion,
                                                                 ProjectEntityType activity);
}
