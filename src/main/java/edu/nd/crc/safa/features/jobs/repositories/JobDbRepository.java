package edu.nd.crc.safa.features.jobs.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JobDbRepository extends CrudRepository<JobDbEntity, UUID> {

    List<JobDbEntity> findByUserOrderByLastUpdatedAtDesc(SafaUser user);

    List<JobDbEntity> findByProjectProjectIdInOrderByLastUpdatedAtDesc(List<UUID> completedEntityIds);
}
