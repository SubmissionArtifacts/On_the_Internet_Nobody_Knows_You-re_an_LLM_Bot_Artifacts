const mongoose = require("mongoose");

const ChallengeSchema = mongoose.Schema(
  {
    timestamp: { type: Number, default: Date.now },
    siteKey: { type: String, default: "site0" },
  },
  {
    timestamps: true,
    strict: false,
    versionKey: false,
  }
);

module.exports = mongoose.model("Challenge", ChallengeSchema);
