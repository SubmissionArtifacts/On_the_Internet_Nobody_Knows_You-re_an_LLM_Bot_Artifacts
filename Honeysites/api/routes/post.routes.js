const express = require("express");
const router = express.Router();
const postController = require("../controllers/post.controller");

// GET /posts/:sitekey
router.get("/:sitekey", postController.getPostsBySiteKey);
// POST /posts/
router.post("/", postController.create);

module.exports = router;