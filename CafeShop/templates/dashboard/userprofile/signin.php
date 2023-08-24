<?php
// Database connection details
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "db_cafeshop";

// Create a connection to the database
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Authenticate the user (you need to replace `users` and `password_column` with your actual table and column names)
    $sql = "SELECT * FROM userprofile_signup WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        // Authentication successful, redirect to the Django 'home' view
        header("Location: /home/");  // Replace with your Django 'home' URL pattern
        exit();
    } else {
        // Authentication failed, display an error message or redirect back to the sign-in page
        echo "Authentication failed. Please try again.";
    }
}

$conn->close();
?>
