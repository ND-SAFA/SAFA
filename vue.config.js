// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require("fs");

module.exports = {
  transpileDependencies: ["vuetify"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
  },
  lintOnSave: true,
  pwa: {
    iconPaths: {
      favicon16: "favicon.ico",
      favicon32: "favicon.ico",
    },
  },
  devServer: fs.existsSync("./certs/localhost.safa.ai.pem")
    ? {
        https: {
          key: fs.readFileSync("./certs/localhost.safa.ai-key.pem"),
          cert: fs.readFileSync("./certs/localhost.safa.ai.pem"),
        },
        host: "localhost.safa.ai",
        port: 8080,
      }
    : {},
  //TODO: remove after fully migrating to Vue3.
  chainWebpack: (config) => {
    config.resolve.alias.set("vue", "@vue/compat");

    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => {
        return {
          ...options,
          compilerOptions: {
            compatConfig: {
              MODE: 2,
            },
          },
        };
      });
  },
};
