const hiddenFilesAndFolders = "**/.*";

const imageFiles = [
  "**/*.jpg",
  "**/*.jpeg",
  "**/*.png",
  "**/*.gif",
  "**/*.bmp",
  "**/*.svg",
];

const dataFiles = [
  "**/*.json",
  "**/*.csv",
  "**/*.xls",
  "**/*.xlsx",
  "**/*.pdf",
  "**/*.txt",
  "**/*.text",
  "**/*.log",
];

const configurationFiles = [
  "**/ehthumbs.db",
  "**/Thumbs.db",
  "**/*.sublime*",
  "**/*.idea/**",
  "**/*.vscode/**",
  "**/*.swp",
  "**/*.swo",
  "**/*tsserver.log",
  "**/*.pid.lock",
  "**/npm-debug.log*",
  "**/yarn-debug.log*",
  "**/yarn-error.log*",
];

const envFiles = ["venv/**", "env/**", "ENV/**", "renv/**"];

const buildFiles = [
  "bin/**",
  "obj/**",
  "jars/**",
  "gems/**",
  "target/**",
  "out/**",
  "build/**",
  "_build/**",
];

const dependencyFiles = [
  "node_modules/**",
  "dependencies/**",
  "dist-packages/**",
  "site-packages/**",
  "vendor/**",
  "bower_components/**",
  "lib/**",
  "libs/**",
  "egg-info/**",
  "Pods/**",
];

/**
 * Default exclude patterns for GitHub.
 */
export const GITHUB_DEFAULT_EXCLUDE = [
  hiddenFilesAndFolders,
  ...imageFiles,
  ...dataFiles,
  ...configurationFiles,
  ...dependencyFiles,
  ...envFiles,
  ...buildFiles,
];
