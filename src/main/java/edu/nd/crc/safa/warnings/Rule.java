package edu.nd.crc.safa.warnings;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.db.entities.sql.Warning;

public class Rule {
    private final Name mName;
    public List<Tokenizer.Token> mTokens;
    List<String> ImplementedFunctions = Arrays.asList(
        "at-least-one",
        "at-least-n",
        "exactly-one",
        "exactly-n",
        "less-than-n"
    );
    String mText;

    public Rule() {
        mName = new Name();
        mText = "";
        mTokens = new ArrayList<>();
    }

    public Rule(Rule that) {
        mName = that.mName;
        mText = that.mText;
        mTokens = new ArrayList<>(that.mTokens);
    }

    public Rule(final String name, final String longname, final String rule) {
        mName = new Name(name, longname);
        mText = rule;
        mTokens = Tokenizer.lex(mText);
    }

    public Rule(Warning warning) {
        this(warning.getNShort(), warning.getNLong(), warning.getRule());
    }

    public Name getName() {
        return mName;
    }

    public String unprocessedRule() {
        return mText;
    }

    public boolean result() {
        return mTokens.get(0).t == Tokenizer.Type.TRUE;
    }

    public boolean isValid() {
        // Handle unbalanced parenthesis
        long lParenCount = mTokens.stream().filter(t -> t.t == Tokenizer.Type.LPAREN).count();
        long rParenCount = mTokens.stream().filter(t -> t.t == Tokenizer.Type.RPAREN).count();
        if (lParenCount != rParenCount) {
            return false;
        }

        // Handle unbalanced function
        long fStartCount = mTokens.stream().filter(t -> t.t == Tokenizer.Type.FUNCS).count();
        long fEndCount = mTokens.stream().filter(t -> t.t == Tokenizer.Type.FUNCE).count();
        if (fStartCount != fEndCount) {
            return false;
        }

        // Handle functions that are not implemented
        return mTokens
            .stream()
            .filter(t -> t.t == Tokenizer.Type.FUNCS)
            .anyMatch(t -> ImplementedFunctions.contains(t.c));
    }

    public Optional<Function> nextFunction() {
        Function r = new Function();

        String name = "";
        List<String> arguments = new ArrayList<>();
        for (final Tokenizer.Token t : mTokens) {
            if (t.t == Tokenizer.Type.FUNCS) {
                name = t.c;
            }

            if (t.t == Tokenizer.Type.ARGUMENT) {
                arguments.add(t.c);
            }

            if (t.t == Tokenizer.Type.FUNCE) {
                break;
            }
        }

        if (name.equals("")) {
            return Optional.empty();
        }

        int argOffset = 0;
        switch (name) {
            case "at-least-one":
                r.Requirement = Requirement.ATLEAST;
                r.Count = 1;
                break;
            case "at-least-n":
                r.Requirement = Requirement.ATLEAST;
                r.Count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            case "exactly-one":
                r.Requirement = Requirement.EXACTLY;
                r.Count = 1;
                break;
            case "exactly-n":
                r.Requirement = Requirement.EXACTLY;
                r.Count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            case "less-than-n":
                r.Requirement = Requirement.LESSTHAN;
                r.Count = Integer.parseInt(arguments.get(0).trim());
                argOffset++;
                break;
            default:
        }

        r.Target = arguments.get(argOffset).trim().toLowerCase();
        switch (arguments.get(argOffset + 1).trim().toLowerCase()) {
            case "child":
                r.Relationship = Relationship.CHILD;
                break;
            case "sibling":
                r.Relationship = Relationship.SIBLING;
                break;
            default:
        }
        r.RequiredTarget = arguments.get(argOffset + 2).trim().toLowerCase();

        return Optional.of(r);
    }

    public void setFunctionResult(final boolean result) {
        int start = -1;
        int end = -1;
        for (int i = 0; i < mTokens.size(); i++) {
            final Tokenizer.Token t = mTokens.get(i);
            if (t.t == Tokenizer.Type.FUNCS) {
                start = i;
            }

            if (t.t == Tokenizer.Type.FUNCE) {
                end = i;
                break;
            }
        }

        if (result) {
            mTokens.set(start, new Tokenizer.Token(Tokenizer.Type.TRUE, "True"));
        } else {
            mTokens.set(start, new Tokenizer.Token(Tokenizer.Type.FALSE, "False"));
        }

        for (int i = start; i < end; i++) {
            mTokens.remove(start + 1);
        }
    }

    public boolean reduce() {
        return reduceSingle(mTokens);
    }

    public boolean reduceSingle(List<Tokenizer.Token> input) {
        // Handle Parentesis groups
        int leftParen = -1;
        int rightParen = -1;
        for (int i = 0; i < input.size(); i++) {
            final Tokenizer.Token t = input.get(i);
            if (t.t == Tokenizer.Type.LPAREN) {
                leftParen = i;
            }
            if (leftParen != -1 && t.t == Tokenizer.Type.RPAREN) {
                rightParen = i;
                break;
            }
        }

        if (leftParen != -1 && rightParen != -1) {
            List<Tokenizer.Token> group = input.subList(leftParen + 1, rightParen);
            reduceSingle(group);

            if (group.size() > 1) {
                return false;
            }

            final Tokenizer.Token t = group.get(0);
            input.set(leftParen, t);
            input.remove(leftParen + 1);
            input.remove(leftParen + 1);
            return true;
        }

        // Handle Not
        for (int i = 0; i < input.size(); i++) {
            final Tokenizer.Token t = input.get(i);
            if (t.t == Tokenizer.Type.NOT) {
                final Tokenizer.Token b = input.get(i + 1);
                assert b.isBoolean();

                if (b.t == Tokenizer.Type.TRUE) {
                    input.set(i, new Tokenizer.Token(Tokenizer.Type.FALSE, "False"));
                } else {
                    input.set(i, new Tokenizer.Token(Tokenizer.Type.TRUE, "True"));
                }
                input.remove(i + 1);
                return true;
            }
        }

        // Handle AND
        for (int i = 0; i < input.size(); i++) {
            final Tokenizer.Token t = input.get(i);
            if (t.t == Tokenizer.Type.AND) {
                final Tokenizer.Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.t == Tokenizer.Type.TRUE;

                final Tokenizer.Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.t == Tokenizer.Type.TRUE;

                if (leftBool && rightBool) {
                    input.set(i - 1, new Tokenizer.Token(Tokenizer.Type.TRUE, "True"));
                } else {
                    input.set(i - 1, new Tokenizer.Token(Tokenizer.Type.FALSE, "False"));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        // Handle OR
        for (int i = 0; i < input.size(); i++) {
            final Tokenizer.Token t = input.get(i);
            if (t.t == Tokenizer.Type.OR) {
                final Tokenizer.Token left = input.get(i - 1);
                assert left.isBoolean();
                final boolean leftBool = left.t == Tokenizer.Type.TRUE;

                final Tokenizer.Token right = input.get(i + 1);
                assert right.isBoolean();
                final boolean rightBool = right.t == Tokenizer.Type.TRUE;

                if (leftBool || rightBool) {
                    input.set(i - 1, new Tokenizer.Token(Tokenizer.Type.TRUE, "True"));
                } else {
                    input.set(i - 1, new Tokenizer.Token(Tokenizer.Type.FALSE, "False"));
                }
                input.remove(i);
                input.remove(i);
                return true;
            }
        }

        return false;
    }

    public enum Requirement {
        ATLEAST, EXACTLY, LESSTHAN,
    }

    public enum Relationship {
        CHILD, SIBLING,
    }

    public static class Name {
        public String Short;
        public String Long;

        public Name() {
            Short = "";
            Long = "";
        }

        public Name(String s, String l) {
            Short = s;
            Long = l;
        }
    }

    public static class Function {
        public int Count;
        public Requirement Requirement;
        public String Target;
        public Relationship Relationship;
        public String RequiredTarget;
    }
}
