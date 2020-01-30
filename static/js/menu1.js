(function() {
    "use strict";

    document.addEventListener("keydown", function(event) {
        let key = event.key;

        switch(key) {
            case "1":
                window.location.replace(`/choosecam`);
                break;
            case "2":
                window.location.replace(`/dualcam`);
                break;
            // case "4":
            //     console.log("Single camera.");
            //     window.location.replace("/selectcam/" + key);
            //     break;
            // case "5":
            //     window.location.replace("/");
            //     break;
            // case "7":
            //     // var camera = prompt("Välj kamera", "1-4");
            //     window.location.replace("/selectbox")
            //     // var delay = prompt("Välj delay", "sekunder");
            //     // // var inst = prompt("Antal instanser", "1-4");
            //     // // var delta = prompt("Ange delta", "sekunder");
            //     // if (delay != null) {
            //     //     window.location.replace("/stream/" + delay);
            //     // }
            //     break;
            // case "8":
            //     var camera = prompt("Välj kamera", "1-4");
            //     var time = prompt("Hur många sekunder?", "sekunder");
            //     if (camera != null && time != null) {
            //         window.location.replace("/record/" + camera + "/" + time);
            //     }
            //     break;
            // case "9":
            //     // window.location.replace("/kill");
            //     window.location.replace("/fourcams");
            //
            //     break;


            case "0":
                window.location.replace("/");
                break;

        }
    })

})();
