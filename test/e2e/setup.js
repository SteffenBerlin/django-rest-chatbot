process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

var chakram = require('chakram');

chakram.addMethod("body", function (respObj, expected) {
    var body = respObj.body;

    if (arguments.length === 1) {
        this.assert(
            body !== undefined && body !== null,
            'expected body to exist',
            'expected not to exist'
        );
    } else if (expected instanceof RegExp) {
        this.assert(
            expected.test(body),
            'expected body with value ' + body + ' to match regex ' + expected,
            'expected body with value ' + body + ' not to match regex ' + expected
        );
    } else if (typeof(expected) === 'function') {
        expected(body);
    } else {
        this.assert(
            body === expected,
            'expected body with value ' + body + ' to match ' + expected,
            'expected body with value ' + body + ' not to match ' + expected
        );
    }
});

var settings = {
    headers: {},
    followRedirect: false,
    baseUrl: '',
};

chakram.getRequestSettings = function () {
    return settings;
};

chakram.setRequestSettings = function (s) {
    settings = s;
    chakram.setRequestDefaults(settings);
};
chakram.setRequestSettings(settings);

chakram.setRequestHeader = function (header, value) {
    var s = chakram.getRequestSettings();
    s.headers[header] = value;
    chakram.setRequestSettings(s);
};

exports.chakram = chakram;
