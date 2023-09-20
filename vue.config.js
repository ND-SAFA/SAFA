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
  devServer: fs.existsSync("./certs/localhost.safa.ai.pem")
    ? {
        server: {
          type: "https",
          options: {
            key: fs.readFileSync("./certs/localhost.safa.ai-key.pem"),
            cert: fs.readFileSync("./certs/localhost.safa.ai.pem"),
          },
        },
        host: "localhost",
        port: 8080,
      }
    : {},
};
