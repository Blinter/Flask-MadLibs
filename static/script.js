$(window).on("load", () => {
    $('#story_ask').on("submit", (e) => {
        for(item of $('#story_ask :input')) {
            if($(item).attr('id') === undefined)
                continue;
            $(item).val($(item).val().trim().toLowerCase());
            if($(item).val().length < 3) {
                alert("Invalid input length: Please ensure all fields are 3 or more characters long.")
                e.preventDefault();
                break;
            }
        }
    });
});
