const mongoose = require("mongoose");

const Action = mongoose.Schema(
  {
    cookieId: { type: String, index: true },
    siteKey: { type: String, default: "site0" },
    actionType : { type: String },
    actionValue : { type: String },
  },
  {
    timestamps: true,
    strict: false,
    versionKey: false,
  }
);

module.exports = mongoose.model("Action", Action);
