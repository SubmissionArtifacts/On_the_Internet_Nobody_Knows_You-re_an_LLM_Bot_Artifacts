const mongoose = require("mongoose");

const PostSchema = mongoose.Schema(
  {
    firstName: { type: String, default: "First name" },
    lastName: { type: String, default: "Last name" },
    textContent: { type: String, default: "Post content" },
    siteKey: { type: String, default: "site0" },
    cookieId: { type: String, default: "cookieId" },
    authorId: { type: String, default: "authorId" },
  },
  {
    timestamps: true,
    strict: false,
    versionKey: false,
  }
);

module.exports = mongoose.model("Post", PostSchema);
