const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json()); // Python se aane wale JSON data ko read karne ke liye
app.set("view engine", "ejs");

// Database Connection
const db = mysql.createConnection({
  host: "localhost",
  user: "root", // Apna SQL username daalo
  password: "password", // Apna SQL password daalo
  database: "arp_ids",
});

db.connect((err) => {
  if (err) {
    console.error("Database connection failed:", err);
  } else {
    console.log("Connected to SQL Database successfully!");
  }
});

// ---------------------------------------------------------
// 1. POST Route: Python script se alert receive karne ke liye
// ---------------------------------------------------------
app.post("/api/alerts", (req, res) => {
  // Python se jo data bheja gaya tha, use nikalna
  const { attacker_mac, target_ip } = req.body;

  if (!attacker_mac || !target_ip) {
    return res.status(400).json({ error: "Incomplete data received" });
  }

  // Data ko SQL database me insert karne ki query
  const sql = "INSERT INTO alerts (attacker_mac, target_ip) VALUES (?, ?)";

  db.query(sql, [attacker_mac, target_ip], (err, result) => {
    if (err) {
      console.error("Error saving alert to DB:", err);
      return res.status(500).json({ error: "Failed to save alert" });
    }
    console.log(
      `[ALERT SAVED] Fake MAC: ${attacker_mac} targeting IP: ${target_ip}`,
    );
    res.status(200).json({ message: "Alert saved successfully!" });
  });
});

// ---------------------------------------------------------
// 2. GET Route: Frontend Dashboard pe data dikhane ke liye
// ---------------------------------------------------------
app.get("/", (req, res) => {
  // Database se saare alerts fetch karo, naye wale pehle (DESC)
  const sql = "SELECT * FROM alerts ORDER BY alert_time DESC";

  db.query(sql, (err, results) => {
    if (err) {
      console.error("Error fetching data:", err);
      return res.status(500).send("Database fetching error");
    }
    // Saara data 'index.ejs' file ko pass kar do
    res.render("index", { alerts: results });
  });
});

// Start Server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
