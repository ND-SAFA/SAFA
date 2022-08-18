package edu.nd.crc.safa.features.rules.parser;

/**
 * The types of token expected to be found in a rule definition.
 */
public enum TokenType {
    LEFT_PAREN,
    RIGHT_PAREN,
    FUNC_START,
    FUNC_END,
    ARGUMENT,
    NOT,
    AND,
    OR,
    TRUE,
    FALSE
}
