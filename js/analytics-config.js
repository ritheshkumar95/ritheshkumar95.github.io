(function () {
  "use strict";

  var campaignKeys = [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref"
  ];

  window.goatcounter = window.goatcounter || {};
  window.goatcounter.referrer = function (defaultReferrer) {
    var params = new URLSearchParams(window.location.search);
    var campaign = campaignKeys
      .map(function (key) {
        var value = params.get(key);
        return value ? key + "=" + value : "";
      })
      .filter(Boolean)
      .join("&");

    return campaign || defaultReferrer;
  };
})();
