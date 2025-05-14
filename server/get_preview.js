const spotifyPreviewFinder = require('spotify-preview-finder');

const [,, trackName, artistName] = process.argv;
if (!trackName || !artistName) {
  console.error("Usage: node get_preview.js <track> <artist>");
  process.exit(1);
}

(async () => {
  try {
    const query = `${trackName} ${artistName}`;
    const result = await spotifyPreviewFinder(query, 1);
    if (result.success && result.results.length > 0 && result.results[0].previewUrls.length > 0) {
      const previewUrl = result.results[0].previewUrls[0];
      console.log(previewUrl);
    } else {
      console.error("No preview found");
      process.exit(2);
    }
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(3);
  }
})();
