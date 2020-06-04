function login(event) {
    event.preventDefault();

    let username = $("#username").val();
    let password = $("#password").val();

    $("#incorrect-creds").hide();

    if (username.length === 0) {
        $("#username-box").html(`<label class="label">Username</label>
        <div class="control has-icons-left">
            <input class="input is-danger" id="username" type="text">
            <span class="icon is-small is-left">
              <i class="fas fa-user"></i>
            </span>
        </div>
        <p class="help is-danger">This is a required field.</p>`)
    } else {
        $("#username-box").html(`<label class="label">Username</label>
        <div class="control has-icons-left">
            <input class="input" id="username" type="text">
            <span class="icon is-small is-left">
              <i class="fas fa-user"></i>
            </span>
        </div>`)
    };

    if (password.length === 0) {
        $("#password-box").html(`<label class="label">Password</label>
        <div class="control has-icons-left">
            <input class="input is-danger" id="password" type="password">
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
        </div>
        <p class="help is-danger">This is a required field.</p>`)
    } else {
        $("#password-box").html(`<label class="label">Password</label>
        <div class="control has-icons-left">
            <input class="input" id="password" type="password">
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
        </div>`)
    };

    if (username.length !== 0 & password.length !== 0) {
        $.ajax({
            url: "/api/authenticate",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(res) {
                document.cookie = `_auth_token=${res.token}; path=/; expires=2038-01-19 04:14:07`;
                window.location.replace("/");
            },
            error: function(res) {
                $("#incorrect-creds").show();
            }
        });
    }
};