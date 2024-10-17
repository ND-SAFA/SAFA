// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require("fs");

module.exports = {
  configureWebpack: {
    resolve: {
      fallback: {
        fs: false,
      },
    },
    devServer: {
      client: { overlay: false },
    },
  },
  transpileDependencies: ["quasar"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
    quasar: {
      importStrategy: "kebab",
      rtlSupport: false,
    },
  },
  lintOnSave: true,
  css: {
    loaderOptions: {
      sass: {
        sassOptions: {
          quietDeps: true,
        },
      },
    },
  },
  pwa: {
    iconPaths: {
      favicon16: "favicon.ico",
      favicon32: "favicon.ico",
    },
  },
};
