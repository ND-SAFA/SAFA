package edu.nd.crc.safa.features.attributes.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeExtraInfoType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.FloatAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.IntegerAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.SelectionAttributeOption;
import edu.nd.crc.safa.features.attributes.repositories.definitions.FloatAttributeInfoRepository;
import edu.nd.crc.safa.features.attributes.repositories.definitions.IntegerAttributeInfoRepository;
import edu.nd.crc.safa.features.attributes.repositories.definitions.SelectionAttributeOptionRepository;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

/**
 * The attribute service provides utility functions to help with handling
 * attributes, particularly with translating between back-end and front-end
 * representations of attribute definitions.
 */
@AllArgsConstructor
@Service
public class AttributeService {
    private final NotificationService notificationService;
    private final AttributeSystemServiceProvider serviceProvider;

    /**
     * Creates a front-end attribute representation from a back-end attribute representation.
     *
     * @param attribute The front-end attribute schema object.
     * @return The back-end attribute schema object.
     */
    public CustomAttributeAppEntity appEntityFromCustomAttribute(CustomAttribute attribute) {
        CustomAttributeAppEntity out = new CustomAttributeAppEntity(attribute.getKeyname(), attribute.getLabel(),
            attribute.getType());

        switch (attribute.getType().getExtraInfoType()) {
            case OPTIONS:
                out.setOptions(getStringOptionsForAttribute(attribute));
                break;
            case FLOAT_BOUNDS:
                FloatAttributeInfo floatInfo = getFloatAttributeInfoForAttribute(attribute);
                out.setMin(floatInfo.getMin());
                out.setMax(floatInfo.getMax());
                break;
            case INT_BOUNDS:
                IntegerAttributeInfo intInfo = getIntegerAttributeInfoForAttribute(attribute);
                out.setMin(intInfo.getMin());
                out.setMax(intInfo.getMax());
                break;
            default:
                break;
        }

        return out;
    }

    /**
     * Retrieves selection options for a custom attribute.
     *
     * @param attribute The attribute to get options for.
     * @return The options, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have selection options.
     */
    public List<SelectionAttributeOption> getOptionsForAttribute(CustomAttribute attribute) {
        return getOptionsForAttributeSorted(attribute, Sort.unsorted());
    }

    /**
     * Retrieves selection options for a custom attribute sorted by display label.
     *
     * @param attribute The attribute to get options for.
     * @return The options, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have selection options.
     */
    public List<SelectionAttributeOption> getOptionsForAttributeSorted(CustomAttribute attribute) {
        return getOptionsForAttributeSorted(attribute, Sort.by("value"));
    }

    /**
     * Retrieves selection options for a custom attribute sorted by the given sort.
     *
     * @param attribute The attribute to get options for.
     * @param sort      The sort to use for the retrieved data.
     * @return The options, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have selection options.
     */
    public List<SelectionAttributeOption> getOptionsForAttributeSorted(CustomAttribute attribute, Sort sort) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }
        return serviceProvider.getSelectionAttributeOptionRepository().findByAttribute(attribute, sort);
    }

    /**
     * Retrieves selection options for a custom attribute as strings.
     *
     * @param attribute The attribute to get options for.
     * @return The options, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have selection options.
     */
    public List<String> getStringOptionsForAttribute(CustomAttribute attribute) {
        return getOptionsForAttributeSorted(attribute)
            .stream()
            .map(SelectionAttributeOption::getValue)
            .collect(Collectors.toList());
    }

    /**
     * Retrieves float bounds for a custom attribute.
     *
     * @param attribute The attribute to get the bounds of.
     * @return The bounds, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have float bounds.
     * @throws IllegalStateException    If this attribute is supposed to have float bounds, but they are not found.
     */
    public FloatAttributeInfo getFloatAttributeInfoForAttribute(CustomAttribute attribute) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        Optional<FloatAttributeInfo> attributeInfo =
            serviceProvider.getFloatAttributeInfoRepository().findByAttribute(attribute);

        if (attributeInfo.isEmpty()) {
            throw new IllegalStateException("Custom attribute should have float info associated with it,"
                + " but it was not found.");
        }

        return attributeInfo.get();
    }

    /**
     * Retrieves integer bounds for a custom attribute.
     *
     * @param attribute The attribute to get the bounds of.
     * @return The bounds, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have integer bounds.
     * @throws IllegalStateException    If this attribute is supposed to have integer bounds, but they are not found.
     */
    public IntegerAttributeInfo getIntegerAttributeInfoForAttribute(CustomAttribute attribute) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have integer info associated with it.");
        }

        Optional<IntegerAttributeInfo> attributeInfo =
            serviceProvider.getIntegerAttributeInfoRepository().findByAttribute(attribute);

        if (attributeInfo.isEmpty()) {
            throw new IllegalStateException("Custom attribute should have integer info associated with it,"
                + " but it was not found.");
        }

        return attributeInfo.get();
    }

    /**
     * Creates a new CustomAttribute object based on the given front-end entity. Note that this
     * does not create any additional objects such as selection objects or numerical bounds.
     *
     * @param appEntity The front-end attribute entity.
     * @return A newly created back-end entity.
     */
    public CustomAttribute customAttributeFromAppEntity(CustomAttributeAppEntity appEntity) {
        CustomAttribute out = new CustomAttribute();
        out.setType(appEntity.getType());
        out.setLabel(appEntity.getLabel());
        out.setKeyname(appEntity.getKey());
        return out;
    }

    /**
     * Creates selection options based on the given front-end entity.
     *
     * @param appEntity       The front-end attribute entity.
     * @param parentAttribute The custom attribute these options belong to.
     * @return Newly created selection options.
     * @throws IllegalArgumentException If this object is not supposed to have selection options.
     */
    public List<SelectionAttributeOption> selectionOptionsFromAppEntity(CustomAttributeAppEntity appEntity,
                                                                        CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != CustomAttributeExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }

        List<String> options = appEntity.getOptions();

        if (options == null) {
            options = new ArrayList<>();
        }

        return options.stream()
            .map(option -> new SelectionAttributeOption(parentAttribute, option))
            .collect(Collectors.toList());
    }

    /**
     * Creates a float bounds object based on the data in the given front-end object.
     *
     * @param appEntity       The front-end attribute entity.
     * @param parentAttribute The custom attribute these bounds belong to.
     * @return Newly created float bounds.
     * @throws IllegalArgumentException If this object is not supposed to have float bounds.
     */
    public FloatAttributeInfo floatAttributeInfoFromAppEntity(CustomAttributeAppEntity appEntity,
                                                              CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        Number min = appEntity.getMin();
        Number max = appEntity.getMax();

        if (min == null) {
            min = -Float.MAX_VALUE;
        }

        if (max == null) {
            max = Float.MAX_VALUE;
        }

        return new FloatAttributeInfo(parentAttribute, min.doubleValue(), max.doubleValue());
    }

    /**
     * Creates an int bounds object based on the data in the given front-end object.
     *
     * @param appEntity       The front-end attribute entity.
     * @param parentAttribute The custom attribute these bounds belong to.
     * @return Newly created int bounds.
     * @throws IllegalArgumentException If this object is not supposed to have int bounds.
     */
    public IntegerAttributeInfo intAttributeInfoFromAppEntity(CustomAttributeAppEntity appEntity,
                                                              CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != CustomAttributeExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have int info associated with it.");
        }

        Number min = appEntity.getMin();
        Number max = appEntity.getMax();

        if (min == null) {
            min = Integer.MIN_VALUE;
        }

        if (max == null) {
            max = Integer.MAX_VALUE;
        }

        return new IntegerAttributeInfo(parentAttribute, min.intValue(), max.intValue());
    }

    /**
     * Saves a front-end attribute entity into the database. This function assumes the user
     * has permission to modify project attributes and does not check to ensure this is true.
     *
     * @param user      The user saving the entity.
     * @param appEntity The attribute object from the front-end.
     * @param project   The project the attribute is a part of.
     * @param isNew     Whether this is a new attribute being created or an existing attribute being updated.
     * @throws SafaError If the attribute was marked as new, but an attribute with that key already exists
     *                   within the project; or if the attribute was marked as not new, but no attribute with
     *                   that key was found withing the project.
     */
    @Transactional
    public void saveEntity(SafaUser user, Project project, CustomAttributeAppEntity appEntity, boolean isNew) {
        CustomAttribute newAttribute = customAttributeFromAppEntity(appEntity);
        newAttribute.setProjectId(project.getId());

        if (isNew) {
            if (serviceProvider.getCustomAttributeRepository()
                    .existsByProjectIdAndKeyname(project.getId(), appEntity.getKey())) {
                throw new SafaError("Attribute with the name %s already exists within this project.",
                    appEntity.getKey());
            }
        } else {
            Optional<CustomAttribute> oldAttributeOpt = serviceProvider.getCustomAttributeRepository()
                .findByProjectIdAndKeyname(project.getId(), appEntity.getKey());

            if (oldAttributeOpt.isEmpty()) {
                throw new SafaError("Attribute with the name %s doesn't exist within this project.",
                    appEntity.getKey());
            }

            checkModifiedValues(newAttribute, oldAttributeOpt.get());
            newAttribute.setId(oldAttributeOpt.get().getId());
        }

        newAttribute = serviceProvider.getCustomAttributeRepository().save(newAttribute);
        saveExtraInfo(newAttribute, appEntity);

        this.notificationService.broadcastChange(
            EntityChangeBuilder.create(user, project).withAttributeUpdate(appEntity)
        );
    }

    /**
     * Checks that values that are not allowed to change within an attribute were not changed from the
     * old version to the new version.
     *
     * @param newAttribute The new version of the attribute.
     * @param oldAttribute The existing version of the attribute in the database.
     */
    private void checkModifiedValues(CustomAttribute newAttribute, CustomAttribute oldAttribute) {
        if (!newAttribute.getKeyname().equals(oldAttribute.getKeyname())) {
            throw new SafaError("Cannot modify keyname.");
        }
        if (newAttribute.getType() != oldAttribute.getType()) {
            throw new SafaError("Cannot modify type."); //TODO some type modifications might later be allowed
        }
    }

    /**
     * Saves any extra info (selection options, numeric bounds, etc.) contained within a
     * front-end attribute entity into the database. Note that {@link AttributeService#saveEntity}
     * already calls this function, so it is not necessary to call both.
     *
     * @param attribute The parent attribute of the extra info.
     * @param appEntity The front-end entity containing the extra information.
     */
    @Transactional
    public void saveExtraInfo(CustomAttribute attribute, CustomAttributeAppEntity appEntity) {
        switch (attribute.getType().getExtraInfoType()) {
            case OPTIONS:
                saveSelectionOptions(attribute, appEntity);
                break;
            case FLOAT_BOUNDS:
                saveFloatAttributeInfo(attribute, appEntity);
                break;
            case INT_BOUNDS:
                saveIntegerAttributeInfo(attribute, appEntity);
                break;
            default:
                break;
        }
    }

    /**
     * Saves selection options contained within a front-end attribute entity into the database.
     * It is not necessary to call this function if {@link AttributeService#saveEntity} or
     * {@link AttributeService#saveExtraInfo} are already called.
     *
     * @param attribute The parent attribute of the selection options.
     * @param appEntity The front-end entity containing the selection options.
     * @throws IllegalArgumentException If this attribute is not meant to have selection options.
     */
    @Transactional
    public void saveSelectionOptions(CustomAttribute attribute, CustomAttributeAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }

        SelectionAttributeOptionRepository optionRepo = serviceProvider.getSelectionAttributeOptionRepository();
        List<SelectionAttributeOption> options = selectionOptionsFromAppEntity(appEntity, attribute);
        optionRepo.deleteByAttribute(attribute);
        optionRepo.saveAll(options);
    }

    /**
     * Saves float bounds contained within a front-end attribute entity into the database.
     * It is not necessary to call this function if {@link AttributeService#saveEntity} or
     * {@link AttributeService#saveExtraInfo} are already called.
     *
     * @param attribute The parent attribute of the float bounds.
     * @param appEntity The front-end entity containing the float bounds.
     * @throws IllegalArgumentException If this attribute is not meant to have float bounds.
     */
    @Transactional
    public void saveFloatAttributeInfo(CustomAttribute attribute, CustomAttributeAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        FloatAttributeInfoRepository floatAttributeRepo = serviceProvider.getFloatAttributeInfoRepository();
        FloatAttributeInfo floatInfo = floatAttributeInfoFromAppEntity(appEntity, attribute);

        floatInfo.setId(
            floatAttributeRepo.findByAttribute(attribute)
                .map(FloatAttributeInfo::getId)
                .orElse(null));

        floatAttributeRepo.save(floatInfo);
    }

    /**
     * Saves integer bounds contained within a front-end attribute entity into the database.
     * It is not necessary to call this function if {@link AttributeService#saveEntity} or
     * {@link AttributeService#saveExtraInfo} are already called.
     *
     * @param attribute The parent attribute of the integer bounds.
     * @param appEntity The front-end entity containing the integer bounds.
     * @throws IllegalArgumentException If this attribute is not meant to have integer bounds.
     */
    @Transactional
    public void saveIntegerAttributeInfo(CustomAttribute attribute, CustomAttributeAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != CustomAttributeExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have int info associated with it.");
        }

        IntegerAttributeInfoRepository intAttributeRepo = serviceProvider.getIntegerAttributeInfoRepository();
        IntegerAttributeInfo intInfo = intAttributeInfoFromAppEntity(appEntity, attribute);

        intInfo.setId(
            intAttributeRepo.findByAttribute(attribute)
                .map(IntegerAttributeInfo::getId)
                .orElse(null));

        intAttributeRepo.save(intInfo);
    }

    /**
     * Returns all custom attributes in a given project.
     *
     * @param project The project to search.
     * @return All attributes in the given project.
     */
    public List<CustomAttribute> getAttributesForProject(Project project) {
        return serviceProvider.getCustomAttributeRepository().findByProjectId(project.getId());
    }

    /**
     * Returns all custom attributes in a given project sorted by the given sort.
     *
     * @param project The project to search.
     * @param sort    The sort order to use.
     * @return All attributes in the given project.
     */
    public List<CustomAttribute> getAttributesForProject(Project project, Sort sort) {
        return serviceProvider.getCustomAttributeRepository().findByProjectId(project.getId(), sort);
    }

    /**
     * Returns all custom attributes in a given project as front-end entities.
     *
     * @param project The project to search.
     * @return All attributes in the given project.
     */
    public List<CustomAttributeAppEntity> getAttributeEntitiesForProject(Project project) {
        return this.getAttributesForProject(project)
            .stream()
            .map(this::appEntityFromCustomAttribute)
            .collect(Collectors.toList());
    }

    /**
     * Returns all custom attributes in a given project as front-end entities sorted by the given sort.
     *
     * @param project The project to search.
     * @param sort    The sort order to use.
     * @return All attributes in the given project.
     */
    public List<CustomAttributeAppEntity> getAttributeEntitiesForProject(Project project, Sort sort) {
        return this.getAttributesForProject(project, sort)
            .stream()
            .map(this::appEntityFromCustomAttribute)
            .collect(Collectors.toList());
    }

    /**
     * Finds an attribute with a given key within the given project.
     *
     * @param project The project to search.
     * @param keyname The key for the attribute to find.
     * @return The attribute, if it exists.
     */
    public Optional<CustomAttribute> getByProjectAndKeyname(Project project, String keyname) {
        return serviceProvider.getCustomAttributeRepository().findByProjectIdAndKeyname(project.getId(), keyname);
    }

    /**
     * Delete an attribute from the given project.
     *
     * @param project The project to delete from.
     * @param keyname The key of the attribute to delete.
     */
    public void deleteByProjectAndKeyname(Project project, String keyname) {
        serviceProvider.getCustomAttributeRepository().deleteByProjectIdAndKeyname(project.getId(), keyname);
    }
}
