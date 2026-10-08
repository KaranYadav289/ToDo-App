document.addEventListener("DOMContentLoaded", function () {

    // 1. Animate table rows one after another
    document.querySelectorAll("tbody tr").forEach(function (row, index) {
        row.classList.add("row-animate");
        row.style.animationDelay = (index * 0.08) + "s";
    });

    // 2. Ripple effect on every button click
    document.querySelectorAll(".btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            var rect = btn.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
            var ripple = document.createElement("span");
            ripple.className = "ripple";
            ripple.style.width = ripple.style.height = size + "px";
            ripple.style.left = (e.clientX - rect.left - size / 2) + "px";
            ripple.style.top = (e.clientY - rect.top - size / 2) + "px";
            btn.appendChild(ripple);
            setTimeout(function () { ripple.remove(); }, 600);
        });
    });

    // 3. Highlight the correct navbar link for the current page
    var currentPath = window.location.pathname;
    var links = document.querySelectorAll(".navbar-nav .nav-link");
    links.forEach(function (link) {
        var href = link.getAttribute("href");
        if (href && href.charAt(0) === "/") {
            link.classList.remove("active");
            if (href === currentPath) {
                link.classList.add("active");
            }
        }
    });

    // 4. Reveal elements when they scroll into view (used on About page)
    var revealItems = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealItems.forEach(function (item, i) {
            item.style.transitionDelay = ((i % 3) * 0.12) + "s";
            observer.observe(item);
        });
    } else {
        revealItems.forEach(function (item) { item.classList.add("visible"); });
    }

    // 5. Prevent double submit on the Add form
    var form = document.querySelector('form[action="/"]');
    if (form) {
        form.addEventListener("submit", function () {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = "Adding...";
                setTimeout(function () { submitBtn.disabled = true; }, 0);
            }
        });
    }
});