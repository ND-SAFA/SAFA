package edu.nd.crc.safa.repositories.sql;

import java.util.UUID;

import edu.nd.crc.safa.entities.sql.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TIMFileRepository extends CrudRepository<ArtifactFile, UUID> {

}
