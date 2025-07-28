document.addEventListener("DOMContentLoaded", function() {
    const avatar = document.querySelector(".avatar-placeholder");
    const modal = document.getElementById("screenshotModal");
    const img = document.getElementById("screenshotImage");
    const refresh = document.getElementById("refreshScreenshot");
    const fechar = document.getElementById("fecharScreenshot");

    if (avatar && modal && img && refresh && fechar) {
        avatar.style.cursor = "pointer";
        avatar.title = "Clique para ver o print da sessão";

        avatar.addEventListener("click", function() {
            modal.style.display = "flex";
        });

        refresh.addEventListener("click", function() {
            img.src = "http://192.168.99.41:3100/api/screenshot?session=default&t=" + Date.now();
        });

        fechar.addEventListener("click", function() {
            modal.style.display = "none";
        });
    }
});
