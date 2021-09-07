package edu.nd.crc.safa.warnings;

public class RuleName {
    public String ruleName;
    public String ruleMessage;

    public RuleName(String s, String l) {
        ruleName = s;
        ruleMessage = l;
    }

    public String toString() {
        return String.format("%s:%s", ruleName, ruleMessage);
    }
}
