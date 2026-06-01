const { faker } = require('@faker-js/faker');

function generateId() {
  return Math.random().toString(36).substring(2, 10);
}


function getRandomText(zone) {
  const headlineTemplates = [
    "New economic alliance formed in the {zone} region.",
    "Scientists discover strange atmospheric patterns above {zone}.",
    "Tensions rise between factions in {zone}, say experts.",
    "Historic peace treaty signed today in {zone}.",
    "Citizens of {zone} celebrate a record-breaking solar harvest.",
    "{zone} authorities launch major investigation into cyber heists.",
    "Cultural renaissance sparks innovation boom in {zone}.",
    "Earthquake rattles the eastern edge of {zone}, no casualties reported.",
    "Secret AI project leaks in {zone}, causing international concern.",
    "Environmental activists push green policies across {zone}.",
    "Medical breakthrough reported in a {zone} research facility.",
    "Unprecedented solar flare disrupts comms in {zone}.",
    "Military drills escalate near the border of {zone}.",
    "{zone} bans fossil fuel vehicles starting next decade.",
    "Mystery signals detected from deep underground in {zone}.",
    "Mass migration observed as climate shifts affect {zone}.",
    "{zone} hosts first inter-zone tech summit.",
    "Archaeologists uncover ancient artifacts near {zone}.",
    "Wildfires sweep across southern {zone}, prompting evacuations.",
    "Biodiversity study reveals surprising trends in {zone}.",
    "Energy independence achieved in {zone} using fusion tech.",
    "Skybridge network opens, connecting {zone} to orbital stations.",
    "{zone} declares state of emergency after flash floods.",
    "Artificial intelligence appointed to lead {zone}'s planning council.",
    "Meteor fragment recovered near {zone} sparks scientific gold rush.",
    "Unrest grows as controversial policy passes in {zone}.",
    "{zone} achieves zero-emissions milestone ahead of schedule.",
    "Time capsule opened in {zone}, revealing messages from a lost generation.",
    "Drone surveillance increased following threats in {zone}.",
    "Massive black market raid in {zone} yields surprising results.",
    "Education reforms launch in {zone}, targeting STEM expansion.",
    "{zone} tech firm unveils quantum encryption for civilians.",
    "Ancient virus revived in {zone}'s permafrost — scientists monitor closely.",
    "Genetic engineering debate heats up in {zone}'s parliament.",
    "Rare celestial event draws tourists to {zone}.",
    "{zone} celebrates centennial of planetary independence.",
    "Civilians protest water privatization plans in {zone}.",
    "Cyberattack on {zone}'s banking network temporarily halts economy.",
    "New language dialect recognized officially in {zone}.",
    "{zone} zone-wide blackout traced to solar grid overload.",
    "Breakthrough in synthetic food tech announced in {zone}.",
    "Cultural archives digitized by AI across {zone}.",
    "{zone} wins bid to host the next Pan-Zone Games.",
    "Hyperloop project connects {zone} with outer provinces.",
    "Holographic education trial expands to rural {zone}.",
    "{zone} introduces universal basic income for all citizens.",
    "Decentralized government model tested in {zone}.",
    "Cryptocurrency replaces national currency in {zone}.",
    "Climate dome installed to protect downtown {zone}.",
    "Virtual reality therapy replaces traditional methods in {zone}.",
    "High-speed AI judiciary rolled out in {zone} courts."
  ];

  // Select a random template
  const template = headlineTemplates[Math.floor(Math.random() * headlineTemplates.length)];

  // Replace all occurrences of {zone} with the given zone
  return template.replace(/{zone}/g, zone);
}


/**
 * Generate fake posts for a given site key.
 * @param {string} siteKey - The site key to assign to each post.
 * @param {number} numberOfPosts - How many fake posts to generate.
 * @returns {Array<Object>} - Array of post objects.
 */
function generateFakePosts(siteKey, numberOfPosts) {
  const posts = [];
  const siteNames = {
    "site1": "Babylone", 
    "site2": "Akalaman", 
    "site3": "X879ILE", 
    "site4": "Terberestan", 
    "site5": "JUANXA", 
    "site6": "Dessika", 
    "site7": "New Atlantis", 
    "site8": "Lonparislin", 
    "site9": "Coffee Kingdom", 
    "site0": "World Clock", 
  }
  for (let i = 0; i < numberOfPosts; i++) {
    const post = {
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      textContent: getRandomText(siteNames[siteKey]),
      //textContent: faker.lorem.paragraphs({ min: 1, max: 3 }),
      siteKey: siteKey,
      cookieId:  "fakeCookieId",
      authorId: generateId(),
      createdAt: faker.date.recent({ days: 30 })  // Created within the last 30 days
    };

    posts.push(post);
  }

  return posts;
}

module.exports = {
  generateFakePosts,
};