package edu.nd.crc.safa.features.attributes.entities.db.values;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeStorageType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "artifact_attribute_version")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class ArtifactAttributeVersion {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_version_id", nullable = false)
    private ArtifactVersion artifactVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_id", nullable = false)
    private CustomAttribute attribute;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "attributeVersion", fetch = FetchType.EAGER)
    private BooleanAttributeValue booleanValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "attributeVersion", fetch = FetchType.EAGER)
    private FloatAttributeValue floatValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "attributeVersion", fetch = FetchType.EAGER)
    private IntegerAttributeValue intValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "attributeVersion", fetch = FetchType.EAGER)
    private StringAttributeValue stringValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToMany(mappedBy = "attributeVersion", fetch = FetchType.EAGER)
    private List<StringArrayAttributeValue> stringArrayValue;

    public CustomAttributeStorageType getValueType() {
        return attribute.getType().getStorageType();
    }

    public boolean getBooleanValue() {
        if (getValueType() != CustomAttributeStorageType.BOOLEAN || booleanValue == null) {
            throw new NullPointerException("This attribute does not have a boolean value.");
        }
        return booleanValue.isValue();
    }

    public float getFloatValue() {
        if (getValueType() != CustomAttributeStorageType.FLOAT || floatValue == null) {
            throw new NullPointerException("This attribute does not have a float value.");
        }
        return floatValue.getValue();
    }

    public int getIntegerValue() {
        if (getValueType() != CustomAttributeStorageType.INTEGER || intValue == null) {
            throw new NullPointerException("This attribute does not have an int value.");
        }
        return intValue.getValue();
    }

    public String getStringValue() {
        if (getValueType() != CustomAttributeStorageType.STRING || stringValue == null) {
            throw new NullPointerException("This attribute does not have a string value.");
        }
        return stringValue.getValue();
    }

    public List<String> getStringArrayValue() {
        if (getValueType() != CustomAttributeStorageType.STRING_ARRAY || stringArrayValue == null) {
            throw new NullPointerException("This attribute does not have a string value.");
        }
        return stringArrayValue.stream().map(StringArrayAttributeValue::getValue).collect(Collectors.toList());
    }
}
