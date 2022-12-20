package edu.nd.crc.safa.features.artifacts.entities.db.schema;

import java.util.function.Supplier;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.BooleanFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.FloatFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IntegerFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringArrayFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringFieldValue;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Contains details about how values for custom artifact attributes are actually
 * stored within the database.
 */
@Getter
@AllArgsConstructor
public enum ArtifactFieldStorageType {
    STRING(StringFieldValue::new, false),
    STRING_ARRAY(StringArrayFieldValue::new, true),
    INTEGER(IntegerFieldValue::new, false),
    FLOAT(FloatFieldValue::new, false),
    BOOLEAN(BooleanFieldValue::new, false);

    final Supplier<IFieldValue> fieldValueSupplier;
    final boolean isArrayType;
}
