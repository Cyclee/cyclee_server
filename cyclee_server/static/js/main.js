/*global define:true, requirejs:true, alert: true  */

requirejs.config({

    shim: {
        'libs/underscore': {exports: '_'},
        'libs/jquery.mobile': {
            deps: ['jquery'],
        },
        'libs/backbone'  : {
            deps: ['libs/underscore', 'jquery'],
            exports: 'Backbone'
        }
    }

});

define([
    'jquery',
    'libs/jquery.mobile',
    'Trace',
    'Traces'], function ($, Trace, Traces) {
    'use strict';

    $(function () {
        var traces = new Traces();
        traces.fetch();
        console.log(traces);
    });

});