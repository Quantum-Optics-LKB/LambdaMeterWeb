// utils.js

// Function to calculate background gradient from the wavelength value
function nmToRGB(wavelength) {
  var Gamma = 0.8,
    IntensityMax = 255,
    factor,
    red,
    green,
    blue;

  if (wavelength >= 380 && wavelength < 440) {
    red = -(wavelength - 440) / (440 - 380);
    green = 0.0;
    blue = 1.0;
  } else if (wavelength >= 440 && wavelength < 490) {
    red = 0.0;
    green = (wavelength - 440) / (490 - 440);
    blue = 1.0;
  } else if (wavelength >= 490 && wavelength < 510) {
    red = 0.0;
    green = 1.0;
    blue = -(wavelength - 510) / (510 - 490);
  } else if (wavelength >= 510 && wavelength < 580) {
    red = (wavelength - 510) / (580 - 510);
    green = 1.0;
    blue = 0.0;
  } else if (wavelength >= 580 && wavelength < 645) {
    red = 1.0;
    green = -(wavelength - 645) / (645 - 580);
    blue = 0.0;
  } else if (wavelength >= 645 && wavelength < 781) {
    red = 1.0;
    green = 0.0;
    blue = 0.0;
  } else {
    red = 0.0;
    green = 0.0;
    blue = 0.0;
  }

  // Let the intensity fall off near the vision limits
  if (wavelength >= 380 && wavelength < 420) {
    factor = 0.3 + (0.7 * (wavelength - 380)) / (420 - 380);
  } else if (wavelength >= 420 && wavelength < 701) {
    factor = 1.0;
  } else if (wavelength >= 701 && wavelength < 781) {
    factor = 0.3 + (0.7 * (780 - wavelength)) / (780 - 700);
  } else {
    factor = 0.0;
  }

  if (red !== 0) {
    red = Math.round(IntensityMax * Math.pow(red * factor, Gamma));
  }
  if (green !== 0) {
    green = Math.round(IntensityMax * Math.pow(green * factor, Gamma));
  }
  if (blue !== 0) {
    blue = Math.round(IntensityMax * Math.pow(blue * factor, Gamma));
  }

  return [red, green, blue];
}

// Function to apply a background gradient based on the wavelength
function makebg(element, wavelength, freq, configBackground) {
  if (configBackground) {
    element.css({
      background: configBackground,
      color: "white",
    });
  } else {
    if (freq) {
      var wl = 3e8 / wavelength;
      var v = nmToRGB(wl);
    } else {
      var v = nmToRGB(wavelength);
    }

    var color = d3.rgb(v[0], v[1], v[2]);
    var c1 = color;
    var c2 = color.darker(2);
    element.css({
      background: "linear-gradient(135deg, " + c2 + " 0%," + c1 + " 100%)",
      color: "white",
    });
  }
  if (!element.hasClass("colored")) {
    element.addClass("colored");
  }
}

// Function to reset the background
function resetbg(element) {
  if (element.hasClass("colored")) {
    element.removeClass("colored");
    element.css({
      background: "transparent",
      color: "inherit",
    });
  }
}

$(document).ready(function() {
    $('#channel-select').multiselect({
        includeSelectAllOption: true,
        enableFiltering: true,
        maxHeight: 150,
        buttonWidth: '150px',
        nonSelectedText: 'Select Channels',
        nSelectedText: 'Channels hidden',
        allSelectedText: 'All channels hidden',
        templates: {
            button: '<button type="button" class="multiselect dropdown-toggle btn btn-sm btn-secondary" data-toggle="dropdown"></button>'
        }
    });

    // Initialize by showing all channels
    $('#channel-select').multiselect('refresh');
});