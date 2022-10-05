// eslint-disable-next-line @typescript-eslint/no-var-requires
const fs = require("fs");

module.exports = {
  transpileDependencies: ["vuetify", "vuex-module-decorators", "vuex-persist"],
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
    },
  },
  lintOnSave: true,
  devServer: {
    https: {
      key: fs.readFileSync("./certs/localhost-key.pem"),
      cert: fs.readFileSync("./certs/localhost.pem"),
    },
  },
};
