document.addEventListener("DOMContentLoaded", () => {
    const endpoint = "http://127.0.0.1:6789/get_startup_time";
    let lastStartupTime = null;
    console.log("Checking endpoint...");
    async function checkEndpoint() {
      try {
        const response = await fetch(endpoint, { method: "GET"});
        if (!response.ok) throw new Error("Endpoint not available");
        const startupTime = await response.text();

        if (lastStartupTime === null) {
          // First successful check, save the startup time
          lastStartupTime = startupTime;
        } else if (startupTime !== lastStartupTime) {
          // Startup time has changed, reload the page
          console.log("Startup time changed. Reloading...");
          window.location.reload(true);
        }
      } catch (error) {
        console.error("Error checking endpoint:", error);
        try {
            clearInterval(intervalId); // Stop checking if the endpoint becomes unavailable

        } catch (error) {
            console.error("Error clearing interval:", error);
        }
      }
    }

    // Check if the endpoint exists initially
    checkEndpoint().then(() => {
      // Set up periodic checks if the endpoint is available
      window.intervalId = setInterval(checkEndpoint, 1000); // Check every 1 second
    });
  });