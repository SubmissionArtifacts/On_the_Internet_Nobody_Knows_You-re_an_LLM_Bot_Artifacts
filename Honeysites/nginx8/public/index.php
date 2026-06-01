<?php
// Call sessions 
session_start();

// 1. Prepare server-side dynamic data
$domainKey = "site8";
$backendUrl = "https://api.example.org";

// Fetch blog posts data from backend API
$postsJson = file_get_contents("$backendUrl/posts/$domainKey");
$posts = ($postsJson !== false) ? json_decode($postsJson, true) : [];
if (!is_array($posts)) $posts = [];

// Define and shuffle hidden links
$top_bar_links = [
  '<a href="https://example.org" style="color:white; margin:0 10px;">World Clock</a>',
  '<a href="https://site1.example.org" style="color:white; margin:0 10px;">Babylone</a>',
  '<a href="https://site2.example.org" style="color:white; margin:0 10px;">Akalaman</a>',
  '<a href="https://site3.example.org" style="color:white; margin:0 10px;">X879ILE</a>',
  '<a href="https://site4.example.org" style="color:white; margin:0 10px;">Terberestan</a>',
  '<a href="https://site5.example.org" style="color:white; margin:0 10px;">JUANXA</a>',
  '<a href="https://site6.example.org" style="color:white; margin:0 10px;">Dessika</a>',
  '<a href="https://site7.example.org" style="color: white; margin: 0 10px">New Atlantis</a>',
  '<a href="https://site9.example.org" style="color: white; margin: 0 10px">Coffee Kingdom</a>'
];

shuffle($top_bar_links);// Randomize the links order

$links = [
  '<div class="spaced-link"><a class="display-none-link" href="secret_files/empty.html">display: none</a></div>',
  '<div class="spaced-link"><a class="visibility-hidden-link" href="secret_files/index.html">visibility: hidden</a></div>',
  '<div class="spaced-link"><a class="offscreen-link" href="secret_files/secret.txt">off-screen</a></div>',
  '<div class="spaced-link"><a class="opacity-zero-link" href="secret_files/password.html">opacity: 0</a></div>',
  '<div class="spaced-link"><a class="hidden-link" href="secret_files/user.txt">white on white</a></div>'
];
shuffle($links);  // Randomize the links order

// Compute "wrong" current date and time with offsets
$offsetMinutes = -37; $offsetSeconds = -13; $offsetDays = -7876;
$offsetTotal = $offsetDays*24*3600 + $offsetMinutes*60 + $offsetSeconds;
$wrongTimestamp = time() + $offsetTotal;
$wrongDateStr = date("Y-m-d", $wrongTimestamp);
$wrongTimeStr = date("H:i:s", $wrongTimestamp);

// Create a Random Session ID
function generateRandomID() {
    return substr(base_convert(random_int(0, PHP_INT_MAX), 10, 36), 0, 8);
}

if (!isset($_SESSION["sessionID"])) {
    $_SESSION["sessionID"] = generateRandomID();
}

$randomSessionId = $_SESSION["sessionID"];

// Save the randomSessionID to a separate collection named sessionIds
$clientHeaders = getallheaders(); // Get the client headers
$ch = curl_init("$backendUrl/fingerprints/");

$data = [
  "sessionId" => $randomSessionId,
  "siteKey" => $domainKey,
  "headers" => $clientHeaders,
];

curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        "Content-Type: application/json",
        "Accept: application/json"
    ],
    CURLOPT_POSTFIELDS => json_encode($data),
]);

$response = curl_exec($ch);

if ($response === false) {
    die("cURL error: " . curl_error($ch));
}

$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Clock Blog - Lonparislin</title>
  <link rel="icon" type="image/x-icon" href="favicon.ico" />
  <style>
      body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        padding: 2rem;
        color: #333;
      }

      #clock-canvas {
        background: #fff;
        border: 1px solid #ccc;
        border-radius: 50%;
        display: block;
        margin: 0 auto 1rem;
      }

      #numerical-clock {
        text-align: center;
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 1rem;
      }

      .spaced-link {
        margin: 10px 0;
      }

      .blog-post {
        margin-top: 2rem;
        padding: 1rem;
        background: #fff;
        border-left: 5px solid #007bff;
      }

      .post-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
      }

      .display-none-link {
        display: none;
      }
      .visibility-hidden-link {
        visibility: hidden;
      }
      .offscreen-link {
        position: absolute;
        left: -9999px;
      }
      .opacity-zero-link {
        opacity: 0;
      }
      .hidden-link {
        color: #f4f4f4;
        background: #f4f4f4;
      }

      #blog-form {
        margin-top: 2rem;
      }
  </style>
  <!-- Matomo -->
  <script>
    var _paq = window._paq = window._paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
    _paq.push(['trackPageView']);
    _paq.push(['enableLinkTracking']);
    (function() {
      var u="//analytics.example.org/";
      _paq.push(['setTrackerUrl', u+'matomo.php']);
      _paq.push(['setSiteId', '1']);
      var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
      g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
    })();
  </script>
  <!-- End Matomo Code -->
</head>
<body>
  <!-- Top bar container (shuffled links) -->
  <div id="top-bar"
       style="
        background: #007bff;
        padding: 10px;
        color: white;
        text-align: center;
      " class="post-links"
      >
    <?= implode("", $top_bar_links) ?>
  </div>
  
  <h1>Clock Blog - Lonparislin</h1>

  <p><strong>Timezone:</strong> <span id="timezone-label"> - Lonparislinian Time Zone </span></p>
  <p><strong>Date:</strong> 
     <span id="wrong-date"><?= htmlspecialchars($wrongDateStr) ?></span>
  </p>
  <canvas id="clock-canvas" width="200" height="200"></canvas>
  <div id="numerical-clock"><?= htmlspecialchars($wrongTimeStr) ?></div>

  <p><strong>Current Unique ID:</strong> <span id="unique-id"><?= $randomSessionId ?></span></p>

  <!-- Blog Post Form -->
  <form id="blog-form" method="post" onsubmit="return false;">
    <label>First Name: <input type="text" id="first-name" required /></label><br/><br/>
    <label>Last Name: <input type="text" id="last-name" required /></label><br/><br/>
    <label>Post Content:<br/>
       <textarea id="blog-content" rows="4" cols="50" required></textarea>
    </label><br/><br/>
    <button type="submit">Post</button>
  </form>

  <!-- Example of an initial static post (could also be included in $posts) -->
  <div class="blog-post">
    <div class="post-header">ID: John Doe | kfj4748 | 7/23/2025, 12:16:31 PM</div>
    <p>Clocks are devices used to measure and display the passage of time. 
        They come in various forms, from traditional analog models with hands 
        that move around a dial, to digital versions that show numbers on a screen. 
        Clocks play a crucial role in organizing daily life, helping people keep 
        track of schedules, appointments, and routines. Over the centuries, 
        clockmaking has evolved from intricate mechanical designs to precise atomic 
        timekeeping. Whether hanging on a wall, worn on a wrist, or built into a 
        smartphone, clocks remain essential tools for modern living.
    </p>
  </div>

  <!-- Post history loaded from backend -->
  <div id="post-history">
    <?php foreach ($posts as $post): 
          $first = htmlspecialchars($post['firstName'] ?? '');
          $last  = htmlspecialchars($post['lastName'] ?? '');
          $author = htmlspecialchars($post['authorId'] ?? '');
          $dateStr = '';
          if (!empty($post['createdAt'])) {
              $ts = strtotime($post['createdAt']);
              $dateStr = $ts ? date("n/j/Y, g:i:s A", $ts) : '';
          }
          $dateStr = htmlspecialchars($dateStr);
          $content = nl2br(htmlspecialchars($post['textContent'] ?? ''));
    ?>
      <div class="blog-post">
        <div class="post-header">ID: <?= "$first $last" ?> | <?= $author ?> | <?= $dateStr ?></div>
        <p><?= $content ?></p>
      </div>
    <?php endforeach; ?>
  </div>

  <!-- Hidden links container (shuffled links) -->
  <div id="static-links" class="post-links">
    <?= implode("", $links) ?>
  </div>

  <script src="bundle.js" defer></script>
  <script defer>
    // Keep fingerprinting and interaction scripts
    window.onload = async () => {
      // For sending the fingerprint JS
      const domainKey = "site8";
      const timezoneLabel = "Lonparislinian Time Zone";
      const backendUrl = "https://api.example.org"; // Change to your backend domain/IP

      // To draw the clock 
      const wrongTimeOffset = { minutes: -37, seconds: -13, days: -7876 };

      function getWrongTimeAndDate() {
        const now = new Date();
        const wrong = new Date(now);
        wrong.setMinutes(now.getMinutes() + wrongTimeOffset.minutes);
        wrong.setSeconds(now.getSeconds() + wrongTimeOffset.seconds);
        wrong.setDate(now.getDate() + wrongTimeOffset.days);
        return wrong;
      }

      function drawClock(ctx, time) {
          const radius = ctx.canvas.height / 2;
          ctx.translate(radius, radius);
          ctx.clearRect(-radius, -radius, ctx.canvas.width, ctx.canvas.height);

          ctx.beginPath();
          ctx.arc(0, 0, radius - 5, 0, 2 * Math.PI);
          ctx.fillStyle = "#fff";
          ctx.fill();
          ctx.stroke();

          ctx.font = radius * 0.15 + "px Arial";
          ctx.textBaseline = "middle";
          ctx.textAlign = "center";
          for (let num = 1; num <= 12; num++) {
            const ang = (num * Math.PI) / 6;
            ctx.rotate(ang);
            ctx.translate(0, -radius * 0.85);
            ctx.rotate(-ang);
            ctx.fillText(num.toString(), 0, 0);
            ctx.rotate(ang);
            ctx.translate(0, radius * 0.85);
            ctx.rotate(-ang);
          }

          const hour = time.getHours() % 12;
          const minute = time.getMinutes();
          const second = time.getSeconds();

          drawHand(
            ctx,
            ((hour + minute / 60) * 30 * Math.PI) / 180,
            radius * 0.5,
            6
          );
          drawHand(
            ctx,
            ((minute + second / 60) * 6 * Math.PI) / 180,
            radius * 0.75,
            4
          );
          drawHand(ctx, (second * 6 * Math.PI) / 180, radius * 0.9, 2, "red");

          ctx.translate(-radius, -radius);
      }

      function drawHand(ctx, pos, length, width, color = "#333") {
        ctx.beginPath();
        ctx.lineWidth = width;
        ctx.lineCap = "round";
        ctx.strokeStyle = color;
        ctx.moveTo(0, 0);
        ctx.rotate(pos);
        ctx.lineTo(0, -length);
        ctx.stroke();
        ctx.rotate(-pos);
      }

      async function update() {
          const wrong = getWrongTimeAndDate();

          const canvas = document.getElementById("clock-canvas");
          const ctx = canvas.getContext("2d");
          drawClock(ctx, wrong);

          const hh = String(wrong.getHours()).padStart(2, "0");
          const mm = String(wrong.getMinutes()).padStart(2, "0");
          const ss = String(wrong.getSeconds()).padStart(2, "0");
          document.getElementById(
            "numerical-clock"
          ).innerText = `${hh}:${mm}:${ss}`;

          const y = wrong.getFullYear();
          const m = String(wrong.getMonth() + 1).padStart(2, "0");
          const d = String(wrong.getDate()).padStart(2, "0");
          document.getElementById("wrong-date").innerText = `${y}-${m}-${d}`;
      }

      // Utils for creating posts
      function getSessionID() {
        if (!sessionStorage.getItem("sessionID")) {
          // Use the Server Random generated ID 
          sessionStorage.setItem("sessionID", <?php echo json_encode($randomSessionId); ?>);
        }
        return sessionStorage.getItem("sessionID");
      }

      // First intit of the page (Set the clock and send the js fingerprint)
      update();
      
      // Set evCookieId to ""
      let evCookieIdVal = ""

      try {
        // Get the saved cookieId
        evCookieId = await window.getEverCookie("cookieId", false);
        let evCookieIdVal = evCookieId.value;
        //console.log("Check evCookieId : ", evCookieId)

        const result = await window.computeFingerprint();
        //console.log("Fingerprint:", result)
        // Send it to your server (adjust URL and method as needed)
        const res = await fetch(`${backendUrl}/fingerprints`, {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            attributesJS: result, 
            siteKey: domainKey,
            sessionId: getSessionID() 
           }),
        });

        const data = await res.json();

        console.log("Fingerprint sent successfully.");
        // save cookie
        const cookieId = data["cookieId"];

        if (!evCookieIdVal) {
          await window.setEverCookie("cookieId", cookieId, 120);
        }
      } catch (error) {
        console.error("Error computing or sending fingerprint:", error);
      }

      console.log("page is fully loaded");

      // Continue updating the clock every second
      setInterval(update, 1000);
      
      // When creating new post save post and render the posts 
      function renderNewPost(post) {
        const container = document.getElementById("post-history");

        const div = document.createElement("div");
        div.className = "blog-post";
        // we set the date to the current date
        div.innerHTML = `
          <div class="post-header">
            ID: ${post.firstName} ${post.lastName} | ${post.authorId} |
            ${new Date().toLocaleString()}
          </div>
          <p>${post.textContent}</p>
        `;

        container.prepend(div);
      }

      // Set the event listner
      document.getElementById("blog-form")
          .addEventListener("submit", async (e) => {
            e.preventDefault();
            const first = document.getElementById("first-name").value.trim();
            const last = document.getElementById("last-name").value.trim();
            const content = document.getElementById("blog-content").value.trim();

            const body = {
              firstName: first,
              lastName: last,
              textContent: content,
              siteKey: domainKey,
              cookieId: evCookieIdVal,
              authorId: getSessionID(),
            }

            await fetch(`${backendUrl}/posts/`, {
              method: "POST",
              credentials: "include",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(body),
            });

            e.target.reset();
            renderNewPost(body);
      });

      // Keep the same logic for page interactions --> 
      let mouseStatus = "NONE";
      let hasMovedSinceClick = false;
        
      window.addEventListener("mousedown", () => {
        if (mouseStatus !== "MOVE" && mouseStatus !== "CLICKED") {
          mouseStatus = "CLICKED";
          hasMovedSinceClick = false;
          console.log("Mouse clicked");
          fetch(`${backendUrl}/actions`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              siteKey: domainKey,
              actionType: "MOUSE_MOVE",
              actionValue: mouseStatus,
              sessionId: getSessionID(),
            }),
          }).then((res) => {
            //console.log(res);
          }).catch((err) => console.log(err));
        }
      });

      window.addEventListener("mousemove", (ev) => {
        if (ev.movementX !== 0 || ev.movementY !== 0) {
          if (!hasMovedSinceClick || mouseStatus !== "MOVE") {
            console.log("Mouse moved");
            mouseStatus = "MOVE";
            hasMovedSinceClick = true;
            fetch(`${backendUrl}/actions`, {
              method: "POST",
              credentials: "include",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                siteKey: domainKey,
                actionType: "MOUSE_MOVE",
                actionValue: mouseStatus,
                sessionId: getSessionID(),
              }),
            }).then((res) => {
            //console.log(res);
            }).catch((err) => console.log(err));
          }
        }
      });

      const firstName = document.getElementById("first-name");
      const lastName = document.getElementById("last-name");
      const blogContent = document.getElementById("blog-content");

      let formStatus = false;

      function setFormStatusOnce() {
        if (!formStatus) {
          formStatus = true;
          console.log("User interacted with a text input.");
          fetch(`${backendUrl}/actions`, {
              method: "POST",
              credentials: "include",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                siteKey: domainKey,
                actionType: "FILL_FORM",
                actionValue: formStatus,
                sessionId: getSessionID(),
              }),
            }).then((res) => {
              //console.log(res);
            }).catch((err) => console.log(err));
        }
      }

      // Use "input" or "focus" depending on how early you want to detect interaction
      [firstName, lastName, blogContent].forEach((input) => {
        input.addEventListener("input", setFormStatusOnce);
      });

      // Set StartTime on page load 
      let startTime = Date.now();
      let totalTime = 0;

      document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "hidden") {
          totalTime += Date.now() - startTime;
        } else {
          startTime = Date.now();
        }
      });

      window.addEventListener("beforeunload", () => {
        totalTime += Date.now() - startTime;
        
        fetch(`${backendUrl}/actions`, {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            siteKey: domainKey,
            actionType: "TIME_SPENT",
            actionValue: totalTime,
            sessionId: getSessionID(),
          }),
          }).then((res) => {
            console.log("Total time spent (ms):", totalTime);
          }).catch((err) => console.log(err));
      });
    };
  </script>
</body>
</html>