const express = require("express");
const router = express.Router();
const fingerprintController = require("../controllers/fp.controller");

// POST /fingerprints/
router.post("/", fingerprintController.create);

// ✅ GET /fingerprints/ — test endpoint
router.get("/", (req, res) => {
  res.status(200).json({ message: "GET /fingerprints is working!" });
});

module.exports = router;