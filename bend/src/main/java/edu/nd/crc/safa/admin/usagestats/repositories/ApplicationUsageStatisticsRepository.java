package edu.nd.crc.safa.admin.usagestats.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.admin.usagestats.entities.db.ApplicationUsageStatistics;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;

public interface ApplicationUsageStatisticsRepository extends CrudRepository<ApplicationUsageStatistics, UUID> {

    Optional<ApplicationUsageStatistics> findByUser(SafaUser user);
}
