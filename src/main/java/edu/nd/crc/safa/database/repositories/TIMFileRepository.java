package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.database.entities.TIMFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TIMFileRepository extends CrudRepository<TIMFile, UUID> {

    List<TIMFileRepository> findByProjectId(UUID projectId);

}
