<?php

// Grab URL from query string.
$url = '';
if (isset($_GET['url'])) {
  // Escape command (very important for security).
  url = escapeshellcmd($_GET['url']);
} else {
  http_response_code(400); // Give 400 bad request.
  echo json_encode(['error' => 'No URL supplied.']);
  die();
}

// Assemble command.
$command = __DIR__ . '/detector.py --url ' . $url;

// Echo output of detector.
$output = shell_exec($command);
echo json_encode(['url' => $url, 'is_phishing' => $output]);
