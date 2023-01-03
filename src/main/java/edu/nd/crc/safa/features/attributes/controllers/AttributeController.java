package edu.nd.crc.safa.features.attributes.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import javax.transaction.Transactional;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

//TODO send notifications

@RestController
public class AttributeController extends BaseController  {

    private final AttributeService attributeService;

    @Autowired
    public AttributeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                               AttributeService attributeService) {
        super(resourceBuilder, serviceProvider);
        this.attributeService = attributeService;
    }

    /**
     * Gets all attributes associated with a project.
     *
     * @param projectId The ID of the project.
     * @return A list of project attributes.
     * @throws SafaError If something goes wrong while retrieving the data.
     */
    @GetMapping(AppRoutes.Attribute.ROOT)
    public List<CustomAttributeAppEntity> getProjectAttributes(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return attributeService.getAttributeEntitiesForProject(project);
    }

    /**
     * Creates a new attribute associated with a project.
     *
     * @param projectId The ID of the project.
     * @param appEntity The front-end representation of the new attribute.
     * @return The created attribute.
     * @throws SafaError If something goes wrong while saving the data.
     */
    @PostMapping(AppRoutes.Attribute.ROOT)
    public CustomAttributeAppEntity createNewProjectAttribute(@PathVariable UUID projectId,
                                                              @RequestBody CustomAttributeAppEntity appEntity) {

        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        if (appEntity.getKey().isBlank()) {
            throw new SafaError("Attribute key cannot be blank");
        }

        attributeService.saveEntity(appEntity, project, true);

        return getProjectAttribute(projectId, appEntity.getKey());
    }

    /**
     * Gets an attribute with a given key name within the given project.
     *
     * @param projectId The ID of the project.
     * @param key The key name of the attribute to retrieve.
     * @return The attribute if it is found.
     * @throws SafaError If the attribute could not be retrieved.
     */
    @GetMapping(AppRoutes.Attribute.BY_KEY)
    public CustomAttributeAppEntity getProjectAttribute(@PathVariable UUID projectId, @PathVariable String key)
        throws SafaError {

        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();

        if (key.isBlank()) {
            throw new SafaError("Attribute key cannot be blank");
        }

        Optional<CustomAttribute> attr = attributeService.getByProjectAndKeyname(project, key);

        if (attr.isEmpty()) {
            throw new SafaError(String.format("No attribute named %s in project.", key));
        }

        return attributeService.appEntityFromCustomAttribute(attr.get());
    }

    /**
     * Edits a project attribute.
     *
     * @param projectId The ID of the project.
     * @param key The key name of the attribute to edit.
     * @param appEntity The new attribute definition.
     * @return The updated attribute
     * @throws SafaError If there is a problem updating the attribute.
     */
    @PutMapping(AppRoutes.Attribute.BY_KEY)
    public CustomAttributeAppEntity updateProjectAttribute(@PathVariable UUID projectId, @PathVariable String key,
                                                           @RequestBody CustomAttributeAppEntity appEntity) {

        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        if (key.isBlank()) {
            throw new SafaError("Attribute key cannot be blank");
        }

        if (!appEntity.getKey().equals(key)) {
            throw new SafaError("Cannot change attribute key.");
        }

        attributeService.saveEntity(appEntity, project, false);

        return getProjectAttribute(projectId, key);
    }

    /**
     * Deletes an attribute from a project.
     *
     * @param projectId The ID of the project.
     * @param key The key name of the attribute to remove.
     * @throws SafaError If there is a problem deleting the attribute.
     */
    @DeleteMapping(AppRoutes.Attribute.BY_KEY)
    @Transactional
    public void deleteProjectAttribute(@PathVariable UUID projectId, @PathVariable String key) throws SafaError {

        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();

        if (key.isBlank()) {
            throw new SafaError("Attribute key cannot be blank");
        }

        attributeService.deleteByProjectAndKeyname(project, key);
    }

}
