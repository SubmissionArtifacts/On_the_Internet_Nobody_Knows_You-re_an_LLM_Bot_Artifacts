const mongoose = require("mongoose");

const FPSchema = mongoose.Schema(
  {
    cookieId: { type: String, index: true },
    timestamp: { type: Number, default: Date.now },
    siteKey: { type: String, default: "site0" },
    sessionId: { type: String, default:"" },
  },
  {
    timestamps: true,
    strict: false,
    versionKey: false,
  }
);

module.exports = mongoose.model("Fingerprint", FPSchema);
