/* Site settings — fill these in, then push. Empty values switch the feature off safely. */
window.BUNDLE = {
  formspreeId: "",          // e.g. "xyzabcd" from https://formspree.io/f/xyzabcd
  cloudflareToken: "",      // Cloudflare Web Analytics token
  supportEmail: "support@meetbundle.com",
  company: "Meet Bundle"
};
(function(){var t=window.BUNDLE.cloudflareToken;if(!t)return;var s=document.createElement('script');s.defer=true;s.src='https://static.cloudflareinsights.com/beacon.min.js';s.setAttribute('data-cf-beacon',JSON.stringify({token:t}));document.head.appendChild(s)})();
