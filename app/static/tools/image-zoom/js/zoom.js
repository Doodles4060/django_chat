function imageZoom(imgID, resultID) {
    var img, lens, result, cx, cy;
    img = document.getElementById(imgID);
    result = document.getElementById(resultID);

    lens = document.createElement("DIV");
    lens.setAttribute("class", "img-zoom-lens");
    img.parentElement.insertBefore(lens, img);

    // Initialize the lens size and zoom level
    var lensSize = 40; // Default lens size (you can adjust this as needed)
    lens.style.width = lensSize + "px";
    lens.style.height = lensSize + "px";

    cx = result.offsetWidth / lens.offsetWidth;
    cy = result.offsetHeight / lens.offsetHeight;

    result.style.backgroundImage = "url('" + img.src + "')";
    result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";

    lens.addEventListener("mousemove", moveLens);
    img.addEventListener("mousemove", moveLens);
    lens.addEventListener("touchmove", moveLens);
    img.addEventListener("touchmove", moveLens);

    // Mouse wheel to resize the lens
    lens.addEventListener("wheel", function (e) {
        e.preventDefault(); // Prevents the page from scrolling
        let newSize = lens.offsetWidth + (e.deltaY < 0 ? 5 : -5); // Increase or decrease size based on wheel direction

        // Ensure lens size is within a range (20px to 100px)
        if (newSize >= 20 && newSize <= 100) {
            // Store current cursor position
            var cursorPos = getCursorPos(e);

            lens.style.width = newSize + "px";
            lens.style.height = newSize + "px";

            // Recalculate the background size based on the new lens size
            cx = result.offsetWidth / lens.offsetWidth;
            cy = result.offsetHeight / lens.offsetHeight;
            result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";

            // Reposition the lens to center it on the cursor position
            var x = cursorPos.x - (lens.offsetWidth / 2);
            var y = cursorPos.y - (lens.offsetHeight / 2);

            // Prevent lens from going out of bounds
            if (x > img.width - lens.offsetWidth) { x = img.width - lens.offsetWidth; }
            if (x < 0) { x = 0; }
            if (y > img.height - lens.offsetHeight) { y = img.height - lens.offsetHeight; }
            if (y < 0) { y = 0; }

            lens.style.left = x + "px";
            lens.style.top = y + "px";

            result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
        }
    });

    function moveLens(e) {
        var pos, x, y;
        e.preventDefault();
        pos = getCursorPos(e);
        x = pos.x - (lens.offsetWidth / 2);
        y = pos.y - (lens.offsetHeight / 2);

        if (x > img.width - lens.offsetWidth) { x = img.width - lens.offsetWidth; }
        if (x < 0) { x = 0; }
        if (y > img.height - lens.offsetHeight) { y = img.height - lens.offsetHeight; }
        if (y < 0) { y = 0; }

        lens.style.left = x + "px";
        lens.style.top = y + "px";

        result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
    }

    function getCursorPos(e) {
        var a, x = 0, y = 0;
        e = e || window.event;
        a = img.getBoundingClientRect();

        x = e.pageX - a.left;
        y = e.pageY - a.top;

        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        return { x: x, y: y };
    }
}
