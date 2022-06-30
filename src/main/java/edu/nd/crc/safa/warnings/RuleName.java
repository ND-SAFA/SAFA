package edu.nd.crc.safa.warnings;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Provides rules with a name and message.
 */
@Data
@AllArgsConstructor
public class RuleName {
    public String name;
    public String description;
}
