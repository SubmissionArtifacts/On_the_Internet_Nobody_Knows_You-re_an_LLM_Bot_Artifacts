const express = require("express");
const router = express.Router();
const challengeController = require("../controllers/challenge.controller");

// POST /posts/
router.post("/", challengeController.create);

module.exports = router;