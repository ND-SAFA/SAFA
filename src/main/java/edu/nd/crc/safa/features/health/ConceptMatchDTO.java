package edu.nd.crc.safa.features.health;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class ConceptMatchDTO {
    /**
     * ID of concept artifact matched.
     */
    private String id;
    /**
     * Index in artifact context where match occurs.
     */
    private int loc;
}
