package edu.nd.crc.safa.warnings;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Provides rules with a name and message.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RuleName {
    public String ruleName;
    public String ruleMessage;
}
