const enJson =
  'https://raw.githubusercontent.com/tmrowco/electricitymap-contrib/master/web/locales/en.json';

$.getJSON(enJson, function (enJson) {
  $.each(enJson['zoneShortName'], function (key, entry) {
    value = key;
    text = entry.zoneName;
    if ('countryName' in entry) {
      text = entry.countryName + ' - ' + text;
    }
    $('#zoneSelect').append(
      '<option value="' + value + '">' + text + '</option>',
    );
  });
});

$(document).ready(function () {
  $('#zoneSelect').change(function () {
    stopConnectionCalls();
  });
  $('.toggle').on('click', function () {
    if ($('#toggle-trigger').prop('checked') == true) {
      stopConnectionCalls();
    } else {
      var zone = $('#zoneSelect').children('option:selected').val();
      var selector = $('#bulbSelector').val();
      var lifxApiKey = $('#lifxApiKey').val();
      var co2SignalApiKey = $('#co2SignalApiKey').val();

      if (
        zone != 'Choose one of the following zones...' &&
        selector &&
        lifxApiKey &&
        co2SignalApiKey
      ) {
        $('#connected-alert').show();
      } else {
        $('#missing-alert').show();
      }
    }
  });
});

function stopConnectionCalls() {
  // $('#toggle-trigger').prop('checked', false).change();
  $('#missing-alert').hide();
  $('#connected-alert').hide();
}
