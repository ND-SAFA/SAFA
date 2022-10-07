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
  devServer: fs.existsSync("./certs/localhost-key.pem")
    ? {
        https: {
          key: fs.readFileSync("./certs/localhost-key.pem"),
          cert: fs.readFileSync("./certs/localhost.pem"),
        },
        host: "localhost",
        port: 8080,
      }
    : {},
};
