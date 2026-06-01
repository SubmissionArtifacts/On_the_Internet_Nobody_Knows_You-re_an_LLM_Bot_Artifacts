const mongoose = require("mongoose");
const MONGO_USERNAME = process.env.MONGO_INITDB_ROOT_USERNAME;
const MONGO_PASSWORD = process.env.MONGO_INITDB_ROOT_PASSWORD;
const MONGO_HOST = process.env.MONGO_HOST;
const MONGO_PORT = process.env.MONGO_PORT;
const MONGO_DATABASE = process.env.MONGO_INITDB_DATABASE
const MONGO_URL = `mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DATABASE}`;
const connectOptions = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  authSource: "admin",
};
console.log("url : " + MONGO_URL)

mongoose.connect(MONGO_URL, connectOptions);
const database = mongoose.connection;

module.exports =database;
