package edu.nd.crc.safa.database.repositories;

import java.util.UUID;

import edu.nd.crc.safa.database.entities.Layout;
import edu.nd.crc.safa.database.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LayoutRepository extends CrudRepository<Layout, UUID> {

    Layout findByProjectAndHash(Project project, String hash);
}
