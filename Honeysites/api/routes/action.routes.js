const express = require("express");
const router = express.Router();
const actionsController = require("../controllers/action.controller");

// POST /fingerprints/
router.post("/", actionsController.create);


module.exports = router;