package edu.nd.crc.safa.test.features.attributes.crud;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeExtraInfoType;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.services.AttributeService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.features.attributes.AttributesForTesting;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestAttributeDefinitionCrud extends ApplicationBaseTest {

    @Autowired
    ObjectMapper jsonObjectMapper;

    @Autowired
    AttributeService attributeService;

    AttributesForTesting attributesForTesting = new AttributesForTesting();

    Project project;

    @Test
    public void testCrud() throws Exception {
        project = dbEntityBuilder.newProjectWithReturn(projectName);

        for (CustomAttributeType type : CustomAttributeType.values()) {
            runTest(type);
        }
    }

    private void runTest(CustomAttributeType type) throws Exception {
        checkCreate(type);
        checkRetrieve(type);
        checkUpdate(type);
        checkDelete(type);
    }

    private void checkCreate(CustomAttributeType type) throws Exception {
        CustomAttributeAppEntity appEntity = attributesForTesting.setupAttributeAppEntity(type);

        JSONObject response = SafaRequest
                .withRoute(AppRoutes.Attribute.ROOT)
                .withProject(project)
                .postWithJsonObject(appEntity);

        CustomAttributeAppEntity returnedEntity = jsonObjectMapper.readValue(response.toString(),
            CustomAttributeAppEntity.class);
        checkAppEntity(appEntity, returnedEntity);
    }

    private void checkRetrieve(CustomAttributeType type) throws Exception {
        CustomAttributeAppEntity expected = attributesForTesting.setupAttributeAppEntity(type);

        CustomAttributeAppEntity returnedEntity = SafaRequest
                .withRoute(AppRoutes.Attribute.BY_KEY)
                .withProject(project)
                .withKey(expected.getKey())
                .getAsType(new TypeReference<>() {});

        checkAppEntity(expected, returnedEntity);

        List<CustomAttributeAppEntity> returnedEntities = SafaRequest
                .withRoute(AppRoutes.Attribute.ROOT)
                .withProject(project)
                .getAsType(new TypeReference<>() {});

        assertEquals(1, returnedEntities.size());
        checkAppEntity(expected, returnedEntities.get(0));
    }

    private void checkUpdate(CustomAttributeType type) throws Exception {
        CustomAttributeAppEntity expected = attributesForTesting.setupAltAttributeAppEntity(type);

        JSONObject response = SafaRequest
                .withRoute(AppRoutes.Attribute.BY_KEY)
                .withProject(project)
                .withKey(expected.getKey())
                .putWithJsonObject(expected);

        CustomAttributeAppEntity returnedEntity = jsonObjectMapper.readValue(response.toString(),
            CustomAttributeAppEntity.class);
        checkAppEntity(expected, returnedEntity);
    }

    private void checkDelete(CustomAttributeType type) throws Exception {

        String key = attributesForTesting.attributes.get(type).keyName;

        JSONObject response = SafaRequest
                .withRoute(AppRoutes.Attribute.BY_KEY)
                .withProject(project)
                .withKey(key)
                .deleteWithJsonObject();

        Optional<CustomAttribute> attribute = attributeService.getByProjectAndKeyname(project, key);
        assertFalse(attribute.isPresent());
    }

    private void checkAppEntity(CustomAttributeAppEntity expected, CustomAttributeAppEntity actual) {
        assertEquals(expected.getType(), actual.getType());
        assertEquals(expected.getKey(), actual.getKey());
        assertEquals(expected.getLabel(), actual.getLabel());
        assertEquals(expected.getOptions(), actual.getOptions());

        // It gets mad if I do this the normal way just asserting things are equal
        if (actual.getType().getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            assertEquals(expected.getMin().floatValue(), actual.getMin().floatValue());
            assertEquals(expected.getMax().floatValue(), actual.getMax().floatValue());
        } else if (actual.getType().getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
            assertEquals(expected.getMin().intValue(), actual.getMin().intValue());
            assertEquals(expected.getMax().intValue(), actual.getMax().intValue());
        } else {
            assertNull(actual.getMin());
            assertNull(actual.getMax());
        }
    }
}
