function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

    const isDark =
        document.body.classList.contains("dark-mode");

    localStorage.setItem(
        "darkMode",
        isDark
    );

}

window.onload = function () {

    const darkMode =
        localStorage.getItem("darkMode");

    if (darkMode === "true") {

        document.body.classList.add("dark-mode");

    }

}