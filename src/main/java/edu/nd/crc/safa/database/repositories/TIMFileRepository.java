package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.database.entities.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TIMFileRepository extends CrudRepository<ArtifactFile, UUID> {

    List<TIMFileRepository> findByProjectId(UUID projectId);

}
