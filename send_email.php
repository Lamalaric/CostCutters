<?php
// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get form data
    $author = htmlspecialchars($_POST["author"]);
    $title = htmlspecialchars($_POST["title"]);
    $content = htmlspecialchars($_POST["content"]);

    // Email details
    $to = "amalaric.leforestier@gmail.com";
    $subject = "New Message from $author: $title";
    $message = "You have received a new message from $author.\n\n" . $content;
    $headers = "From: amalaric.leforestier@gmail.com"; // Replace with your domain or email

    // Send the email
    if (mail($to, $subject, $message, $headers)) {
        echo "<p class='success-message'>Message sent successfully! Thank you for contacting us.</p>";
    } else {
        echo "<p class='error-message'>Failed to send your message. Please try again later.</p>";
    }
} else {
    // Redirect to the contact form if the script is accessed directly
    header("Location: testindex.html");
    exit;
}
?>