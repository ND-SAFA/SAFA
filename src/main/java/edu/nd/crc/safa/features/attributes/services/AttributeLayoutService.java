package edu.nd.crc.safa.features.attributes.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.features.attributes.entities.AttributeLayoutAppEntity;
import edu.nd.crc.safa.features.attributes.entities.AttributePositionAppEntity;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.ArtifactTypeToLayoutMapping;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributeLayout;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributePosition;
import edu.nd.crc.safa.features.attributes.repositories.layouts.ArtifactTypeToLayoutMappingRepository;
import edu.nd.crc.safa.features.attributes.repositories.layouts.AttributeLayoutRepository;
import edu.nd.crc.safa.features.attributes.repositories.layouts.AttributePositionRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.flatfiles.services.ArtifactTypeService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AttributeLayoutService implements IAppEntityService<AttributeLayoutAppEntity> {

    private final ArtifactTypeToLayoutMappingRepository typeToLayoutRepo;
    private final AttributeLayoutRepository layoutRepo;
    private final AttributePositionRepository positionRepo;
    private final AttributeService attributeService;
    private final ArtifactTypeService artifactTypeService;
    private final NotificationService notificationService;

    @Override
    public List<AttributeLayoutAppEntity> getAppEntities(ProjectVersion projectVersion) {
        return layoutRepo.findByProject(projectVersion.getProject())
                .stream()
                .map(this::appEntityFromAttributeLayout)
                .collect(Collectors.toList());
    }

    /**
     * Converts a back-end attribute layout entity into its front-end equivalent.
     *
     * @param attributeLayout The attribute layout entity to convert.
     * @return The front-end layout entity.
     */
    public AttributeLayoutAppEntity appEntityFromAttributeLayout(AttributeLayout attributeLayout) {
        List<String> artifactTypes = typeToLayoutRepo.findByLayout(attributeLayout)
                .stream()
                .map(mapping -> mapping.getArtifactType().getName())
                .collect(Collectors.toList());

        List<AttributePositionAppEntity> positions = positionRepo.findByLayout(attributeLayout)
                .stream()
                .map(this::appEntityFromAttributePosition)
                .collect(Collectors.toList());

        return new AttributeLayoutAppEntity(attributeLayout.getId(), attributeLayout.getName(),
                artifactTypes, positions);
    }

    /**
     * Converts a back-end attribute position entity into its front-end equivalent.
     *
     * @param attributePosition The attribute position entity to convert.
     * @return The front-end layout entity.
     */
    public AttributePositionAppEntity appEntityFromAttributePosition(AttributePosition attributePosition) {
        return new AttributePositionAppEntity(attributePosition.getAttribute().getKeyname(), attributePosition.getX(),
                attributePosition.getY(), attributePosition.getWidth(), attributePosition.getHeight());
    }

    /**
     * Constructs a back-end attribute layout object from the front-end version. This only converts the base
     * attribute layout object, not the child position objects or type mappings.
     *
     * @param project The project we're working in.
     * @param appEntity The front-end entity to convert.
     * @return The back-end representation of the front-end layout entity.
     */
    public AttributeLayout attributeLayoutFromAppEntity(Project project, AttributeLayoutAppEntity appEntity) {
        return new AttributeLayout(appEntity.getId(), appEntity.getName(), project);
    }

    /**
     * Constructs a back-end attribute position object from the front-end version.
     *
     * @param project The project we're working in.
     * @param layout The layout object the position exists in.
     * @param appEntity The front-end position entity.
     * @return The back-end representation of the front-end position entity.
     */
    public AttributePosition attributePositionFromAppEntity(Project project, AttributeLayout layout,
                                                            AttributePositionAppEntity appEntity) {
        Optional<CustomAttribute> attribute = attributeService.getByProjectAndKeyname(project, appEntity.getKey());
        return new AttributePosition(null, appEntity.getX(), appEntity.getY(), appEntity.getWidth(),
                appEntity.getHeight(), layout, attribute.orElseThrow());
    }

    /**
     * Finds a layout object based on its ID.
     *
     * @param id Layout ID.
     * @return Layout object with that ID.
     */
    public Optional<AttributeLayout> getLayoutById(UUID id) {
        return layoutRepo.findById(id);
    }

    /**
     * Gets all layouts associated with a particular project.
     *
     * @param project The project.
     * @return All layouts associated with this project.
     */
    public List<AttributeLayout> getLayoutsByProject(Project project) {
        return layoutRepo.findByProject(project);
    }

    /**
     * Deletes a layout by its ID.
     *
     * @param id The ID of the layout to delete.
     */
    @Transactional
    public void deleteLayoutById(UUID id) {
        Optional<AttributeLayout> layout = getLayoutById(id);
        layoutRepo.deleteById(id);

        if (layout.isPresent()) {
            Project project = layout.get().getProject();
            notificationService.broadcastChange(
                    EntityChangeBuilder.create(project.getProjectId()).withProjectUpdate(project.getProjectId())
            );
        }
    }

    /**
     * Save a front-end layout entity to the database.
     *
     * @param appEntity The entity to save.
     * @param project The project the layout is associated with.
     * @param isNew True if this layout is being newly created, false otherwise. If this is set to false and
     *              there is no layout with an ID that matches the given entity, the operation will fail and
     *              nothing will be saved.
     * @return The database entity that was created/updated.
     */
    @Transactional
    public AttributeLayout saveLayoutEntity(AttributeLayoutAppEntity appEntity, Project project, boolean isNew) {
        AttributeLayout layout = attributeLayoutFromAppEntity(project, appEntity);

        if (!isNew && (appEntity.getId() == null || layoutRepo.findById(appEntity.getId()).isEmpty())) {
            throw new SafaError("No layout with the ID %s was found.", appEntity.getId());
        }

        layout = layoutRepo.save(layout);
        saveArtifactTypes(layout, appEntity.getArtifactTypes());
        savePositions(layout, appEntity.getPositions());

        notificationService.broadcastChange(
                EntityChangeBuilder.create(project.getProjectId()).withProjectUpdate(project.getProjectId())
        );

        return layout;
    }

    /**
     * Saves all given position objects to the database under the given layout.
     *
     * @param layout The layout these positions belong to.
     * @param positions The front-end position representations.
     */
    @Transactional
    private void savePositions(AttributeLayout layout, List<AttributePositionAppEntity> positions) {
        positionRepo.deleteByLayout(layout);
        positions.stream()
                .map(position -> this.attributePositionFromAppEntity(layout.getProject(), layout, position))
                .forEach(positionRepo::save);
    }

    /**
     * Maps all given artifact types to the given layout and saves the mappings to the database.
     *
     * @param layout The layout associated with these artifact types.
     * @param artifactTypes The names of the artifact types.
     */
    @Transactional
    private void saveArtifactTypes(AttributeLayout layout, List<String> artifactTypes) {
        typeToLayoutRepo.deleteByLayout(layout);
        artifactTypes.stream()
                .map(typeName -> artifactTypeService.findArtifactType(layout.getProject(), typeName))
                .map(type -> new ArtifactTypeToLayoutMapping(layout, type))
                .forEach(typeToLayoutRepo::save);
    }
}
