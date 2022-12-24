package edu.nd.crc.safa.features.artifacts.services;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.transaction.Transactional;

import edu.nd.crc.safa.features.artifacts.entities.AttributeSchemaAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldExtraInfoType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.FloatFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.IntegerFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.SelectionFieldOption;
import edu.nd.crc.safa.features.artifacts.repositories.schema.FloatFieldInfoRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.IntegerFieldInfoRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.SelectionFieldOptionRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.stereotype.Service;

/**
 * The attribute service provides utility functions to help with handling
 * attributes, particularly with translating between back-end and front-end
 * representations of attribute definitions.
 */
@Service
public class AttributeService {

    //TODO tests

    private final ArtifactSystemServiceProvider serviceProvider;

    public AttributeService(ArtifactSystemServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    /**
     * Creates a front-end attribute representation from a back-end attribute representation.
     *
     * @param attribute The front-end attribute schema object.
     * @return The back-end attribute schema object.
     */
    public AttributeSchemaAppEntity appEntityFromCustomAttribute(CustomAttribute attribute) {
        AttributeSchemaAppEntity out = new AttributeSchemaAppEntity(attribute.getKeyname(), attribute.getLabel(),
            attribute.getType());

        switch (attribute.getType().getExtraInfoType()) {
            case OPTIONS:
                out.setOptions(getStringOptionsForAttribute(attribute));
                break;
            case FLOAT_BOUNDS:
                FloatFieldInfo floatInfo = getFloatFieldInfoForAttribute(attribute);
                out.setMin(floatInfo.getMin());
                out.setMax(floatInfo.getMax());
                break;
            case INT_BOUNDS:
                IntegerFieldInfo intInfo = getIntegerFieldInfoForAttribute(attribute);
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
    public List<SelectionFieldOption> getOptionsForAttribute(CustomAttribute attribute) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }
        return serviceProvider.getSelectionFieldOptionRepository().findBySchemaField(attribute);
    }

    /**
     * Retrieves selection options for a custom attribute as strings.
     *
     * @param attribute The attribute to get options for.
     * @return The options, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have selection options.
     */
    public List<String> getStringOptionsForAttribute(CustomAttribute attribute) {
        return getOptionsForAttribute(attribute)
            .stream()
            .map(SelectionFieldOption::getValue)
            .collect(Collectors.toList());
    }

    /**
     * Retrieves float bounds for a custom attribute.
     * @param attribute The attribute to get the bounds of.
     * @return The bounds, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have float bounds.
     * @throws IllegalStateException If this attribute is supposed to have float bounds, but they are not found.
     */
    public FloatFieldInfo getFloatFieldInfoForAttribute(CustomAttribute attribute) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        Optional<FloatFieldInfo> fieldInfo =
            serviceProvider.getFloatFieldInfoRepository().findBySchemaField(attribute);

        if (fieldInfo.isEmpty()) {
            throw new IllegalStateException("Custom attribute should have float info associated with it,"
                + " but it was not found.");
        }

        return fieldInfo.get();
    }

    /**
     * Retrieves integer bounds for a custom attribute.
     * @param attribute The attribute to get the bounds of.
     * @return The bounds, if they are found.
     * @throws IllegalArgumentException If this attribute is not supposed to have integer bounds.
     * @throws IllegalStateException If this attribute is supposed to have integer bounds, but they are not found.
     */
    public IntegerFieldInfo getIntegerFieldInfoForAttribute(CustomAttribute attribute) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have integer info associated with it.");
        }

        Optional<IntegerFieldInfo> fieldInfo =
            serviceProvider.getIntegerFieldInfoRepository().findBySchemaField(attribute);

        if (fieldInfo.isEmpty()) {
            throw new IllegalStateException("Custom attribute should have integer info associated with it,"
                + " but it was not found.");
        }

        return fieldInfo.get();
    }

    /**
     * Creates a new CustomAttribute object based on the given front-end entity. Note that this
     * does not create any additional objects such as selection objects or numerical bounds.
     *
     * @param appEntity The front-end attribute entity.
     * @return A newly created back-end entity.
     */
    public CustomAttribute customAttributeFromAppEntity(AttributeSchemaAppEntity appEntity) {
        CustomAttribute out = new CustomAttribute();
        out.setType(appEntity.getType());
        out.setLabel(appEntity.getLabel());
        out.setKeyname(appEntity.getKey());
        return out;
    }

    /**
     * Creates selection options based on the given front-end entity.
     *
     * @param appEntity The front-end attribute entity.
     * @param parentAttribute The custom attribute these options belong to.
     * @return Newly created selection options.
     * @throws IllegalArgumentException If this object is not supposed to have selection options.
     */
    public List<SelectionFieldOption> selectionOptionsFromAppEntity(AttributeSchemaAppEntity appEntity,
                                                                    CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }

        return appEntity.getOptions()
            .stream()
            .map(option -> new SelectionFieldOption(parentAttribute, option))
            .collect(Collectors.toList());
    }

    /**
     * Creates a float bounds object based on the data in the given front-end object.
     *
     * @param appEntity The front-end attribute entity.
     * @param parentAttribute The custom attribute these bounds belong to.
     * @return Newly created float bounds.
     * @throws IllegalArgumentException If this object is not supposed to have float bounds.
     */
    public FloatFieldInfo floatFieldInfoFromAppEntity(AttributeSchemaAppEntity appEntity,
                                                      CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        return new FloatFieldInfo(parentAttribute, appEntity.getMin().floatValue(), appEntity.getMax().floatValue());
    }

    /**
     * Creates an int bounds object based on the data in the given front-end object.
     *
     * @param appEntity The front-end attribute entity.
     * @param parentAttribute The custom attribute these bounds belong to.
     * @return Newly created int bounds.
     * @throws IllegalArgumentException If this object is not supposed to have int bounds.
     */
    public IntegerFieldInfo intFieldInfoFromAppEntity(AttributeSchemaAppEntity appEntity,
                                                      CustomAttribute parentAttribute) {

        if (appEntity.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have int info associated with it.");
        }

        return new IntegerFieldInfo(parentAttribute, appEntity.getMin().intValue(), appEntity.getMax().intValue());
    }

    /**
     * Saves a front-end attribute entity into the database. This function assumes the user
     * has permission to modify project attributes and does not check to ensure this is true.
     *
     * @param appEntity The attribute object from the front-end.
     * @param project The project the attribute is a part of.
     * @param isNew Whether this is a new attribute being created or an existing attribute being updated.
     * @throws SafaError If the attribute was marked as new, but an attribute with that key already exists
     *                   within the project; or if the attribute was marked as not new, but no attribute with
     *                   that key was found withing the project.
     */
    @Transactional
    public void saveEntity(AttributeSchemaAppEntity appEntity, Project project, boolean isNew) {
        CustomAttribute newAttribute = customAttributeFromAppEntity(appEntity);
        newAttribute.setProject(project);

        if (isNew) {
            if (serviceProvider.getCustomAttributeRepository().existsByProjectAndKeyname(project, appEntity.getKey())) {
                throw new SafaError(String.format("Attribute with the name %s already exists within this project.",
                    appEntity.getKey()));
            }
        } else {
            Optional<CustomAttribute> oldAttributeOpt = serviceProvider.getCustomAttributeRepository()
                .findByProjectAndKeyname(project, appEntity.getKey());

            if (oldAttributeOpt.isEmpty()) {
                throw new SafaError(String.format("Attribute with the name %s doesn't exist within this project.",
                    appEntity.getKey()));
            }

            checkModifiedValues(newAttribute, oldAttributeOpt.get());
            newAttribute.setId(oldAttributeOpt.get().getId());
        }

        newAttribute = serviceProvider.getCustomAttributeRepository().save(newAttribute);
        saveExtraInfo(newAttribute, appEntity);
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
            throw new SafaError("Cannot modify type."); //TODO some type modifications are allowed
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
    public void saveExtraInfo(CustomAttribute attribute, AttributeSchemaAppEntity appEntity) {
        switch (attribute.getType().getExtraInfoType()) {
            case OPTIONS:
                saveSelectionOptions(attribute, appEntity);
                break;
            case FLOAT_BOUNDS:
                saveFloatFieldInfo(attribute, appEntity);
                break;
            case INT_BOUNDS:
                saveIntegerFieldInfo(attribute, appEntity);
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
    public void saveSelectionOptions(CustomAttribute attribute, AttributeSchemaAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.OPTIONS) {
            throw new IllegalArgumentException("The given custom attribute does not have options associated with it.");
        }

        SelectionFieldOptionRepository optionRepo = serviceProvider.getSelectionFieldOptionRepository();
        List<SelectionFieldOption> options = selectionOptionsFromAppEntity(appEntity, attribute);
        optionRepo.deleteBySchemaField(attribute);
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
    public void saveFloatFieldInfo(CustomAttribute attribute, AttributeSchemaAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have float info associated with it.");
        }

        FloatFieldInfoRepository floatFieldRepo = serviceProvider.getFloatFieldInfoRepository();
        FloatFieldInfo floatInfo = floatFieldInfoFromAppEntity(appEntity, attribute);

        floatInfo.setId(
            floatFieldRepo.findBySchemaField(attribute)
                .map(FloatFieldInfo::getId)
                .orElse(null));

        floatFieldRepo.save(floatInfo);
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
    public void saveIntegerFieldInfo(CustomAttribute attribute, AttributeSchemaAppEntity appEntity) {
        if (attribute.getType().getExtraInfoType() != ArtifactFieldExtraInfoType.INT_BOUNDS) {
            throw new IllegalArgumentException(
                "The given custom attribute does not have int info associated with it.");
        }

        IntegerFieldInfoRepository intFieldRepo = serviceProvider.getIntegerFieldInfoRepository();
        IntegerFieldInfo intInfo = intFieldInfoFromAppEntity(appEntity, attribute);

        intInfo.setId(
            intFieldRepo.findBySchemaField(attribute)
                .map(IntegerFieldInfo::getId)
                .orElse(null));

        intFieldRepo.save(intInfo);
    }
}
