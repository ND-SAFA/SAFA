package edu.nd.crc.safa.repositories.sql;

import java.util.UUID;

import edu.nd.crc.safa.entities.sql.Layout;
import edu.nd.crc.safa.entities.sql.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LayoutRepository extends CrudRepository<Layout, UUID> {

    Layout findByProjectAndTreeId(Project project, String treeId);
}
