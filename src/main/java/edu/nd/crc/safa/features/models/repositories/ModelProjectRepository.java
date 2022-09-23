package edu.nd.crc.safa.features.models.repositories;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.models.entities.ModelProject;

import org.springframework.data.repository.CrudRepository;

public interface ModelProjectRepository extends CrudRepository<ModelProject, UUID> {

    List<ModelProject> findByModel(Model model);

    default List<ModelProject> getAllModels() {
        ArrayList<ModelProject> models = new ArrayList<>();
        findAll().forEach(models::add);
        return models;
    }
}
