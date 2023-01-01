package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AttributeLayoutAppEntity {

    @NotNull
    @NotEmpty
    private String id;

    @NotNull
    @NotEmpty
    private String name;

    @NotNull
    private List<String> artifactTypes;

    @NotNull
    private List<AttributePositionAppEntity> positions;
}
