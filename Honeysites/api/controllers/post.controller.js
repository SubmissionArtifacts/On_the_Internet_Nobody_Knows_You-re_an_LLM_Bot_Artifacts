const PostModel = require("../models/post.model");
const { generateFakePosts } = require("../utils/post.faker");

exports.create = async (req, res) => {
  try {
    if (!req.body) {
      return res.status(400).send("No post sent.");
    }
    const { firstName, lastName, textContent, siteKey, cookieId, authorId } =
      req.body;
    const headers = req.headers;

    // Create a new MongoDB document
    const newDocument = new PostModel({
      firstName: firstName,
      lastName: lastName,
      textContent: textContent,
      siteKey: siteKey,
      httpHeaders: headers,
      cookieId: cookieId,
      authorId: authorId,
    });

    // Save the document in MongoDB
    await newDocument.save();

    console.log("Post inserted successfully as one MongoDB object ");
    res.status(200).json({ status: "Data saved" });
  } catch (error) {
    console.error("Error occurred:", error);
    res.status(500).json({ status: "Error occurred" });
  }
};

// Create and Save a new Document
exports.getPostsBySiteKey = async (req, res) => {
  const { sitekey } = req.params;
  const fakePosts = generateFakePosts(sitekey,5)
  try {
    const posts = await PostModel
    .find({ siteKey: sitekey })
    .sort({ createdAt: -1 }) // newest first
    .limit(5); // return 5 last inserted posts

    // Merge and sort by most recent createdAt
    const mergedPosts = [...posts, ...fakePosts].sort((a, b) => {
      return new Date(b.createdAt) - new Date(a.createdAt);
    });
  
    res.status(200).json(mergedPosts);
  } catch (error) {
    console.error("Error fetching posts:", error);
    res.status(500).json({ message: "Server error" });
  }
};
