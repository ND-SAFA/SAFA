package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.accounts.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JobDbRepository extends CrudRepository<JobDbEntity, UUID> {

    List<JobDbEntity> findByUserOrderByLastUpdatedAtDesc(SafaUser user);
}
