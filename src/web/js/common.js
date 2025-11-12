document.addEventListener("DOMContentLoaded", () => {
  const langSelect = document.getElementById("language-selector");
  const textElements = document.querySelectorAll("[data-en][data-de]");
  const savedLang = getCookie("language");

  if (savedLang) {
    langSelect.value = savedLang;
    applyLanguage(langSelect.value);
  }

  langSelect.addEventListener("change", () => {
    applyLanguage(langSelect.value);
    setCookie("language", langSelect.value);
  });

  function applyLanguage(lang) {
    document.documentElement.lang = lang;
    textElements.forEach((el) => {
      el.textContent = el.dataset[lang];
    });
  }

  function setCookie(name, value, days = 30) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
  }

  function getCookie(name) {
    return document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="))
      ?.split("=")[1];
  }
});
