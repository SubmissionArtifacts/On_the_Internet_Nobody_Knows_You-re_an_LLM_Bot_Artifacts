const ChallengeModel = require("../models/challenge.model");

exports.create = async (req, res) => {
  try {
    if (!req.body) {
      return res.status(400).send("No body sent.");
    }
    let {challenge, headers, siteKey} = req.body;
    if (!headers) {
      headers = req.headers;
    }

    // Create a new MongoDB document
    const newDocument = new ChallengeModel({
      siteKey: siteKey,
      challenge: challenge,
      httpHeaders: headers,
    });

    // Save the document in MongoDB
    await newDocument.save();
    res.status(200).json({ status: "Data saved" });
  } catch (error) {
    console.error("Error occurred:", error);
    res.status(500).json({ status: "Error occurred" });
  }
};
