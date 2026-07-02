(function () {
  "use strict";

  var internalHosts = {
    "ritheshkumar.com": true,
    "www.ritheshkumar.com": true,
    "ritheshkumar95.github.io": true
  };

  function clean(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function compact(value, limit) {
    value = clean(value);
    return value.length > limit ? value.slice(0, limit - 3) + "..." : value;
  }

  function slug(value) {
    return clean(value)
      .toLowerCase()
      .replace(/^https?:\/\//, "")
      .replace(/^www\./, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 80) || "unknown";
  }

  function sourcePage() {
    var path = clean(window.location.pathname).replace(/^\/+|\/+$/g, "");
    return path ? slug(path) : "home";
  }

  function isDownload(url) {
    return /\.(pdf|zip|tar|gz|docx?|pptx?|xlsx?|csv)$/i.test(url.pathname);
  }

  function classify(url) {
    if (url.protocol === "mailto:") return "email";
    if (url.protocol === "tel:") return "phone";
    if (isDownload(url)) return "download";
    if (internalHosts[url.hostname]) return "internal";
    if (url.protocol === "http:" || url.protocol === "https:") return "outbound";
    return null;
  }

  function destination(link, url, kind) {
    if (kind === "email") return url.pathname;
    if (kind === "phone") return url.pathname;
    if (kind === "download") return url.pathname.split("/").filter(Boolean).pop();
    if (kind === "internal") return url.pathname + url.hash;
    return url.hostname.replace(/^www\./, "") + url.pathname.replace(/\/$/, "");
  }

  function titleFor(link, url, kind, dest) {
    var label = link.getAttribute("aria-label") ||
      link.getAttribute("title") ||
      clean(link.textContent) ||
      dest;

    return compact("Click: " + label + " [" + kind + "] from " + window.location.pathname, 200);
  }

  function shouldTrack(link, url, kind) {
    if (!kind) return false;
    if (link.dataset.analyticsIgnore === "true") return false;
    if (url.hash && url.pathname === window.location.pathname && url.hostname === window.location.hostname) {
      return false;
    }
    return true;
  }

  function sendClick(link) {
    if (!window.goatcounter || typeof window.goatcounter.count !== "function") return;

    var url;
    try {
      url = new URL(link.getAttribute("href"), window.location.href);
    } catch (error) {
      return;
    }

    var kind = classify(url);
    if (!shouldTrack(link, url, kind)) return;

    var dest = destination(link, url, kind);
    window.goatcounter.count({
      path: ["click", sourcePage(), kind, slug(dest)].join(":"),
      title: titleFor(link, url, kind, dest),
      event: true,
      no_session: true
    });
  }

  document.addEventListener("click", function (event) {
    var target = event.target;
    var link = target && target.closest ? target.closest("a[href]") : null;
    if (link) sendClick(link);
  }, true);

  document.addEventListener("auxclick", function (event) {
    var target = event.target;
    var link = target && target.closest ? target.closest("a[href]") : null;
    if (link) sendClick(link);
  }, true);
})();
