import dotenv, { DotenvConfigOutput } from "dotenv";

const config: DotenvConfigOutput = dotenv.config();
export const baseURL = config.parsed?.API_ENDPOINT;

console.log("URL", baseURL);
