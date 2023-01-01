package edu.nd.crc.safa.features.attributes.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.services.AttributeLayoutService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

public class AttributeLayoutController extends BaseController {

    private final AttributeLayoutService attributeLayoutService;

    @Autowired
    public AttributeLayoutController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                     AttributeLayoutService attributeLayoutService) {
        super(resourceBuilder, serviceProvider);
        this.attributeLayoutService = attributeLayoutService;
    }

    /**
     * Creates a new attribute layout within the given project.
     *
     * @param projectId The ID of project containing the new layout.
     * @param layout The layout entity to create.
     * @return The newly created layout entity.
     */
    @PostMapping(AppRoutes.AttributeLayout.ROOT)
    public AttributeLayoutAppEntity createLayout(@PathVariable UUID projectId,
                                                 @RequestBody AttributeLayoutAppEntity layout) {
        return null;
    }

    /**
     * Edits an existing attribute layout.
     *
     * @param projectId The ID of project containing the layout to edit.
     * @param id The ID of the layout to edit.
     * @param layout The new version of the layout.
     * @return The new version of the layout as saved in the database.
     */
    @PutMapping(AppRoutes.AttributeLayout.BY_ID)
    public AttributeLayoutAppEntity editLayout(@PathVariable UUID projectId, @PathVariable UUID id,
                                               @RequestBody AttributeLayoutAppEntity layout) {
        return null;
    }

    /**
     * Deletes an attribute layout.
     *
     * @param projectId The ID of project containing the layout to delete.
     * @param id The ID of the layout to delete.
     */
    @DeleteMapping(AppRoutes.AttributeLayout.BY_ID)
    public void deleteLayout(@PathVariable UUID projectId, @PathVariable UUID id) {
        return;
    }

    /**
     * Returns a specific attribute layout.
     *
     * @param projectId The ID of project containing the layout.
     * @param id The ID of the layout.
     * @return The layout with that ID.
     */
    @GetMapping(AppRoutes.AttributeLayout.BY_ID)
    public AttributeLayoutAppEntity getLayout(@PathVariable UUID projectId, @PathVariable UUID id) {
        return null;
    }

    /**
     * Returns all attribute layouts within the given project.
     *
     * @param projectId The ID of project.
     * @return All layouts within the given project.
     */
    @GetMapping(AppRoutes.AttributeLayout.ROOT)
    public List<AttributeLayoutAppEntity> getProjectLayouts(@PathVariable UUID projectId) {
        return null;
    }
}
