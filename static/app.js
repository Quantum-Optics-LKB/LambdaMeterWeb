$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('WebSocket connected!');
        $('#modal').hide();
        setInterval(function() {
            socket.emit('request_update');
        }, 100);  // Update every second
    });

// Listen for real-time updates from the server
socket.on('update_channels', function(data) {
    // Loop through each channel and update only the data inside each channel's `div`
    for (var i = 0; i < channels.length; i++) {
        var value = isWavelengthsPage 
            ? `${data.wavelengths[i].toFixed(precision)} nm` 
            : `${data.frequencies[i].toFixed(precision)} GHz`;

        // Update the specific div for each channel
        $(`#wl${i}`).text(value);

        const configBackground = channels[i].background || null; 
        // If we're displaying wavelengths, apply the background gradient based on the wavelength
        if (isWavelengthsPage) {
            makebg($(`#wl${i}`).parent(), data.wavelengths[i], false, configBackground);
        } else {
            makebg($(`#wl${i}`).parent(), data.frequencies[i], true, configBackground);
        }

    }
});

    socket.on('disconnect', function() {
        $('#modal').show();
    });

    socket.on('reconnect', function() {
        $('#modal').hide();
    });

        // Handle channel selection
        $('#channel-select').change(function () {
            // Get the selected channels
            var selectedChannels = $(this).val();
            
            // Loop through each channel div
            $('.container > div').each(function () {
                var channelId = $(this).attr('id').replace('container', '');  // Extract the channel ID from the div ID
                
                // Show or hide the channel based on whether it is selected
                if (selectedChannels.includes(channelId)) {
                    $(this).show();  // Show channel if it's selected
                } else {
                    $(this).hide();  // Hide channel if it's not selected
                }
            });
        });
    
        // Initialize by selecting all channels by default
        $('#channel-select option').prop('selected', true).trigger('change');
});
