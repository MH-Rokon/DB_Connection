<?php
// Enable error reporting for troubleshooting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Database connection details for PostgreSQL
$host = "dpg-csdvkr3v2p9s73b2bkog-a";
$port = "5432";
$dbname = "preventers";
$user = "preventers_user";
$password = "xR7u0DpZsQRdyArWZGmrCQ7zMrH53lQp";

try {
    // Set up the DSN for PostgreSQL
    $dsn = "pgsql:host=$host;port=$port;dbname=$dbname";
    $pdo = new PDO($dsn, $user, $password);

    // Set error mode to exception for easier debugging
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Set the region_id to retrieve
    $region_id = 2;

    // SQL query to retrieve the latest weather data for the specified region_id
    $sql = "
    SELECT temperature, wind_speed, humidity, current_instruction
    FROM weather_data 
    WHERE region_id = :region_id 
    AND id = (SELECT MAX(id) FROM weather_data WHERE region_id = :region_id);
    ";

    // Prepare and execute the statement
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':region_id', $region_id, PDO::PARAM_INT);
    $stmt->execute();
    $data = $stmt->fetch(PDO::FETCH_ASSOC);

    // Check if data was found
    if ($data) {
        // Output data in JSON format
        $ordered_data = [
            'temperature' => $data['temperature'],
            'wind_speed' => $data['wind_speed'],
            'humidity' => $data['humidity'],
            'current_instruction' => $data['current_instruction'],
        ];
        echo json_encode($ordered_data);
    } else {
        echo json_encode(["error" => "No data found"]);
    }
} catch (PDOException $e) {
    // Handle connection and query errors
    echo json_encode(["error" => "Connection or query failed: " . $e->getMessage()]);
}
?>
