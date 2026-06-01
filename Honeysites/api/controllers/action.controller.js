const Action = require("../models/action.model");
const { v4: uuidv4 } = require("uuid");

// Create and Save a new Document
exports.create = async (req, res) => {
   try {
    // 1 - Fetch body params
    let { actionType, actionValue, siteKey, sessionId="" } = req.body;

    
    cookieId = undefined
    // 2 - Fetch cookieID or Set it
    if(req.cookies)
      cookieId = req.cookies["cookieId"];
    if (!cookieId) {
      cookieId = uuidv4();
      res.cookie("cookieId", cookieId, {
        maxAge: 120 * 24 * 60 * 60 * 1000, // Duration is : 120 days
        httpOnly: false,
        sameSite: "none", 
        secure: true 
      });
    }

    // 3 - Save Action to database
    const action = {
      cookieId: cookieId,
      siteKey: siteKey || "site0", 
      actionType: actionType,
      actionValue: actionValue,
      sessionId: sessionId
    };
    const actionObject = new Action(action);
    await actionObject.save();

    res.status(200).json(action);
  } catch (error) {

    res.status(500).send({
      message: error.message || "Some error occurred",
    });
  }
};