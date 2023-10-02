module.exports = {
  root: true,
  globals: {
    defineProps: "readonly",
    defineEmits: "readonly",
  },
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "@vue/eslint-config-typescript/recommended",
    "@vue/prettier",
    // "plugin:import/errors",
    "plugin:import/warnings",
  ],
  parserOptions: {
    ecmaVersion: "latest",
  },
  plugins: ["prettier"],
  settings: {},
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "max-lines": ["warn", 300],
    "vue/no-mutating-props": 0,
    "vue/script-setup-uses-vars": "error",
    "vue/multi-word-component-names": 0,
    "@typescript-eslint/no-duplicate-enum-values": ["off"],
    "prettier/prettier": [
      "warn",
      {
        trailingComma: "es5",
        endOfLine: "auto",
        printWidth: 80,
      },
    ],
    "import/order": [
      "warn",
      {
        groups: [
          "builtin",
          "external",
          "type",
          "internal",
          "parent",
          "sibling",
          "index",
          "object",
        ],
        pathGroups: [
          {
            pattern: "@/types",
            group: "type",
          },
          {
            pattern: "@/util",
            group: "internal",
            position: "before",
          },
          {
            pattern: "@/hooks",
            group: "internal",
            position: "before",
          },
          {
            pattern: "@/router",
            group: "internal",
            position: "before",
          },
          {
            pattern: "@/api",
            group: "internal",
            position: "before",
          },
          {
            pattern: "@/cytoscape",
            group: "internal",
            position: "before",
          },
          {
            pattern: "@/components",
            group: "internal",
            position: "after",
          },
          {
            pattern: "@/views",
            group: "internal",
            position: "after",
          },
          {
            pattern: "@/**",
            group: "internal",
          },
        ],
      },
    ],
  },
  overrides: [
    {
      files: [
        "**/__tests__/*.{j,t}s?(x)",
        "**/tests/unit/**/*.spec.{j,t}s?(x)",
      ],
      env: {
        mocha: true,
      },
    },
  ],
};
