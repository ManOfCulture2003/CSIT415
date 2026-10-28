<?php
// Configure a local database with environment variables; never commit passwords.
$host = getenv('DB_HOST') ?: '127.0.0.1';
$dbname = getenv('DB_NAME') ?: 'libraryDB';
$username = getenv('DB_USER') ?: 'root';
$password = getenv('DB_PASSWORD') ?: '';
$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    http_response_code(503);
    error_log('Database connection failed: ' . $conn->connect_error);
    exit('Database temporarily unavailable.');
}
$conn->set_charset('utf8mb4');
?>
