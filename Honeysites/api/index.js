// Import dependencies
const express = require("express");
const database = require("./utils/db");
const cors = require("cors");
const cookieParser = require("cookie-parser");



require("dotenv").config();

// Create app instance
const app = express();

// Use cookie-parser
app.use(cookieParser());

// Use cors
const allowedDomain = "example.org";
const corsOptions = {
    origin: function (origin, callback) {
      if (!origin) return callback(null, true); // allow non-browser clients (curl, Postman)
      try {
        const hostname = new URL(origin).hostname;
        if (
          hostname === allowedDomain ||
          hostname.endsWith("." + allowedDomain)
        ) {
          console.log(hostname)
          callback(null, origin);
        } else {
          callback(new Error("Not allowed by CORS"));
        }
      } catch (error) {
        callback(new Error("Not allowed by CORS"));
      }
    },
    credentials: true,
    methods: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Accept", "Authorization"],
};

app.use(cors(corsOptions));
app.options("*", cors(corsOptions));

// Define JSON as return type
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extend: true, limit: "50mb" }));

// ✅ Root endpoint test
app.get("/", (req, res) => {
  res.status(200).json({ api: "This world clock blog API" });
});

// ✅ Post-related routes
app.use("/posts", require("./routes/post.routes")); // Handles routes like /posts/
// ✅ Fingerprint-related routes
app.use("/fingerprints", require("./routes/fp.routes")); // Handles routes like /fingerprints/
// ✅ Action-related routes
app.use("/actions", require("./routes/action.routes")); // Handles routes like /fingerprints/
// ✅ Challenge-related routes
app.use("/challenges", require("./routes/challenge.routes")); // Handles routes like /fingerprints/

// ✅ 404 fallback (no route matched)
app.all(/.*/, (req, res) => {
   res.status(404).json({ error: "Endpoint not found" });
});

// Handle database error
database.on("error", (error) => {
  console.log("Connection error: --------------------------");
  console.log(error);
  console.log("--------------------------------------------");
});

// Start app after connecting to Database
database.once("connected", async () => {
  console.log("Database Connected");

  const PORT = process.env.APP_PORT || 5000;
  app.listen(PORT, () => console.log("Server ready at port " + PORT));
});
