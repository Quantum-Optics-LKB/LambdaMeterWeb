$(document).ready(function () {
  var socket = io.connect("http://" + document.domain + ":" + location.port);
  var update_time=30 // Update 30 msecond (30Hz)

  socket.on("connect", function () {
    console.log("WebSocket connected!");
    $("#modal").hide();
    setInterval(function () {
      socket.emit("request_update");
    }, update_time); 
  });

  // Listen for real-time updates from the server
  socket.on("update_channels", function (data) {
    // Loop through each channel and update only the data inside each channel's `div`
    for (var i = 0; i < channels.length; i++) {
      var value;
      if (isDetuningPage) {
        value = `${data.detunings[i].toFixed(precision)} GHz`; // Detuning in GHz
      } else if (isWavelengthsPage) {
         value = `${data.wavelengths[i].toFixed(precision)} nm`; // Wavelength in nm
      } else {
         value = `${data.frequencies[i].toFixed(precision)} GHz`; // Frequency in GHz
      }

      // Update the specific div for each channel
      $(`#wl${i}`).text(value);

      const configBackground = channels[i].background || null;
      if (isWavelengthsPage) {
        makebg(
          $(`#wl${i}`).parent(),
          data.wavelengths[i],
          false,
          configBackground
        );
      } else {
        makebg(
          $(`#wl${i}`).parent(),
            data.frequencies[i],
          true,
          configBackground
        );
      }
    }
  });

  socket.on("disconnect", function () {
    $("#modal").show();
  });

  socket.on("reconnect", function () {
    $("#modal").hide();
  });



  $("#channel-select").change(function () {
    var selectedChannels = $(this).val();
    // Loop through each channel div
    $(".container > div").each(function () {
      var channelId = $(this).attr("id").replace("container", ""); 
      if (selectedChannels.includes(channelId)) {
        $(this).show(); // Show channel if it's selected
      } else {
        $(this).hide(); // Hide channel if it's not selected
      }
    });
  });
  // Initialize by selecting all channels by default
  $("#channel-select option").prop("selected", true).trigger("change");
});
