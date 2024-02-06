var contentsElement = document.querySelector('#contents.style-scope.ytmusic-playlist-shelf-renderer');
var songs = document.querySelectorAll('ytmusic-responsive-list-item-renderer.style-scope.ytmusic-playlist-shelf-renderer');

songs.forEach(song => {
    const artist = song.querySelector('ytmusic-responsive-list-item-renderer.style-scope.ytmusic-playlist-shelf-renderer yt-formatted-string.flex-column.style-scope[title]');
    const title = song.querySelector('yt-formatted-string.title.style-scope');

    var artistOut = "";
    var titleOut = "";

    if (artist) {
        const artistText = artist.textContent.trim();

        // Check if there is a comma in the  text
        var firstArtist = artistText
        const commaIndex = artistText.indexOf(',');

        if (commaIndex !== -1) {
            // Extract the text before the first comma
            firstArtist = artistText.substring(0, commaIndex).trim();
        } else {
            // If no comma, take the entire text
            firstArtist = artistText.trim();
        }
        artistOut = firstArtist;
    }

    if (title) {
        const titleText = title.textContent.trim();
        titleOut += titleText;
    }

    console.log(artistOut + " - " + titleOut);
});

