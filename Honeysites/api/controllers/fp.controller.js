const Fingerprint = require("../models/fp.model");
const { v4: uuidv4 } = require("uuid");


exports.create = async (req, res) => {
   try {
    // 1 - Fetch body params
    let attributesHTTP = req.headers;
    let { attributesJS = {}, headers = null, siteKey, sessionId = "" } = req.body;
   
    if (headers != null)
      attributesHTTP = headers
    
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


    // 3 - Save fingerprint to database
    const fp = {
      cookieId: cookieId,
      siteKey: siteKey || "site0", 
      sessionId: sessionId,
      ...attributesJS,
      ...attributesHTTP,
    };
    const fingerprint = new Fingerprint(fp);
    await fingerprint.save();

    res.status(200).json(fp);
  } catch (error) {

    res.status(500).send({
      message: error.message || "Some error occurred",
    });
  }
};