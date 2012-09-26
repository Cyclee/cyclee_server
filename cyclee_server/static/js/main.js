/*global define:true, requirejs:true, alert: true  */

requirejs.config({

    shim: {
        'underscore': {exports: '_'},
        'backbone'  : {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    }

});

define(['jquery', 'Trace', 'Traces'], function ($, Trace, Traces) {
    'use strict';

    $(function () {
        var traces = new Traces();
        traces.fetch();
        console.log(traces);
    });

});