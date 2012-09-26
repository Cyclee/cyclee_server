/*global define: true */

define(['libs/backbone', 'Trace'], function (Backbone, Trace) {
    'use strict';

    var Traces = Backbone.Collection.extend({
        models: Trace,
        url: '/traces'
    });

    return Traces;
});